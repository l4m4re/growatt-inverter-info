# GII-2A — MIN/TL-XH canonical metadata consistency

Final disposition: `GII_MIN_TL_XH_METADATA_CONSISTENCY_ACCEPTED`

Baseline: GII-2 commit `c8fa68397d4c29bbbf68bb4a24bad71c060fc628`

Branch: `research/gii-2-min-tl-xh-semantic-cleanup-20260911`

## Scope and method

This was a bounded consistency sweep of the generated canonical
`MIN/TL-XH` projection. It did not access or modify Home Assistant, the
broker, production state, the inverter, or any write path.

The new `tools/validate_min_tlxh_metadata.py` checker reads
`spec/growatt-register-spec.json` and covers the live-relevant ranges:

- holding `3000–3124`;
- input `3000–3374`.

It checks semantic/unit compatibility, packed and bitfield units, range/enum
text accidentally stored as units, duplicate physical identities, physical
word lengths, logical-field membership and logical-field length. Holding/input
address overlaps are explicitly reported as informational only, because the
same numeric address in different Modbus tables is valid when the physical
identity remains distinct.

The checker accepts source scale notation such as `0.1V` as a V-compatible
unit for this bounded audit. It does not rewrite unrelated legacy metadata
outside the requested scope.

## Corrected inconsistencies

All corrections are recorded in the existing
`sources/evidence/min-6000tl-xh-semantic-review.json` overlay. The historical
source claims remain in provenance; the canonical projection selects the
evidence-supported metadata.

| Physical field | Old canonical metadata | Contamination/source | Corrected canonical metadata | Confidence before → after | Disposition |
|---|---|---|---|---|---|
| `I3021` | Output reactive power; unit `POWER_REACTIVE`; generic register value | OpenInverter symbolic unit collided with the curated/implementation `var` field | signed `s32 / 10`, `0.1 var`; retained as high word of the logical reactive-power field | medium → high | `WRONG_UNIT` |
| `I3071/I3072` | Grid export power; `kWh`; logical power field | Vendor `Etogrid_todayH/L`, Grott, curated and OpenInverter evidence identify daily energy | Grid export energy today; unsigned `u32 / 10`, `kWh`; logical length 2 | medium → high | `MISLABELED` |
| `I3073/I3074` | Grid export power; `kWh`; logical power field | Vendor `Etogrid_totalH/L`, Grott, curated and OpenInverter evidence identify lifetime energy | Grid export energy total; unsigned `u32 / 10`, `kWh`; logical length 2 | medium → high | `MISLABELED` |
| `I3104` | Standby flags with bit-description sentence in `unit`; signed/unknown | Vendor bit descriptions were merged into the unit column | unsigned vendor-defined bitfield; unit empty; existing placeholder bitfield retained | high → high | `WRONG_UNIT` |
| `I3172` | VBUS1 voltage; unit `A` | OpenInverter snapshot says `CURRENT`, conflicting with vendor/curated VBUS voltage | unsigned `u16 / 10`, `0.1 V` | medium → high | `WRONG_UNIT` |
| `I3173` | VBUS2 voltage; unit `A` | Same OpenInverter `CURRENT` contamination | unsigned `u16 / 10`, `0.1 V` | medium → high | `WRONG_UNIT` |
| `I3210` | Battery insulation status with enum text in `unit` | Vendor enum text was placed in the unit field | unsigned enum `0=not detected, 1=detection completed`; unit empty | medium → high | `WRONG_UNIT` |
| `I3212` | BMS status with enum value list in `unit` | Vendor enum text was placed in the unit field | existing decoded `u16 enum`; unit empty | medium → high | `WRONG_UNIT` |
| `I3232` | Battery load voltage; range `[0,650.00]` in `unit`; signed/unknown | Vendor range/value column was merged as unit; curated datatype supplies voltage | unsigned `u16 / 100`, `0.01 V`; range text is not a unit | high → high | `WRONG_UNIT` |

The `I3071–I3074` correction is included because the old canonical name said
power while the unit and independent source evidence said energy. This is an
unambiguous source collision, not an attempt to infer a new undocumented
meaning.

## GII-2 length and logical-field regression checks

The GII-2 invariant remains intact:

```text
physical register word: length_words = 1
logical combined field: length_words = number of physical words
```

The regression suite checks `I3047/I3048`, `I3081/I3082`, warning words
`I110/I111` and `I3110/I3111`, multiword battery power fields, and energy
counters. Logical high/low fields now expose an explicit combined
`length_words` value while retaining physical component identity and word
order.

The holding/input overlaps at the same numeric addresses remain separate;
`H3081` is UPS/EPS frequency selection while `I3081/I3082` remain PV4 energy.

## Preserved GII-2 decisions

No confidence was strengthened merely because metadata was cleaned. In
particular, the following remain bounded or unresolved as appropriate:

- `I3170` remains distinct from validated BMS current `I3217` and its sign is
  not live-validated;
- `I3217` remains signed `/100 A`;
- `I3230/I3231` remain `/1000 V`;
- `I3191/I3194/I3195` retain unresolved scale/channel limitations;
- `I3200/I3201` retain unresolved numeric capacity scale/behavior;
- BMS warning/fault codebooks are not invented;
- the consumer-side `I3110` length finding is not changed in HA.

## Validation results

The complete generation chain was run twice:

```text
build_register_graph.py
generate_consolidated_ref.py --validate-schema
build_resolved_register_reference.py
validate_resolved_register_reference.py
build_register_spec.py
validate_register_spec.py
build_min_tlxh_audit_matrix.py
validate_min_tlxh_metadata.py
```

Both runs produced the same generated outputs. The final validator results
are:

```text
physical records: 4048
holding records: 1805
input records: 2243
conflicted records: 0
live-read records: 60
write-verified records: 0
metadata checker errors: 0
metadata checker warnings: 0
informational holding/input overlaps: 125
```

The full test suite passes (`21 passed`), `compileall` passes, and
`git diff --check` passes. The earlier GII-2 runtime audit remains a separate
consumer audit; this task does not modify its HA findings.

Coverage changes relative to the GII-2 baseline are limited to the explicit
daily/total grid-export energy semantic keys and the logical-length metadata:

| Metric | GII-2 baseline | GII-2A |
|---|---:|---:|
| physical records | 4048 | 4048 |
| holding/input | 1805 / 2243 | 1805 / 2243 |
| semantic concepts | 976 | 978 |
| reconciled records | 320 | 320 |
| logical fields | 550 | 550 |
| runtime audit findings | 22 unique / 23 occurrences | 24 unique / 27 occurrences |

The runtime audit count increases because the corrected energy identities and
metadata expose additional concrete consumer mismatches rather than hiding
them. No physical records were lost and no HA consumer mapping was changed.

## Merge recommendation

The canonical MIN/TL-XH metadata is internally consistent within the bounded
live-relevant scope, the known unit and length collisions are corrected, and
the generated pipeline is reproducible. The GII-2 branch is ready for review
and merge to `main`. The remaining HA runtime findings and unresolved BMS
semantics must still be handled in a separate consumer/evidence task.
