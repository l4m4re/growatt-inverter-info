# GII-MIN-RE-3 — MIN/TL-XH status, fault and warning fields

Date: 2026-09-12  
Scope: read-only vendor/API/live-Modbus reconciliation for the MIN 6000TL-XH

## Disposition

`GII_MIN_STATUS_FAULT_WARNING_RECONCILIATION_WITH_FOLLOW_UP`

The vendor V1.24 specification remains the primary interpretation source. The
Growatt V4/V1 API and a bounded live FC04 read were used only as secondary
cross-checks. No canonical record, Home Assistant code, broker behaviour or
inverter configuration was changed.

Starting `growatt-inverter-info` SHA: `9e81cb373705700dbcf873b1d9d9faaeaa426fa8`  
Implementation SHA: not applicable (evidence-only report)

## Evidence collected

### Vendor source

The primary source was
`sources/vendor/growatt-v1.24-tables.json`, input table pages 47, 50–60 and
70–82. The source distinguishes explicit enums and bitfields from fields for
which it provides only a name such as “fault code”, “warning code” or
“system fault word”. An unnamed `bitfield` is not sufficient evidence for a
bit-to-meaning decoder.

### Growatt API

Read-only V4 current/history and V1 current-data calls were made with the
already authorised token. No identifier or token was retained in this report.

The relevant current API observations were:

| API field | Observed value/domain | Interpretation |
|---|---:|---|
| `status`, `status_text` | `1`, `Normal` | Supports the vendor normal status value. |
| `fault_type`, `fault_type1` | `0` | No current inverter fault reported. |
| `warn_code`, `warn_code1`, `new_warn_code`, `new_warn_sub_code` | `0` | No current API warning code reported. This does not identify a physical Modbus register. |
| `derating_mode` | `0` | Consistent with no derating at the time of the call. |
| `bdc_status`, `bdc1_status`, `bdc1_mode` | `1`, `1`, `2` | Consistent with BDC1 connected, normal and discharging. |
| `bdc1_fault_type`, `bdc1_warn_code` | `0`, `0` | No BDC1 fault/warning reported. |
| `bms_status` | `2` | Consistent with BMS discharging. |
| BMS error/warning fields | `0` | No current BMS error/warning reported. |
| alarms | one historical `Warning401` event | Cloud alarm identity; no vendor evidence equates 401 to a Modbus word. |

The API models are not themselves a wire-level specification. Their status
comments also use different domains for different device models, so API
normalisation must not replace the vendor register definitions.

### Live Modbus cross-check

Two complete, read-only FC04 vendor-page reads were obtained through
`192.168.1.148:5021`, unit 1:

* `start=3000, count=125`: 125 words, approximately 31 ms;
* `start=3125, count=125`: 125 words, approximately 33 ms.

The selected raw values were:

| Register | Raw value | Immediate evidence |
|---|---:|---|
| I3000 | `1` (`0x0001`) | Lower-byte status is `Normal`; upper-byte mode is zero. |
| I3086 | `0` | No derating, consistent with API `derating_mode=0`. |
| I3104 | `0` | None of the documented standby bits set. |
| I3105–I3108 | `0` | No current main/sub fault or warning code in these words. |
| I3110 | `505` (`0x01f9`) | Non-zero unnamed vendor bitfield; must not be called an active warning solely from this value. |
| I3111 | `110` (`0x006e`) | Vendor calls this Present FFT channel A, not a warning code. |
| I3112 | `0` | No AFCI state indicated. |
| I3118 | `1` | BDC1 connected. |
| I3119 | `0` | Dry contact off. |
| I3164 | `0` | No separate BDC data flag. |
| I3165 | `22` (`0x0016`) | Conflicts with the vendor-documented BDC derating enum domain `0..4`. |
| I3166 | `513` (`0x0201`) | Packed value: upper byte `2` = discharge, lower byte `1` = normal. |
| I3167–I3168 | `0` | No BDC1 fault/warning code. |
| I3187 | `3` (`0x0003`) | Bits 0 and 1 set: charging and discharging allowed. |
| I3199 | `0` | No BMS derate reason in this word. |
| I3202–I3205 | `0` | No observed BMS protect/warning/fault flags. |
| I3210 | `0` | Battery insulation detection not completed according to the vendor enum. |
| I3211 | `0` | None of the documented battery request bits set. |
| I3212 | `2` | Vendor BMS status `Discharge`; API also reported `2`. |
| I3213–I3214, I3225–I3226 | `0` | No observed additional BMS flags. |

## Field classification from the vendor source

### Explicit enums

These should be represented as enums, retaining the raw value for unknown or
future firmware values:

* **I0** — legacy inverter status: `0 waiting`, `1 normal`, `3 fault`.
* **I3000** — modern packed inverter status: high byte is the mode and low
  byte is the machine status. The vendor lists the mode values separately;
  it is not equivalent to a flat one-byte status enum.
* **I104/I3086** — derating mode. I3086 has documented values 0–16.
* **I141** — PID status in the low byte: wait, normal or fault; upper byte
  reserved.
* **I206** — packed SVG/APF ratio and status.
* **I238/I3112** — AFCI status, values 0–4.
* **I3118** — BDC connection state, values 0–3.
* **I3119** — dry-contact state, 0/1.
* **I3164** — BDC data separation flag, 0/1.
* **I3165** — BDC derating mode, documented values 0–4.
* **I3166** — packed BDC1 mode/status: high byte mode, low byte status.
* **I3210** — battery insulation detection, 0/1.
* **I3212** — BMS status: dormancy, charge, discharge, free, standby,
  soft-start, fault or update.

