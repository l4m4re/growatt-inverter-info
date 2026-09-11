# GII-MIN-RE-1 — Shine-assisted MIN/TL-XH register completion

Disposition: **`GII_MIN_REGISTER_COMPLETION_ACCEPTED_WITH_FOLLOW_UP`**

This is a bounded, read-side and static reverse-engineering review for the
live MIN 6000TL-XH with ARK storage. It combines the canonical GII material,
retained live Modbus captures, Growatt V4 history, and the existing
ShineWiFi-X analysis. No inverter, broker, Home Assistant, cloud
configuration, or Shine firmware was changed.

## Baseline and evidence identity

| Item | Evidence |
| --- | --- |
| GII starting SHA | `f061c4aeeadeb06246aac6d4d0732da36fc6996d` (`main`) |
| GII branch | `research/gii-min-re-1-20260911` |
| HA-GII-4A integration evidence | `4a452777ea1b8a8d596534723a476ecc42810afd` |
| HA-GII-4B evidence | `64407145886ba0b89cc260ef3715f04d1023c5aa` |
| HA-GII-4B conclusion | BDC/BMS current sign domains resolved from 145 V4 records |
| Shine dump | `ShineWiFi-X-3.1.0.5.bin` |
| Shine dump SHA-256 | `b5e0644d03a33503812bd2770fde49762bd72e03dde3d92b5d68ad2a69afc173` |
| Shine dump size | 4 MiB |
| Architecture/load base | ESP8266/LX106; existing disassembly mapped at `0x40200000` |
| Static tool | Ghidra 12.1.3, Xtensa processor module, plus `xtensa-lx106-elf-objdump` 2.44 |
| Existing Ghidra projects | `/tmp/shine-ghidra-project-full` and `/tmp/shine-ghidra-fc20-project.lbXCvL` |
| Live proprietary capture | existing `HA-DEV-2D` capture, SHA-256 `56fa2ed1fcf859b8fb7e75793f71afbce9084b5bea6855161d85117c63253560` |

The older Ghidra project contains the previously recovered stock-image
analysis. The current 3.1.0.5 image was reviewed through the existing mapped
disassembly and prior exported findings; the binary was not overwritten or
re-imported into the existing project.

The live evidence was reused rather than issuing another cloud inventory or
an unnecessary live read. The relevant retained files are:

* `external/Homeassistant-Growatt-Local-Modbus/doc/HA-GII-4A_GROWATT_CLOUD_CROSS_VALIDATION.md`;
* `external/Homeassistant-Growatt-Local-Modbus/doc/HA-GII-4B_BATTERY_CURRENT_SIGN_DOMAIN.md`;
* `external/growatt-rtu-broker/docs/HA-DEV-2D_FC20_REVERSE_ENGINEERING.md`;
* `external/growatt-rtu-broker/docs/HA-DEV-3B_STOCK_SHINE_FIRMWARE_REVERSE_ENGINEERING.md`;
* `external/growatt-rtu-broker/docs/HA-DEV-3B2_SHINE_3_1_0_5_DIFF_AND_IDENTITY.md`.

## Results at a glance

The review materially narrows the implementation boundary, but it does not
justify a broad canonical rewrite:

* I3170 is a non-negative BDC-side current magnitude in both natural charge
  and discharge history; I3217 remains the signed BMS-side current. This
  confirms HA-GII-4B and leaves the existing GII signedness entry as a
  separate correction candidate, not a runtime change.
* I39 remains a physical layout/length conflict. The Shine image does not
  provide a version-matched, field-specific read path that proves one word
  versus I39/I40 or a wider block.
* I3191, I3194 and I3195 remain BMS temperature identities with unresolved
  scale and channel interpretation. Their raw values and cloud temperature
  fields cannot be joined one-to-one from the retained evidence.
* I3032 and I3036 retain phase-power semantics, but the supplied evidence does
  not distinguish active W from apparent VA for the MIN/TL-XH implementation.
* I1014 remains a legacy/base-map SOC field. Its semantic name is supported,
  but its current canonical unit (`lith/leadacid`) is not credible and its
  live applicability was not re-proven in this task.
* GROWATT_FC0x20 is a distinct proprietary command path. The live frame is
  structurally proven, but its 100-word payload is not proven to use the
  ordinary FC03/FC04 register address space or to be DDSU666 data.
* The stock code visibly contains one-second wait/retry building blocks and a
  bounded retry loop on the dynamic inverter read path. It does not contain
  enough evidence to attribute the observed slow or missing `0..124` page
  responses to a page-specific firmware timeout.

