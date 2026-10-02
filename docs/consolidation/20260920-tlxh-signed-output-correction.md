# MIN 6000TL-XH signed output correction (2026-09-20)

The local HA Recorder showed that the bidirectional MIN 6000TL-XH uses signed
Modbus values while the inverter is charging from the grid:

- I3023–I3024 is one signed 32-bit AC output-power word at 0.1 W resolution.
- I3101 is a signed 16-bit real output percentage.

The previous unsigned decoder turned negative values into implausible values
near 429.5 MW and 65,500%. On 19 September 2026 from 19:29 to 19:59 local
time, stored output power was 429,493,102–429,496,435 W. Signed int32 decoding
produces −3.63…−0.29 kW and matches 0–3.57 kW of battery charge power. The
same interval stored I3101 as 65,476–65,532%; signed int16 decoding produces
−60…−4%, matching the negative output-power direction.

The public Tigo/Growatt history is positive-only, so it cannot disprove the
local signed behavior. This correction is accepted for the bidirectional
MIN 6000TL-XH mapping and is retained with installation-specific scope. It
does not rewrite existing Recorder rows; new reads must use the signed types.

Evidence and generated products updated together:

- `sources/evidence/min-6000tl-xh-recorder-outlier-audit-20260920.json`
- `sources/evidence/min-6000tl-xh-semantic-review.json`
- `sources/consolidated/register-blocks.json`
- `sources/curated/growatt-register-data-types.json`
- `sources/curated/growatt-registers-best-guess.json`
- `spec/growatt-register-spec.json`