The API/live cross-check supports I3000, I3086, I3118, I3166 and I3212 for the
current operating point. It does not prove every enum member.

### Explicit bitfields

These have vendor-defined bit positions and are suitable for structured
decoding once the canonical metadata represents the complete word:

* **I177** — PID fault: output overvoltage, insulation fault and abnormal bus
  voltage; bits 3–15 reserved.
* **I229** — fan fault bits 0–3; bits 4–7 reserved.
* **I3104** — standby flags: turn-off order, PV low, AC voltage/frequency out
  of scope; bits 3–7 reserved.
* **I3187** — BDC1 charge/discharge enable, warning subcode and fault subcode.
* **I3211** — charging prohibition, strong-charge and strong-charge-2 bits.
  The later vendor text also describes discharge-prohibition and power-
  reduction bits; these remain part of the source evidence and need firmware
  validation before being presented as universally applicable.

The current canonical record for I3187 is marked signed. A bitfield is
intrinsically an unsigned raw word; this is a correction candidate, but it was
not silently edited in this evidence task.

### Raw codes/words with no safe bit or enum expansion

The V1.24 source names these fields but does not provide a usable code table or
bit-to-meaning mapping for this model/document revision:

* **I105/I3105** — inverter fault main code;
* **I106/I3106** — inverter warning main code;
* **I107/I3107** — inverter fault subcode (the source says `bitfield`, but
  gives no bit definitions);
* **I108/I3108** — inverter warning subcode (same limitation);
* **I110** — `WarningbitH`;
* **I111** — inverter warning subcode;
* **I112** — inverter warning main code;
* **I115** — aggregate inverter fault code;
* **I1001–I1008** — system fault words, with a reference to a separate
  Hybrid fault description;
* **I1082–I1085 and I1098–I1099** — older BMS status/error/warning words;
* **I3110** — unnamed vendor bitfield;
* **I3167/I3168** — BDC fault/warning codes;
* **I3199** — BMS derate reason;
* **I3202–I3205, I3213/I3214, I3225/I3226** — BMS protect/warning/fault
  words without individual bit definitions.

These should remain raw unsigned words unless a family-specific source adds a
defensible code table. A field being called “warning”, “fault” or “status” is
not enough to infer that it is a boolean, a bitfield with known meanings, or an
enum.

## Important unresolved correlations

### I3110/I3111 versus API system-fault fields

The live read returned I3110=`505` and I3111=`110`. The API simultaneously
reported top-level warning fields as zero, while its `sys_fault_word3` and
`sys_fault_word4` values were observed around `505` and `109/110` in
current history/current data.

This is evidence of a cloud-to-physical mapping or naming collision, not proof
that I3110 is an active warning. The V1.24 source leaves I3110 unnamed and
explicitly labels I3111 as Present FFT channel A. The API field comments place
`sys_fault_word*` in a different logical block. Exact physical mapping remains
unresolved and needs either a known-good frame/register correlation or a
firmware/source-level mapping.

### I3165 versus `bdc_derate_reason`

The API reported `bdc_derate_reason=22`, matching the live raw I3165 value, but
the vendor source defines I3165 as a BDC derating-mode enum with only values
0–4. I3199 was zero in the same live read and is named `BmsDerateReason` by the
vendor.

Possible explanations include a vendor table label/address discrepancy, an API
field-name mismatch, or a firmware-specific overloaded word. The current
evidence is insufficient to choose between them. The canonical record must
not be rewritten from the API label alone. This is the highest-priority
follow-up before exposing I3165 as a decoded enum in runtime code.

### Cloud `Warning401`

The V4 alarm endpoint returned one historical cloud event named
`Warning401`. No V1.24 register table in the reviewed fields defines code
401, and no live Modbus word was proven to contain it. It is therefore retained
as a cloud alarm observation only.

## Recommended bounded follow-up

1. Preserve raw words for I3105–I3112, I3165–I3168 and the system/BMS word
   ranges in future captures.
2. Repeat the complete native FC04 pages over several operating states and
   compare each raw word with the API response at the same timestamp.
3. Resolve I3165 by correlating a documented derating transition or by finding
   an independent family-specific source; do not infer it from the name
   `bdc_derate_reason`.
4. Treat I3110/I3111 and API `sys_fault_word*` as separate namespaces until a
   physical mapping is demonstrated.
5. In a later canonical metadata change, correct only evidence-supported
   representation defects, notably unsigned representation for bitfields such
   as I3187. Do not invent bit names for undocumented words.

## Change-control statement

This task was read-only with respect to the inverter, broker, Home Assistant
and the Growatt account. No write/configuration endpoint was called, no
Modbus write was sent, and no canonical register record was changed.

## Follow-on publication and runtime integration

The reviewed findings are now consumed by the generated canonical GII
specification. The publication represents I3000 and I3166 as separate
mode/status byte fields, gives the vendor-defined enums for I0, I3086, I3118,
I3164, I3165, I3210 and I3212, and expands the documented I3104, I3187 and
I3211 flag fields. I3187 and I3211 are explicitly unsigned. The unresolved
words listed above remain raw and are not given invented meanings.

The HA runtime keeps the existing raw status, fault, warning, BMS and energy
entity identities. It now exposes the proven enum/bitfield interpretations as
diagnostic attributes and adds raw diagnostic entities for the previously
unmapped MIN/TL-XH BDC/status words. The I3164 entity label is corrected from
“BDC present” to “BDC data separation” without changing its entity key or
unique ID. No inverter, broker or production-HA state was changed by this
follow-on implementation.