## Evidence matrix

| Register / area | Canonical/source material | Live Modbus / cloud | Shine firmware | Classification |
| --- | --- | --- | --- | --- |
| I39 | AC phase L1 current; canonical two-register `/10 A`, with conflicting one-word and alternate two-/four-register source claims | No retained live layout proof that separates I39, I40, or a wider decoded value | No direct I39-specific constructor, literal field xref, or conversion path isolated | **CONFLICTING_EVIDENCE** for layout; **SUPPORTED_WITH_NOTES** for quantity |
| I1014 | Legacy/base `StateofchargeCapacity`; canonical `/10` plus malformed `lith/leadacid` unit; I3171 is preferred on MIN/TL-XH | Current MIN evidence uses newer battery block; no direct current I1014 read in this task | No version-matched I1014 decoder or SOC conversion path isolated | **SUPPORTED_WITH_NOTES** |
| I3032 | AC phase L2 power / `Pac2H`; source variants say W, VA, and different word lengths | Aggregate cloud power does not identify this phase register or resolve W versus VA | No direct I3032 field path isolated | **SUPPORTED_WITH_NOTES** for phase-power identity; W/VA **UNRESOLVED** |
| I3036 | AC phase L3 power / `Pac3H`; same source conflict as I3032 | No independent phase-3 cloud field in retained V4 evidence | No direct I3036 field path isolated | **SUPPORTED_WITH_NOTES** for phase-power identity; W/VA **UNRESOLVED** |
| I3191 | BMS average temperature, vendor channel A; vendor omits scale | Repeated local raw value `0`; V4 exposes temperature fields but no defensible one-to-one mapping | No direct address/scaling assignment isolated | **UNRESOLVED** |
| I3194 | BMS maximum cell temperature, vendor channel B; vendor omits scale | Repeated local raw value `2`; cloud fields do not identify this source | No direct address/scaling assignment isolated | **UNRESOLVED** |
| I3195 | BMS average temperature, vendor channel C; vendor omits scale | Repeated local raw `13/14`; cloud fields do not identify this source | No direct address/scaling assignment isolated | **UNRESOLVED** |
| I3170 | Storage-device/BDC current; current canonical entry is signed `/10 A` | 66 charge and 77 discharge V4 records: BDC current was never negative; BDC and BMS values differ by operating state | No new signedness path; existing implementation correlation retained | **PROVEN** as observed non-negative BDC magnitude; canonical correction candidate |
| I3217 | BMS current, signed `/100 A`, alternate physical measurement point | Negative during 74 discharge records and positive during 57 charge records | No collapse with I3170 | **PROVEN** as directional BMS current in observed domain |
| I3101 | Existing GII signedness is true | `real_op_percent` was non-negative in all 145 V4 records, range `0..43%` | Not a Shine field-mapping proof | **STRONGLY_SUPPORTED** unsigned/non-negative metadata correction candidate |

### I39 layout boundary

The canonical source material consistently gives the semantic label “AC phase
L1 current”, but its physical representation is not consistent. The current
MIN/TL-XH record retains a two-register `/10 A` interpretation because that is
the curated source choice, while HA and another implementation expose a
one-word value. The Shine firmware's current image has generic profile and
block machinery, but no isolated read constructor or parser that can be tied
to I39/I40. An isolated numeric `39` in code would not be sufficient evidence
because it can also be an array offset or unrelated parameter.

Conclusion: do not change the HA read length or canonical I39 layout from this
task. The next useful observation is a passive capture in a state where L1
current varies independently, with the surrounding words from the complete
native page retained.

### I3191/I3194/I3195 temperature boundary

The source-level semantic names are useful and are retained, but the vendor
documentation omits the scale for exactly the fields that matter here. The
retained local values (`0`, `2`, and `13/14`) are compatible with unavailable,
low, or scaled temperature channels and therefore cannot distinguish `/1` from
`/10`. V4 fields such as `bms_temp1_bat` and `bdc1_temp1` are not a defensible
one-to-one mapping to these three physical registers. The firmware scan found
no address-specific conversion or upload field that would close this gap.

Conclusion: keep these as diagnostic records with unresolved scale/channel
metadata. Do not create or repurpose HA temperature entities from this result.

### I3032/I3036 W versus VA

