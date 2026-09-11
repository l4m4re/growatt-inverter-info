# GII-MIN-RE-2A — MIN/TL-XH power signedness reconciliation

## Disposition

`GII_MIN_POWER_SIGNEDNESS_RECONCILED_WITH_FOLLOW_UP`

This was a bounded evidence and consumer-snapshot reconciliation. No
canonical register interpretation was changed. The six signedness findings
were caused by a lossy Home Assistant snapshot, not by a change in the GII
canonical map. I3178 and I3180 remain an explicit evidence follow-up because
the independent OpenInverter implementation uses an unsigned size marker for
those two fields, while the Home Assistant implementation and other retained
evidence use signed 32-bit decoding.

## Lineage

| Item | Revision |
| --- | --- |
| Starting GII revision | `ad978fef131e2def8a4086ffe8f54d68e064eff9` |
| HA-GII-2 canonical comparison point | `4296c596091bc118c953c69c39b8d625107fb083` |
| HA decoder correction | `4fbb609c9ce576320edfd5be2c45e76a5116c659` |
| Accepted HA-GII-4B evidence tip | `64407145886ba0b89cc260ef3715f04d1023c5aa` |
| Current HA consumer snapshot source | `custom_components.growatt_local.API` |

The six GII records had the same normalized interpretation at the HA-GII-2
comparison point and at the starting revision: `s32 / 10`, signed, with the
same table/address identity. GII-MIN-RE-2 changed I3101 and I3170 only; it did
not change any of these six power records. No canonical register record or HA
runtime code was changed in this task.

## Register-by-register result

The table describes the two-word logical field represented by each physical
high-word record. “HA” is the effective decoder in the accepted consumer.

| Register | Quantity | Old/current GII | HA | Strongest evidence | Disposition |
| --- | --- | --- | --- | --- | --- |
| I3021 | output reactive power | `s32 / 10`, signed, var | signed | OpenInverter `SIZE_32BIT_S`; curated `s32_reactive_power_decivar`; vendor scale `0.1 var`; semantic review explicitly records signed reactive power | `CURRENT_MATCH_SUPPORTED` |
| I3041 | grid import / power to user | `s32 / 10`, signed, W | signed | OpenInverter `SIZE_32BIT_S`; vendor `PtousertotalH`/`0.1 W`; curated map labels the runtime quantity | `CURRENT_MATCH_SUPPORTED` |
| I3043 | grid export power | `s32 / 10`, signed, W | signed | OpenInverter `SIZE_32BIT_S`; vendor `PtogridtotalH`/`0.1 W`; curated map labels the runtime quantity | `CURRENT_MATCH_SUPPORTED` |
| I3045 | house load power | `s32 / 10`, signed, W | signed | OpenInverter `SIZE_32BIT_S`; vendor `PtoloadtotalH`/`0.1 W`; curated map labels the runtime quantity | `CURRENT_MATCH_SUPPORTED` |
| I3178 | BDC battery discharge power | `s32 / 10`, signed, W | signed | HA code and curated datatype use signed 32-bit; vendor/Grott omit sign; OpenInverter uses `SIZE_32BIT` (unsigned default) | `INSUFFICIENT_EVIDENCE` |
| I3180 | BDC battery charge power | `s32 / 10`, signed, W | signed | HA code and curated datatype use signed 32-bit; vendor/Grott omit sign; OpenInverter uses `SIZE_32BIT` (unsigned default) | `INSUFFICIENT_EVIDENCE` |

For I3021, the negative-value domain is part of the semantic definition:
positive is inductive reactive power and negative is capacitive reactive
power. For I3041/I3043/I3045, the runtime quantities are normally exposed as
non-negative magnitudes or separate import/export/load quantities. That
semantic domain does not prove an unsigned wire encoding; the independent
OpenInverter source explicitly selects signed 32-bit decoding for all three.

For I3178/I3180, the live MIN samples contain only positive values. Such
samples are compatible with both signed and unsigned 32-bit decoding. No
negative value, boundary value, or independently decoded cloud field in the
retained evidence establishes the wire sign bit for these two BDC power
fields. No GII correction is justified by this run.

