# MIN 6000TL-XH TOU smoke tests (2026-09-20)

Status: recorded as controlled behavioural evidence. No consolidated register
semantic was changed.

## Scope

Two short, supervised hardware-in-the-loop tests were run against the retained
MIN 6000TL-XH through the DEV Growatt broker. The tests exercised the rate and
stop-SOC pairs used by the planner:

- Battery First, slot 4, 13:48–13:56 inverter local time: `H3047=30%`,
  `H3048=55%`.
- Grid First, slot 5, 14:08–14:16 inverter local time: `H3036=30%`,
  `H3037=52%`.

The complete bounded extract is in
[`min-6000tl-xh-tou-smoke-20260920.json`](../../sources/evidence/min-6000tl-xh-tou-smoke-20260920.json).

## Battery First trial

The complete desired schedule image was read back after the two FC10 writes.
The slot was enabled as Battery First and the battery charge rate and stop SOC
matched the request. The inverter charged at approximately 1.51–1.54 kW while
the SOC moved from 53% to 55%. At 55%, charge power fell to 0 W. This is a
positive bounded observation of the Battery First and `H3048` stop-SOC behavior.

PV production was substantial during the test. The result therefore does not
prove that the charge came from the grid; a no-PV night test remains needed for
that claim.

## Grid First trial

The two FC10 segments containing the schedule and the `H3036/H3037` values were
accepted and read back. The current-priority readback changed to Grid First at
the slot start. With the Peblar load raised by the user to approximately 6 kW,
the observed inverter load was approximately 6.3–8.0 kW and grid export stayed
at 0 W. The battery supplied approximately 1.57 kW while SOC was 53%. When SOC
reached the requested 52% stop value, discharge fell to approximately
0.12–0.13 kW and remained there. The current-priority readback returned to
Load First after the slot ended.

This confirms the reachable `H3036/H3037` stop-SOC behavior in a battery-to-load
scenario. It is not a pure grid-export test because the controlled load was
larger than PV production.

## Transport and planner findings

The dry-run image included unchanged `H3082` as a third logical segment. An
unchanged FC06 write to `H3082` was attempted during the Grid First trial and
timed out; no retry or cleanup write was made, and read-only verification still
returned `H3082=0`. The future executor must omit unchanged segments and must
not write `H3082` solely because it belongs to the logical image. The timeout is
retained as a transport observation and is not treated as a device semantic
failure.

No disable or reset write was issued after either test. The test slots remain
persistent so a later planner test can overwrite them without an extra flash
write.

## Separate decoder finding

During the Battery First test, Home Assistant recorded values around
`429496354–429496581 W` for the output-power entity while the inverter was
charging. The values correspond to unsigned decoding of negative signed 32-bit
raw words from the single I3023 register (two words: I3023–I3024); for example
`0xFFFFFA31` would be `-148.7 W` at a `0.1` scale. The current GII evidence
describes that 32-bit register as unsigned, so this is an unresolved live
conflict rather than an accepted correction. A follow-up read-only capture and
human review are required before changing the canonical specification or the HA
entity decoder.

## Review disposition

These tests support the existing TL-XH TOU control mapping for this installation
and provide a reachable stop-SOC smoke test. They do not establish universal
firmware behavior, atomicity of a full logical image, flash endurance, or a
grid-charge source claim under PV production. The consolidated register model
is unchanged.