The canonical MIN/TL-XH records currently say VA, while other source names and
the existing HA consumer presentation use power/W terminology. The V4 API
provides aggregate values, not a field that can be unambiguously associated
with phase 2 or phase 3. The Shine payload has electrical-looking values, but
its version-matched 3.1.0.5 field mapping is not isolated and no product of
voltage and current was proven to be the payload source.

Conclusion: preserve the source conflict explicitly. Do not normalize the
canonical unit or change HA metadata until a phase-unbalanced passive capture
or a version-matched decoder establishes whether the register is active power,
apparent power, or a vendor-labeled hybrid.

### I1014 metadata

Across the source corpus, I1014 is consistently named as SOC in the legacy/base
storage map. The `lith/leadacid` unit is a source/canonical metadata defect,
not a meaningful Home Assistant unit. The alternate source that says a
percentage and the preferred modern MIN/TL-XH I3171 mapping support treating
I1014 as a legacy battery-SOC concept, but no direct MIN I1014 read was issued
here and no firmware conversion path was isolated.

Conclusion: retain I1014 as a legacy SOC alternate, but schedule a narrow
canonical metadata correction to replace the malformed unit with a neutral
percentage representation only after the legacy register's scale is directly
verified. The modern runtime should continue to prefer I3171.

## HA-GII-4B signedness incorporation

HA-GII-4B found 66 naturally occurring charging records and 77 discharging
records in one V4 day. The relevant sign counts were:

| State | BDC `bdc1_ibat` | BMS `bms_ibat` |
| --- | --- | --- |
| Charge | `0 negative / 3 zero / 63 positive` | `0 negative / 9 zero / 57 positive` |
| Discharge | `0 negative / 2 zero / 75 positive` | `74 negative / 3 zero / 0 positive` |

This establishes the observed direction convention:

* I3170 / BDC is a non-negative current magnitude, scaled `/10 A` in the
  retained local mapping;
* I3217 / BMS carries direction, with negative discharge and positive charge,
  scaled `/100 A`.

The existing HA interpretation of I3170 as a positive battery-current value
is therefore correct in the observed domain. A later reviewed GII correction
should change I3170 from `signed: true` to an explicit unsigned or
non-negative-magnitude representation. I3101 has a separate correction
candidate because all 145 `real_op_percent` values were non-negative. Neither
change is applied in this evidence commit.

## GROWATT_FC0x20: proprietary address space and payload

The notation is deliberate: Growatt function byte `0x20` is hexadecimal 32.
It is not standard Modbus decimal function 20 (`0x14`, Read File Record).

The retained live capture contains seven exact Shine requests:

```text
01 20 00 00 00 64 81 e6
```

and seven CRC-valid responses of the form:

```text
01 20 c8 <200-byte payload> <CRC>
```

The payload is therefore 100 big-endian words indexed as `word[0]..word[99]`
within this proprietary response. It is not safe to call those words I0..I99
or to assign ordinary FC04 addresses to them.

Existing analysis identifies these bounded observations:

* word 47 is constant `500`, correlating with ordinary I3025 values around
  `5000` only after a different apparent scale; this is a strong correlation,
  not a canonical map;
* words 3, 9, 21, 27, 33, 39, 41, 43 and 45 contain changing or duplicated
  electrical-looking values, but no version-matched standard-register equality
  or independently varying meter signal proves their meaning;
* stable words 55–57 and zero/reserved regions are not evidence of a DDSU666
  payload;
* the existing 120-sample offline/online sample set confirms repeated
  GROWATT_FC0x20 structure and state variation, but only its frequency
  correlation reaches `STRONG_CORRELATION`.

The older stock-image static path is useful but must not be generalized to the
live firmware: a dispatcher routes opcode `0x20` to a report builder with an
`0xa0`-byte payload and an example 80-word request. The live 3.1.0.5 capture
uses 100 words. This is evidence for a version/profile-dependent proprietary
command, not proof of a universal range or address mapping.

The firmware and live capture also do not prove that GROWATT_FC0x20 is a
DDSU666 proxy. Meter attribution still requires a passive capture of the
actual meter bus or an independently identified meter transaction.

## Recovered timeout and retry architecture

The earlier timeout findings are retained and extended as follows.

### H43 discovery path

In the current mapped 3.1.0.5 disassembly, the constructor at `0x40244438`
builds an FC03 request for address 43 and count 1, computes CRC, validates
unit/function/address response bytes, and then classifies the returned type
against a profile table. The success and failure loops at `0x4024463c` and
`0x40244648` pass literal `0x3e8` (1000) to the wait/helper routine. This is
strong evidence of a one-second wait/retry building block, not proof of the
whole observed discovery cadence.

