# GII-PIPELINE-2A — MIN/TL-XH EMS source review

Status: `GII_PIPELINE_MIN_XH_EMS_SOURCE_REVIEW_ACCEPTED_WITH_FOLLOW_UP`

Starting SHA: `79388da2f230912a8a2de19bd39e02b2d9176262`

This review adds source claims only. It does not modify the canonical register
specification, generated compatibility reference, Home Assistant consumers,
the broker, or live device state.

## Source and method

The primary source is the original V1.24 PDF:

`Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf`

SHA-256: `fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320`.

Pages 38–40 were reviewed with both embedded `pdftotext -layout -enc UTF-8`
extraction and rendered-page inspection. No OCR was needed. The review claims
retain source-column text separately from reconstructed split spellings and use
the source section scope `Use for TL-X and TL-XH`.

The installed extraction tools were Poppler `25.03.0` (`pdftotext`, `pdfinfo`,
`pdftoppm`). The reproducible commands for the suspect pages were:

```text
pdftotext -layout -f 38 -l 40 -enc UTF-8 <PDF> -
pdftoppm -f 38 -l 40 -png -r 170 <PDF> /tmp/gii-pipeline-2a/page
```

The original PDF was not modified and no derived PDF or page image is tracked.

The review sidecar is split into the existing status/bitfield review and an EMS
review file. The extractor now supports deterministic `include_files` in a
review sidecar, so the generated V1.24 claims artifact contains all 34 reviewed
claims while keeping the review threads independently auditable.

## Reviewed holding claims

The generated source artifact contains explicit reviewed claims for every
holding register H3036–H3059 and H3081–H3082. Their family scope is exactly
`["TL-X", "TL-XH"]`.

The V1.24 table states:

- H3036: `GridFirstDischargePowerRate`, “Discharge Power Rate when Grid First”, range `1-255`.
- H3037: `GridFirstStopSOC`, “Stop Discharge soc when Grid First”, range `1-100`.
- H3047: `BatFirstPowerRate`, “Charge Power Rate when Bat First”, range `1-100`.
- H3048: `wBatFirst stop SOC`, “Stop Charge soc when Bat First”, range `1-100`.
- H3049: `AcChargeEnable`, with visible `Enable:1` / `Disable:0` mapping.
- H3081: `UPSFreqSet`, R/W, initial `0`, `0:50Hz`, `1:60Hz`.
- H3082: `bLoadFirstStopSocSet`, “StopSoc When LoadFirst”, visible `13-100`, source unit/note `ratio`.

H3046 is retained as the vendor’s reserved row. No meaning is assigned to it.

## Packed schedule model in the source claims

The vendor describes generic priority schedule periods, not separate physical
“Grid First” and “Battery First” slot families:

| Words | Vendor schedule | Source interpretation |
|---|---|---|
| H3038/H3039 | Time 1 | start/control and end |
| H3040/H3041 | Time 2 | start/control and end |
| H3042/H3043 | Time 3 | `With Time1` template |
| H3044/H3045 | Time 4 | `With Time1` template |
| H3050/H3051 … H3058/H3059 | Time 5 … Time 9 | `With Time1` template |

For each start/control word, bits 0–7 are minutes, bits 8–12 are hours,
bits 13–14 select load/battery/grid priority, and bit 15 is prohibited versus
enabled. Each adjacent end word has minutes and hours in bits 0–12 and bits
13–15 reserved. The `With Time1` cells are explicitly retained as template
inheritance evidence; they are not silently converted into a different slot
family.

This is source evidence, not a canonical packed-field schema change. The
canonical model still needs a later reviewed correction for its current
Grid-first/Battery-first split and for any bogus enum values derived from bit
positions.

## Natural Shine TOU evidence

The retained broker checkpoint records one naturally observed action: disabling
TOU Time Period 2 through the Shine/portal path. It associates an FC16 (`0x10`)
write to H3040–H3041 with payload `0x2000 0x0700`, followed by a confirming
read. The reviewed state transition is H3040 `0xA000` → `0x2000` while H3041
remains `0x0700`; this is consistent with clearing bit 15 while retaining the
time word.

The machine-readable evidence file records the deterministic request PDU
reconstruction, but deliberately leaves the raw request, CRC, physical FC16
acknowledgement, and FC03 readback frames null. A targeted search of the
retained broker logs, bounded JSONL captures, and the documented FC20 analysis
artifacts did not recover those byte-level lines. The logical event is retained
as reviewed broker-session evidence, not upgraded to byte-level
`write_verified` evidence.

## Canonical follow-up defects

The source review makes three existing canonical follow-ups concrete:

1. The current canonical records split the periods into Grid-first and
   Battery-first families, while this vendor table describes generic priority
   slots.
2. Bit positions must not be emitted as ordinary enum values; the start/control
   and end words are packed fields with reserved bits.
3. A future canonical packed-field representation should preserve the source
   bit ranges, masks, reserved bits, and `With Time1` inheritance explicitly.

No canonical changes are made in this task.

## Validation and safety

The V1.24 source artifact was regenerated deterministically and contains 1,527
claims, including 34 manually reviewed claims. The new golden test checks all
26 EMS rows, family scope, schedule priority/enable/reserved bits, inheritance,
and H3081/H3082 source cells. No live reads or writes were performed and no
runtime/configuration files were changed.

The exact test and full-suite results are recorded in the handoff for this
branch. The remaining follow-up is recovery or re-capture of the raw natural
TOU write/readback if byte-level CRC evidence is required.
