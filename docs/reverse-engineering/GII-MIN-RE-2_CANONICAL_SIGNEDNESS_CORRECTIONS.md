# GII-MIN-RE-2 — Canonical MIN/TL-XH signedness corrections

## Disposition

```text
GII_MIN_SIGNEDNESS_CORRECTIONS_ACCEPTED_WITH_FOLLOW_UP
```

This bounded correction updates only the evidence-supported signedness of
MIN/TL-XH input registers I3101 and I3170. It does not change Home Assistant
consumer code, physical register identity, access policy, or any holding/write
mapping.

| Item | Value |
| --- | --- |
| Starting SHA | `dd0e3f9` (`Merge Shine-assisted MIN register completion evidence`) |
| Implementation SHA | `9823800` |
| Final/remote SHA | `9823800` (canonical implementation commit; branch publication tip is reported in the handoff) |
| Branch | `fix/gii-min-signedness-20260911` |

## Exact canonical changes

| Register | Before | After | Preserved |
| --- | --- | --- | --- |
| MIN/TL-XH input I3101 | signed; `register value`; `/1`; `%` | unsigned/non-negative; same encoding, scale and unit | family/table/address, length 1, `telemetry.output_power_percentage`, read-only access |
| MIN/TL-XH input I3170 | signed; `s16 / 10` | unsigned/non-negative; `u16 / 10` | family/table/address, length 1, `/10 A`, `battery.current`, BDC/storage-device measurement point, read-only access |

I3170 remains distinct from I3217. I3217 remains the signed directional BMS
current with `/100 A` scaling; it was not changed.

## Evidence basis

HA-GII-4B and the V4 history evidence establish:

- I3170 is Growatt V4 `bdc1_ibat`.
- 66 charging and 77 discharging records were classified.
- Charging values were `0 negative / 3 zero / 63 positive`.
- Discharging values were `0 negative / 2 zero / 75 positive`.
- This supports I3170 as a non-negative BDC/storage-device current magnitude;
  direction must be obtained from the operating state or a separate
  directional measurement such as I3217.
- I3101 is Growatt `real_op_percent`.
- Across 145 V4 history records, the observed range was `0..43%` and there
  were no negative values.

The retained semantic review and generated canonical outputs carry these
observations and mark both records resolved with high confidence.

## Validation

The normal generation and validation route completed successfully:

```text
python3 tools/build_register_graph.py
python3 tools/generate_consolidated_ref.py --validate-schema
python3 tools/build_resolved_register_reference.py
python3 tools/validate_resolved_register_reference.py
python3 tools/build_register_spec.py
python3 tools/validate_register_spec.py
PYTHONPATH=. pytest -q
```

Results:

- 4048 canonical records; holding/input counts remain 1805/2243.
- canonical validator errors: 0.
- resolved-reference validator: OK.
- test suite: 23 passed.
- resolved conflict-record count: 920 before and after.
- resolved conflict-item count: 968 before, 969 after; the additional item
  is the evidence note for the newly represented I3101 review and does not
  create a conflicted record.
- write-verified summary remains unchanged at 0 in this signedness task; no
  write-verified status was invented or promoted here.

The separate live Shine test did observe one Shine-originated write followed
by a confirming read-back: FC0x10 to holding H3040–H3041 while disabling TOU
period 2. That is existing runtime evidence for a future, separately bounded
write-evidence correction; this task did not alter the holding mappings or
canonical write-verification model. The running winter-mode capture and all
sniff/raw logs were left untouched.

## Home Assistant consumer audit

The accepted reconciled consumer was audited in `mapping_declared` mode using
consumer commit `64407145886ba0b89cc260ef3715f04d1023c5aa`.

| Metric | Before | After |
| --- | ---: | ---: |
| Mapping occurrences checked | 274 | 274 |
| Unique family/table/address mappings | 206 | 206 |
| Findings | 29 | 27 |
| Existing GII runtime findings | 24 | 22 |
| `SIGNEDNESS_MISMATCH` | 14 | 11 |
| `MATCH` | 236 | 239 |

The remaining signedness findings are the six unrelated physical records
I3021, I3041, I3043, I3045, I3178 and I3180 (11 repeated occurrences). They
remain visible and are deliberately deferred. The audit was not weakened to
hide them. Other unrelated length, unit, semantic, and live-validation
findings remain visible as well.

## Explicitly deferred

No changes were made to I39, I1014, I3032, I3036, I3191, I3194, I3195, I3217,
any holding/write register, BMS temperature interpretation, W/VA conflicts,
or Home Assistant consumer code. No runtime, inverter, broker, or production
configuration was changed, and no inverter write was issued by this task.
