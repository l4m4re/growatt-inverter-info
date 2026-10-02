# MIN 6000TL-XH TOU grid-charge observation (2026-09-19)

Status: recorded as controlled behavioural evidence. No consolidated register
semantic was changed.

## Observation

The staging Home Assistant Recorder captured a bounded experiment on the
retained MIN 6000TL-XH installation. The enabled second schedule slot decoded
to 19:28–19:58, Battery First (`H3040=0xB31C`, `H3041=0x133A`). The readback
showed `H3049=0` before the window. At `2026-09-19T17:29:41Z`, `H3049` and
the HA AC-charge entity read enabled and the current priority read Battery
First. The current-priority readback returned to Load First at
`17:59:47Z`; the AC-charge readback returned to disabled at `18:00:12Z`.

During the 30-minute active interval, battery charge power was 3,540–3,570 W
(median 3,551 W). Power to user was 4,165–4,263 W and the household-load
entity was 607–707 W while PV input was at most 2.6 W. Battery SOC rose from
46% to 63%, and the battery-charged-today counter rose from 4.1 to 5.8 kWh.
These values are consistent with the inverter charging the battery from the
grid during the Battery First window.

The complete readback values, representative samples, query provenance and
limitations are retained in
[`min-6000tl-xh-tou-grid-charge-20260919.json`](../../sources/evidence/min-6000tl-xh-tou-grid-charge-20260919.json).

## Review disposition

This is a device-and-installation-specific behaviour observation. It supports
using the existing TOU controls for a future attended charging policy, but it
does not by itself establish a universal meaning for `H3049`, prove a firmware
independence claim, or replace the existing register review. The consolidated
register model is therefore unchanged. The raw Recorder database and original
Modbus write frames remain local.

## Related schedule write/readback check

The same staging session also changed the end word of the disabled second TOU
period from `19:58` (`H3041=0x133A`) to `23:55` (`0x1737`) and restored it.
Both FC16 acknowledgements succeeded and the final readback matched the
original disabled period. The bounded request and response values are retained
in
[`min-6000tl-xh-tou-ha-write-readback-20260919.json`](../../sources/evidence/min-6000tl-xh-tou-ha-write-readback-20260919.json).