## Why the audit moved from 3 to 11

The numerical change is fully reproducible:

| Audit input | Signedness mismatches | Explanation |
| --- | ---: | --- |
| HA-GII-2 corrected effective mapping | 3 | The six power mappings were already modeled as signed; the remaining findings were I3101 once and I3170 twice. |
| Current GII + original runtime snapshot | 11 | The snapshot omitted `signed` for the six mappings in 11 occurrences: I3021 once, and I3041/I3043/I3045/I3178/I3180 twice each. `mapping_declared` therefore defaulted each to unsigned. |
| Current GII + corrected runtime projection | 0 | The 11 accepted HA signed decoder declarations are represented explicitly; I3101 and I3170 were already corrected by GII-MIN-RE-2. |

The historical three-result audit was reproduced using the HA-GII-2 GII
specification and a temporary corrected six-field snapshot projection. The
current audit was then run against the current GII spec before and after the
same temporary projection. This is metadata-loss repair in the audit input,
not a weakening of the audit and not a Home Assistant code change. The
projection was not committed because applying a shared snapshot correction to
the generator would propagate the claim into unrelated families.

After the temporary snapshot correction, the current `mapping_declared` audit remains
fully populated and reports:

```text
mapping_occurrences_checked: 274
unique_family_table_address_mappings: 206
SIGNEDNESS_MISMATCH: 0
LENGTH_MISMATCH: 3
NEEDS_LIVE_VALIDATION: 6
SEMANTIC_MISMATCH: 11
UNIT_MISMATCH: 5
```

The unrelated findings remain visible. The change in `UNIT_MISMATCH` from 4
to 5 is an existing classification detail of the current consumer audit,
not a power signedness correction; it is retained for review rather than
hidden.

## Runtime and source evidence reviewed

- HA-GII-2 records six two-word TL-XH mappings as explicitly `signed=True`.
- The accepted HA decoder correction uses signed two-word decoding for these
  mappings; no HA source code was changed here.
- `sources/vendor/growatt-v1.24-tables.json` supplies the relevant variable
  names and `0.1` W/var scale, but does not independently settle sign for the
  five active-power fields.
- `sources/curated/growatt-registers-best-guess.json` and
  `sources/curated/growatt-register-data-types.json` provide the semantic
  quantity mapping. The curated datatype catalogue is unsigned for I3041,
  I3043 and I3045, and signed for I3178/I3180; this is recorded as source
  evidence, not silently treated as decisive over the independent runtime.
- `sources/external/openinverter-gateway-registers.snapshot.json` and the
  retained OpenInverter source distinguish `SIZE_32BIT_S` from `SIZE_32BIT`.
  The implementation's decoder casts the former through `int32_t` and the
  latter through the unsigned default path.
- Grott supplies two-word layout information but no sign declaration for
  these fields.
- Existing live capture samples include positive values such as I3041
  `2484.8 W`, I3043 `561.0 W`, and I3178 `2428.0 W`; they cannot distinguish
  signed from unsigned representation.
- Existing broker sniff logs and the live winter-settings capture were not
  edited, truncated, deleted, or newly interrogated as part of this bounded
  metadata reconciliation. No new live request, write, or forced operating
  condition was used.

## Explicit exclusions and follow-up

This task did not change or reclassify I3101, I3170, I3217, I39, I1014,
I3032, I3036, I3191, I3194, I3195, any holding/write register, or H3040/H3041
write status. It did not normalize W/VA conflicts, resolve BMS temperature
scales, modify HA consumer code, or invent write verification.

The targeted follow-up for I3178/I3180 is a naturally occurring or otherwise
independently captured operating point that can exercise a discriminating
signed value, combined with an authoritative decoder/format confirmation.
Until then, retain signed HA/GII behavior and keep the uncertainty explicit;
changing these records to unsigned based only on positive samples would be
unsupported.

## Validation

The checked-in snapshot is unchanged. The temporary audit projection contained
exactly 11 `signed: true` declarations for the six target occurrences. The
canonical generator and validators were run against the unmodified checked-in
corpus after this comparison; the normal GII tests passed. No unrelated
generated-file change is included in this branch.