### H209 path

The constructor at `0x402447ac` builds FC03 address `0x00d1` (209), count 15,
and validates the response. The success path explicitly waits with literal
`30` at `0x40244821` before receiving/processing the response. The failure
path calls the same wait/helper family with a statically loaded `0xbb8`
argument at `0x40244780`; the current disassembly does not establish that
this value is a UART timeout in milliseconds, so it is not promoted as such.

### Dynamic H180/page path

At `0x40245b07`, the current image passes start `180` and count `199` to the
shared inverter-read helper at `0x40244970`. A failure increments a byte-sized
counter and branches while it is below 6 (`bgeui ... 6` at `0x40245b22`). This
is a concrete broad-block and bounded-retry finding. It does not prove that
the live Shine always transmits a 199-word request, nor that this helper is
the source of the live `0/125` request.

### Other timing/state evidence

The image contains separate inverter, WiFi/AP, cloud TCP, FOTA, local HTTP,
and flash-backlog state paths. The string `no %s found, reconnect after 1s`
belongs to reconnect handling, not proof of a Modbus response timeout. The
`IOT_ESP_Inverter_Task`, inverter-time diagnostics, register-address profile
strings, and CRC diagnostics support separation of these subsystems.

The retained live broker evidence shows native 3000/3125/3250 pages generally
returning in milliseconds, while a complete base `0..124` read once took about
1.9 seconds and other bounded base-page attempts timed out. The stock binary
proves one-second waits, retries, and profile/block reads, but no
page-specific timeout policy for `0..124`. The base-page anomaly therefore
remains an observed transport/device interaction, not a proven firmware bug.
Possible contributors include inverter scheduling, asynchronous Shine traffic,
serial buffering, and request timing; this task does not distinguish them.

For GROWATT_FC0x20, the older static path and live frame structure prove a
separate command/report path, but no version-matched timeout constant or
function-specific retry policy was isolated. The current broker should keep
the command opaque and preserve exact length/CRC and timeout evidence.

## Later passive investigations with highest information value

No active experiment is proposed or performed here. The following passive
observations would most efficiently reduce the remaining uncertainty:

1. Capture a phase-unbalanced interval and retain complete FC04 words around
   I39/I40, I3032/I3033, and I3036/I3037 while correlating voltage, current,
   active power, apparent power, and cloud timestamps.
2. Capture the complete I3187..I3201 BMS range through repeated temperature
   changes and compare it with the V4 BMS/BDC temperature fields. A changing
   raw I3191/I3194/I3195 value is required to distinguish `/1` from `/10`.
3. Read the legacy/base I1014 in a bounded read-only comparison with I3171,
   preserving raw words and decoded values; do not change the runtime source
   until continuity is established.
4. Synchronize GROWATT_FC0x20 requests, complete native pages, and (where
   physically possible) a receive-only DDSU666 bus observation. This is the
   only presently credible route to meter attribution.
5. Record the request-to-response delay and retry state for each complete
   native page separately. This can distinguish a base-page response issue
   from a general serial or broker failure without writes or Shine resets.

These are tracer/evidence tasks, not permission to inject frames, write the
inverter, or alter the live broker.

## Canonical and HA boundary

No canonical GII record and no HA consumer was changed by this task. In
particular, the following are follow-up candidates rather than applied fixes:

* I3170: unsigned/non-negative BDC magnitude `/10 A`;
* I3101: unsigned/non-negative output percentage;
* I1014: replace malformed unit metadata only after direct legacy-scale
  evidence;
* I39: resolve physical length/source layout;
* I3191/I3194/I3195: resolve scale and channel scope;
* I3032/I3036: resolve W versus VA from phase-correlated evidence.

The existing HA public sensor contract is not changed. No new entity is
created for an unresolved diagnostic field, and no existing source register is
silently repurposed.

## Final disposition

**`GII_MIN_REGISTER_COMPLETION_ACCEPTED_WITH_FOLLOW_UP`**

The task materially improves the MIN/TL-XH map: BDC/BMS signedness is
incorporated from natural charge/discharge history, the proprietary
GROWATT_FC0x20 address-space boundary is explicit, and the Shine timeout and
retry architecture is bounded with code locations and limits. I39,
I3191/I3194/I3195, the I3032/I3036 W-versus-VA distinction, and direct legacy
I1014 scale evidence still require passive, version-matched observation.

No HA-GII-5 work was started. No runtime, broker, inverter, cloud
configuration, or Shine firmware state was modified.
