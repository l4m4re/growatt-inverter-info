# MIN 6000TL-XH HA Recorder outlier audit (2026-09-20)

This audit scans the local staging Recorder for physically implausible Growatt
states. It retains a compact result only; the Recorder database is not
redistributed.

## Yesterday's 19:45 outlier

The power-flow value was not one isolated sample. `sensor.growatt_output_power`
stored 173 values between **19:29:06 and 19:59:21 Europe/Amsterdam** in the
range `429,493,102–429,496,435 W` (about 429.5 MW). Around exactly 19:45 the
stored value was approximately `429,493,138 W`.

The same interval had:

- battery charge power: `0–3,570 W`, approximately `3.55 kW` during the active charge;
- power to user: `0–4,263 W`;
- household load: `416–707 W`;
- PV input 1: `0–2.9 W`;
- BMS current: `-2.7–16.5 A`;
- SOC: `46–63%`.

Reversing the unsigned 32-bit wrap at the 0.1 W scale gives approximately
`-3.63 to -0.29 kW`, which matches the battery charging interval. The 429 MW
value is therefore a decoder artifact, not physical production.

## Other findings

`sensor.growatt_output_power` contains 347 values above 100 MW in five episodes:

| Local interval | Samples | Inferred signed range |
| --- | ---: | ---: |
| 13 Sep 20:32–21:32 | 56 | −0.41…−0.40 kW |
| 14 Sep 01:38–02:43 | 60 | −0.41…−0.40 kW |
| 14 Sep 06:50–07:47 | 53 | −0.41…−0.40 kW |
| 19 Sep 19:29–19:59 | 173 | −3.63…−0.29 kW |
| 20 Sep 13:53–13:54 | 5 | −0.38…−0.15 kW |

The percentage entity has 42 values above 100% in 22 episodes. Yesterday it
recorded 65,476–65,532% and during today's smoke test 65,530–65,534%.
These episodes line up with the output-power wrap and are not real percentages.

The BMS-current entity has 3,047 historical values between 637.06 and
655.16 A, from 27 August through 12 September local time. Interpreting those
as signed 16-bit values at 0.01 A gives approximately −18.3 to −0.2 A, which
is physically plausible. No such BMS-current outlier was present yesterday;
current values are already in the signed range.

The structured counts, intervals and limitations are retained in
[`min-6000tl-xh-recorder-outlier-audit-20260920.json`](../../sources/evidence/min-6000tl-xh-recorder-outlier-audit-20260920.json).

## Disposition

This is evidence of historical decoder artifacts. It does not rewrite Recorder
history or change the canonical GII specification. A raw Modbus capture while
charging and discharging is still required before accepting signedness changes
for the I3023 32-bit output-power register or the I3101 percentage register.
