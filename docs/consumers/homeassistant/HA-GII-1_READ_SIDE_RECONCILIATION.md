# HA-GII-1 — Home Assistant read-side reconciliation

Status: audit completed; no Home Assistant, broker, inverter, or live
configuration changes were made.

This report reconciles the Home Assistant consumer source with the canonical
Growatt Register Specification. It is an audit of the read-side contract, not
a proposal to change entity identities or to make live Modbus reads.

## Reproducibility and scope

| Item | Value |
| --- | --- |
| Canonical repository | `growatt-inverter-info` |
| Canonical commit | `4296c596091bc118c953c69c39b8d625107fb083` |
| Consumer repository | `Homeassistant-Growatt-Local-Modbus` |
| Consumer branch | `integration/register-spec-consolidation-20260911` |
| Consumer source commit | `ddfa899d171a2eb84cc9d78d2d1fe3c5a50171f2` |
| Canonical families | `min_tl_xh`, `storage_mix` |
| Tables | holding and input |
| Mapping occurrences checked | 299 |
| Unique physical mappings checked | 230 |
| Unique physical mappings with findings | 84 |
| Existing GII runtime findings carried forward | 24 |

The audit used the consumer's existing extractor and a temporary snapshot. No
private Home Assistant state, serial numbers, recorder data, or network
credentials is included in the public artifact. The development runtime source
was inspected read-only and had no content differences from the checked
consumer source at the time of the audit. Its private entity registry was
examined only for compatibility context; it contained 95 Growatt entities and
none were disabled. No live broker read, inverter read, serial access, write,
or deployment was performed for this audit.

The machine-readable result is
[`HA-GII-1_READ_SIDE_FINDINGS.json`](HA-GII-1_READ_SIDE_FINDINGS.json). It
contains every checked mapping, the effective decoder inferred from the
consumer implementation, the canonical record, evidence, and the required
action.

## Findings by mapping occurrence

The following counts are occurrence counts, because one physical register can
be declared in more than one device/group. The JSON also retains the unique
physical finding count.

| Classification | Occurrences | Meaning |
| --- | ---: | --- |
| `MATCH` | 203 | No consumer change identified |
| `SIGNEDNESS_MISMATCH` | 85 | Effective HA decoder signedness differs from canonical metadata |
| `LENGTH_MISMATCH` | 3 | Declared read length differs from the canonical physical/logical interpretation |
| `UNIT_MISMATCH` | 2 | Entity unit differs from canonical engineering unit |
| `NEEDS_LIVE_VALIDATION` | 6 | Canonical scale remains unresolved; current HA scale is recorded, not endorsed |
| **Total** | **299** | |

Required actions are 203 `NO_HA_CHANGE`, 88 `DECODE_FIX_REQUIRED`, one
`SAFE_METADATA_FIX`, one `GII_FOLLOW_UP_REQUIRED`, and six
`NEEDS_MORE_EVIDENCE` occurrences.

The signedness count is largely explained by the consumer's current decoder:
two-word `float` mappings are decoded as signed 32-bit values regardless of
the declaration's signed flag. This is a real implementation behavior and is
why the audit compares effective decoding, not only dataclass metadata.

## All 24 existing GII runtime findings

The previous canonical runtime audit is preserved rather than hidden. The
current consumer declarations account for all 24 unique findings:

| Physical register | Current field | Finding |
| --- | --- | --- |
| MIN input 3001 | `input_power` | signedness |
| MIN input 3005 | `input_1_power` | signedness |
| MIN input 3009 | `input_2_power` | signedness |
| MIN input 3023 | `output_power` | signedness |
| MIN input 3028 | `output_1_power` | signedness |
| MIN input 3047 | `operation_hours` | signedness |
| MIN input 3049 | `output_energy_today` | signedness; energy continuity risk |
| MIN input 3071 | `energy_to_grid_today` | signedness; energy continuity risk |
| MIN input 3073 | `energy_to_grid_total` | signedness; energy continuity risk |
| MIN input 3101 | `real_output_power_percent` | signedness |
| MIN input 3110 | `warning_code` | length and semantic interpretation |
| MIN input 3170 | `battery_current` | signedness; negative-current behavior needs validation |
| MIX input 1009 | `discharge_power` | signedness |
| MIX input 1011 | `charge_power` | signedness |
| MIX input 1021 | `pac_to_user_total` | signedness; not an energy entity |
| MIX input 1029 | `pac_to_grid_total` | signedness; not an energy entity |
| MIX input 1044 | `energy_to_user_today` | signedness; energy continuity risk |
| MIX input 1046 | `energy_to_user_total` | signedness; energy continuity risk |
| MIX input 1048 | `energy_to_grid_today` | signedness; energy continuity risk |
| MIX input 1050 | `energy_to_grid_total` | signedness; energy continuity risk |
| MIX input 1052 | `discharge_energy_today` | signedness; energy continuity risk |
| MIX input 1054 | `discharge_energy_total` | signedness; energy continuity risk |
| MIX input 1056 | `charge_energy_today` | signedness; energy continuity risk |
| MIX input 1058 | `charge_energy_total` | signedness; energy continuity risk |

The repeated occurrences of MIN 3071, MIN 3073, and MIN 3170 explain why the
24 unique findings produce 27 occurrences in the older GII projection.

## I3110 and adjacent warning/diagnostic words

Canonical I3110 is `min_tl_xh:input:3110`:

- one physical `u16` word;
- vendor-defined warning bitfield;
- semantic key `inverter.warning_flags`;
- no safe individual bit meanings;
- source-only, low-confidence interpretation;
- retained evidence from the V1.24 vendor source and implementation
  correlation, not a proven old two-word `/10` warning-code value.

The consumer currently declares `warning_code` at I3110 with a two-word integer
read. That is both a length mismatch and a semantic/value continuity risk. The
next HA patch should read I3110 as one word and preserve the existing entity
identity while explicitly deciding how the entity presents a raw warning
bitfield. I3111 must remain a separate one-word `present_fft_a` mapping; it is
not the second word of the warning code.

I110 in the older/common mapping has the same length issue. I39 is different:
the canonical source currently describes a two-word physical field while the
consumer declares one word. That case requires a GII/source-layout review
before changing the consumer; it must not be “fixed” mechanically from this
audit alone.

## GII-2A correction impact

- I3021 is reactive power in `var`, signed and `/10`. The consumer entity is
  called reactive wattage and advertises `W`; this is a metadata correction,
  not a new physical quantity. Preserve the entity ID and source quantity.
- I3071–I3074 are unsigned `/10` grid-export energy counters. The current HA
  names are retained as grid-export energy aliases, but the effective decoder
  currently produces signed values. Any correction must include counter
  continuity validation.
- I3104 is a unitless bitfield and has no current HA mapping in the inspected
  groups.
- I3172 and I3173 are voltage values with `/10`; the current HA unit/scale is
  consistent.
- I3210 and I3212 are unitless enum/raw values; no consumer metadata change is
  indicated.
- I3232 is a `/100` battery-load voltage correction with no current HA mapping;
  this audit does not create an entity for it.

## Battery and BMS review

The inspected consumer surface covers the BMS/storage area, but canonical
confidence is not uniform across it. The following register areas remain
important for a later bounded implementation review:

| Area | Audit conclusion |
| --- | --- |
| I3164–I3168 | I3164 is a BDC data-separation flag, not “BDC present”; do not relabel it without an entity-contract review. |
| I3169–I3171 | I3170 is storage-device battery current and shares the semantic quantity with I3217, but it is a different measurement point. Its signedness is not live-sign validated. |
| I3176–I3177 | Keep as distinct BMS/device diagnostics until their exact semantics are proven. |
| I3191, I3194, I3195 | Scale remains unresolved; the current `/10` consumer scale is not endorsed. |
| I3196–I3197 | Parallel-battery maximum/minimum SOC diagnostics, not the actual battery SOC. Zero values alone are not grounds for disabling them. |
| I3200–I3205 | Some scale/behavior remains unresolved; suspicious values are investigation prompts, not permission to repurpose entities. |
| I3212–I3232 | Preserve proven raw/enum/cell-voltage meanings; I3230/I3231 are `/1000 V`, while I3232 is not currently exposed. |

I3217 is the stronger BMS-current reference: signed, `/100 A`, with a retained
negative live sample. It must not be conflated with I3170 merely because both
have semantic key `battery.current`.

The implementation recommendation is to keep the existing battery/BMS entity
surface until per-field evidence and the public HA contract have been reviewed.
Do not disable fields solely because a current installation reports zero, and
do not create new entities for unresolved diagnostic registers in this task.

## Grid, load, and energy semantics

The canonical semantic mapping is:

| HA field/alias | Canonical meaning | Contract handling |
| --- | --- | --- |
| `power_to_user` | grid import power | instantaneous W measurement |
| `power_to_grid` | grid export power | instantaneous W measurement |
| `power_user_load` | house/load power | instantaneous W measurement |
| `energy_to_user_today/total` | load energy | kWh, cumulative/total-increasing semantics |
| `energy_to_grid_today/total` | grid-export energy | kWh, cumulative/total-increasing semantics |
| `pac_to_user_total` / `pac_to_grid_total` | field-like power values with uncertain “total” naming | currently W measurements; do not reclassify as energy |

Changing an energy source later requires old/new interval deltas to agree,
known reset/rollover behavior, no artificial positive jump, and continuity of
existing Recorder long-term statistics. The entity ID, unique ID, unit,
device/state classes, physical quantity, sign convention, and counter semantics
are public contract fields. The consumer implementation uses the template
`growatt_local_<config_serial>_<field_key>` for unique IDs; no real serial is
published here.

## Cell precision and presentation

I3230/I3231 decode as `/1000 V`; the canonical values observed in the retained
evidence are consistent with that precision. The development entity registry
currently indicates display precision zero for these values, so a value such as
3.314 V can be displayed as `3 V` even though the source decode is correct. The
smallest future correction is presentation metadata (for example suggested
display precision 3), without changing source decoding or entity identity.

Similarly, I3021's `W` versus `var` is a metadata/semantic presentation issue;
it is not evidence for a new sensor. `real_output_power_percent` currently uses
the `power_factor` device class even though its semantic name is output-power
percentage. That metadata deserves a separate HA contract review.

## Continuity and migration rules

The findings divide into four practical categories:

1. **Decoder fixes:** unsigned versus signed interpretation, especially the
   two-word float path, I3110 read length, and the I39 source-layout follow-up.
2. **Safe metadata/presentation fixes:** reactive power unit and cell display
   precision; review the percentage device class.
3. **Semantic aliases only:** normalize names in the knowledge layer while
   retaining existing HA IDs and unique IDs.
4. **Evidence-gated source migration:** energy counters and any source change
   that could alter sign, reset, rollover, or interval deltas.

The next implementation task should start with a focused read-decoder patch
and tests, then metadata-only corrections, and only then a separately reviewed
energy migration. Instantaneous old/new values must be compared side by side;
cumulative energy needs the stronger delta/statistics checks above. If a new
register has materially different semantics, it must be exposed as a new
quantity rather than silently repurposing an existing Energy-dashboard sensor.

## Result

The canonical GII map is usable as the authoritative semantic reference, but
the current consumer is not yet fully reconciled. The highest-confidence
consumer work is the decoder correction group and I3110 separation. The
remaining unresolved scale and source-layout cases stay explicitly open in the
machine artifact. No runtime polling, broker behavior, or write behavior was
changed by HA-GII-1.
