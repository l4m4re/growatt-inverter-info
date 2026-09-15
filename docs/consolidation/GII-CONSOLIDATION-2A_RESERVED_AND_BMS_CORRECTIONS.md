# GII-CONSOLIDATION-2A — Reserved-range and BDC/BMS corrections

This bounded offline correction preserves the immutable C2 audit snapshots and regenerates a corrected V2 candidate projection. The frozen canonical specification is unchanged.

## Lineage and safety

- Starting/main and C2 parent SHA: `1c9c0d34e819d6839958cd9b7a2ae4e2d2cff4a8`
- Frozen canonical SHA before/after: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`
- V1.24 PDF SHA-256: `fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320`
- No HA, broker, inverter, Shine, cloud, live API, or configuration operation was performed.
- Historical C2 JSON/Markdown snapshots remain immutable; C2A outputs are phase-specific corrections.

## Corrected classification

| Subject | C2 before | C2A after |
|---|---|---|
| I3281–I3374 | `DIFFERENT_PROTOCOL_OR_SOURCE_REQUIRED` (94) | `RESERVED_VENDOR_RANGE` (94) |
| H3116–H3123 | `CANONICAL_ONLY_PHYSICAL_REGISTER` (8) | `CANONICAL_CONFLICTS_WITH_VENDOR_RESERVED_RANGE` (8) |
| H3115–H3124 | no range-level status | explicit V1.24 `RESERVED` range |

I3281–I3374 have no individual semantic row in the candidate register list. They are inside the explicitly declared V1.24 FC04 block I3250–I3374 and are represented as reserved/unused words. Shine polling and the all-zero runtime observations corroborate that treatment; they do not create additional semantic definitions.

## H3085/H3086 semantic scope

- H3085 is `bdc_bms_slave_address`: read/write, default `1`, range `1..254`, subsystem `bdc_bms`, interface `sys_com_rs485_battery`.
- H3086 is `bdc_bms_rs485_baud_rate`: read/write, default `0`, with `0 = 9600 bps` and `1 = 38400 bps`, on the same subsystem/interface.
- The structured ARK XH-A1 excerpt identifies BDC INV RS485 pins 7/8 with MIN TL-XH SYS COM pins 7/8. Interface scope is documented; inverter-master/BDC-slave remains a high-confidence inference, not a vendor claim.
- H3085 is not treated as a DDSU666 external-meter address. Input I3085 is retained as a V1.24 Reserved word.

## Metrics

- Canonical physical keys: `895` (not used as the V1.24 denominator).
- V1.24-defined MIN/TL-XH candidate physical keys: `648`.
- MIN/TL-XH applicability envelope words: `750`; explicit reserved range words: `10`; declared-block words without semantic rows: `94`.
- Candidate register count remains `1486`; candidate conflicts reduce to `4` after the two H3085 semantic resolutions.
- Corrected gap category counts: `{'CANONICAL_CONFLICTS_WITH_VENDOR_RESERVED_RANGE': 8, 'OUTSIDE_VENDOR_V124_APPLICABILITY': 145, 'RESERVED_VENDOR_RANGE': 94, 'RESOLVED_BY_LOCAL_EXTRACTION_REPAIR': 130}`.
- Active research queue: `1` item containing the four retained access conflicts; the H3085, H3116–H3123, and I3281–I3374 items are removed.

## Deferred scope

The four retained access conflicts remain explicitly unresolved for a later bounded review. Master/slave direction remains inferred at high confidence. No unrelated canonical semantic, access, scaling, unit, or runtime consumer record was changed.

## Generated artifacts

- `spec/growatt-register-spec-v2-candidate.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2A_RESERVED_AND_BMS_CORRECTIONS.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2A_MIN_TL_XH_GAP_CLASSIFICATION.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2A_MIN_TL_XH_PROJECTION.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2A_CONFLICTS.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2A_UNRESOLVED.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2A_RESEARCH_QUEUE.json`
- `sources/evidence/ark-xh-a1-bdc-rs485.json`

`GII_C2A_RESERVED_AND_BMS_CORRECTIONS_ACCEPTED_WITH_FOLLOW_UP`
