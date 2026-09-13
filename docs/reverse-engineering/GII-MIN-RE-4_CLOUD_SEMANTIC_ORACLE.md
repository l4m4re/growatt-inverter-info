# GII-MIN-RE-4 — Growatt cloud semantic oracle and Shine response-injection map

Status: `GII_MIN_CLOUD_SEMANTIC_ORACLE_ACCEPTED_WITH_FOLLOW_UP`

This report records a bounded, read-only cloud inventory, a fresh native-block
capture, and controlled response-injection experiments for the live MIN
6000TL-XH. It deliberately does not change the canonical GII semantics. The
cloud results are useful for field inventory and semantic correlation. The
I3000 status mapping itself is not reopened here: that was the completed
GII-MIN-RE-3 smoke test. RE-4 records the completed remaining-field injection
attempts and the limits of the cloud oracle.

## Scope and safety

- Starting GII commit: `c1f5cf3586d6cba4c4314e418165029db1061261`
- Branch: `research/gii-min-re-4-cloud-semantic-oracle-20260913`
- Device: live MIN 6000TL-XH; identifiers are intentionally omitted here.
- Client library: `growatt-public-api 2026.5.19` in the existing Python 3.13
  environment.
- No inverter writes, configuration writes, HA changes, or production cache
  changes were made.
- The Shine was allowed to continue normal traffic, including any writes it
  might originate. No write frame was observed during the injection window.
- The temporary broker image was removed after the experiment. Production was
  restored to `growatt-rtu-broker:broker-4-tcp-writes-all-61dbb16`, with both
  TCP write paths enabled and no response override.

## Cloud API inventory

All calls below were read-only. Raw private responses were stored temporarily
under `/tmp/gii-min-re4-raw-20260913/`; no token, account identifier, or device
identifier is part of this repository.

| API operation | Result | Returned structure or finding |
|---|---|---|
| V4 device list | success (`0`) | `data`, `error_code`, `error_msg`; paged list metadata and device rows |
| V4 MIN/TLX details | success (`0`) | `data.devices`; model, status, firmware, battery/BDC/BMS, communication and configuration fields |
| V4 device info | success (`0`) | device type/model, nominal power, logger model, battery capability fields |
| V4 current energy | success (`0`) | `data.devices`; complete telemetry/status row |
| V4 plant power | error `18` | `READ_DEVICE_PARAM_FAIL` |
| V4 realtime power | success (`0`) | empty data payload |
| V4 one-day energy history | success (`0`) | `data.datas`, `start`, `have_next`; 110 rows in this run |
| V4 multi-device history | success (`0`) | keyed history response; the key was redacted from derived notes |
| V4 alarms | success (`0`) | alarm list/count envelope; no useful active alarm payload |
| V4 Wi-Fi strength | success (`0`) | empty data payload |
| V1 MIN details | package validation failure | Server response contained values not accepted by the library model, including `IGNORE`-style fields; not an authorization failure |
| V1 energy | success (`0`) | complete telemetry/status row, equivalent in field families to V4 energy |
| V1 energy history | error `10013` | request exceeded the API limit of 100 rows; no retry was needed for this bounded task |
| V1 settings | package validation failure | server data was returned but could not be represented by the library model |
| V1 native setting read | success (`0`) | empty data payload |
| V1 SOC | error `10002` | `storageNotExist` |

The V4 details response exposed communication/configuration fields such as
`baudrate`, `com_address`, `modbus_version`, `bms_communication_type`, and
`datalogger_sn`. Their presence is an API inventory result only; it is not
proof that a field is the external DDSU666 meter's serial configuration.

The V4 energy and history rows expose the following relevant semantic groups:

- inverter: `status`, `status_text`, `operating_mode`, `real_op_percent`;
- BDC: `bdc1_status`, `bdc1_mode`, `bdc1_ibat`, `bdc1_vbat`, charge/discharge
  power and totals, fault/warning fields, and `bdc_derate_reason`;
- BMS: `bms_status`, `bms_ibat`, `bms_vbat`, SOC/SOH, pack/error/warning and
  communication fields;
- system/status words: `warn_code`, `new_warn_code`, `fault_type`,
  `sys_fault_word` through `sys_fault_word7`, `warn_text`;
- grid/load/energy: `pac`, `p_system`, `pac_to_local_load`, grid/export
  totals, PV totals, charge/discharge totals, and daily/total energy fields;
- winter mode: `win_mode`, `win_request`, `win_on_grid_soc`,
  `win_off_grid_soc` and window timestamps.

The current V4 row was internally coherent: `status=1`/`Normal`,
`operating_mode=0`, BDC mode/status active, and BDC/BMS charge/discharge
fields present. The history contains both charging and discharging records,
including distinct BDC and BMS current conventions already documented by
HA-GII-4B and GII-MIN-RE-2.

The Shine/cloud reporting cadence is approximately one publication every five
minutes. A manipulated value must therefore remain stable for at least one
complete five-minute interval, and the API must then be queried after the
publication, before a cloud effect can be assessed. The returned history
timestamps also extend beyond the local UTC wall clock in this environment.
This is retained as an API/device-time observation. Together these facts mean
that a returned history row cannot be assumed to be caused by a live
experiment without a fresh, uniquely identifiable time window.

## Native Modbus and Shine capture

Before the experiment, complete vendor-native FC04 pages were read through the
broker at unit 1:

| Function | Start/count | Result |
|---|---:|---|
| FC04 | 3000/125 | success, 125 words |
| FC04 | 3125/125 | success, 125 words |
| FC04 | 3250/125 | success, 125 words |

The fresh sniff capture was taken from the broker event stream, not from the
large persistent broker logs:

`/tmp/gii-min-re4-sniff-20260913T090349Z.jsonl`

Its SHA-256 was
`1ed3f41e97a1945534ed67c2761ed72e3a94bee61d7d207a524cbae9ebd7ee6a`.
The existing analyzer reported successful native block traffic, no bad CRCs,
no drops, and FC20 as function byte `0x20` (decimal 32), not register 20.

The capture also confirms that the Shine uses the native 125-word pages and
that FC20 is a separate opaque namespace. The FC20 request observed was the
standard `01 20 00 00 00 64 ...` form; it must not be interpreted as an
ordinary FC03/FC04 register block.

## Controlled Shine-bound response injection

The existing broker framing and CRC code was extended in the temporary
experiment image with a repeatable `ADDRESS=VALUE` response override. It only
rewrote responses sent to the Shine after the normal virtual/cache/physical
path had produced a valid FC03/FC04 response. HA TCP clients, the shared cache,
FC20 traffic, and the physical inverter response were not modified.

The same broker framing and CRC code was used to test the remaining
candidate fields one at a time. Each override was held for at least 300 seconds
before the read-only V4 history query. The temporary image was replaced only
between candidate fields; no inverter write was issued by the experiment.

I3000 was intentionally not repeated: its `0..8` status smoke test is already
complete in GII-MIN-RE-3.

The complete remaining-field run was:

| Target | Injected word | Active interval | Valid rewrites | Cloud result |
|---|---:|---:|---:|---|
| I3165 | `0` | 09:32:26–09:37:21 UTC | 29 | no new history timestamp |
| I3110 | `0x1234` (`4660`) | 09:38:04–09:43:58 UTC | 69 | no new history timestamp |
| I3111 | `0x2345` (`9029`) | 09:53:09–09:58:08 UTC | 64 | no new history timestamp |
| I3211 | `1` | 09:58:50–10:03:50 UTC | 30 | no new history timestamp |
| I3166 | `0x0101` (`257`) | 10:04:34–10:09:35 UTC | 5 | no new history timestamp |
| I3212 | `1` | 10:10:15–10:15:14 UTC | 29 | no new history timestamp |

I3111 also had an earlier partial attempt (09:44:59–09:49:48 UTC, 40
rewrites); it was not counted as evidence and was repeated as the complete
cycle shown above.

For each completed cycle the API returned the same latest device timestamp,
`2026-09-13T00:02:13`, despite returning a few additional duplicate history
rows. This is not a fresh cloud publication and cannot identify any injected
field. The portal observation supplied during the run likewise showed a stale
inverter update time. Consequently none of these trials promotes a new
physical-to-cloud semantic mapping.

Transport details from the bounded broker logs:

- all override responses had valid recomputed CRCs;
- FC03/FC04 response rewriting remained Shine-bound; FC20 was untouched;
- no inverter write frame was generated by the experiment;
- transient physical retries/timeouts and serial reopen events occurred during
  some container replacements, so they are retained as transport observations,
  not attributed to any injected value;
- after the final cycle the known stable image
  `growatt-rtu-broker:broker-4-tcp-writes-all-61dbb16` was restored with both
  TCP write paths enabled, and the broker reported `shine_online`.

The earlier I3000 experiment remains recorded below for provenance, but is not
part of this remaining-field count.

The earlier I3000 trial, which is retained for provenance rather than counted
as remaining-field evidence, was:

- target: input register `I3000`;
- injected full word: `0x0002` (`2`);
- original observed values: `0x0000` and `0x0001`;
- response types: both FC03 and FC04;
- observed rewrite events: 51 in the first available temporary-container log;
- every rewritten response had a recomputed valid CRC;
- no Shine write frame was observed in the bounded capture;
- the Shine continued its normal FC03/FC04 native-page and FC20 polling.

A second local sniff capture was started for this run at
`/tmp/gii-min-re4-live-20260913T090936Z.jsonl` and has SHA-256
`bcfacb83a9e9bba40ad7c64aa6eb2c098dddf7d00c79bf9a08754e8796763905`.
The TCP sniff connection was interrupted when the broker container was
replaced, so it covers the beginning of the experiment only. The broker logs
covered the continuing response rewrites and showed intermittent physical
timeouts in the same period; these are transport observations, not evidence
that the injected status caused them.

The first I3000 trial lasted about 4 minutes 16 seconds, which is shorter than
the required five-minute publication interval. A second trial was started only
to correct that timing deficiency, but was stopped when it became clear that
I3000 was already complete in the prior GII-MIN-RE-3 smoke test. Its container
lifetime crossed five minutes, but no API query was coupled to a uniquely
identified publication from that run. Neither trial can therefore be used as
a fresh cloud correlation. The available post-trial V4 current/history reads
returned the same older cloud snapshot, including `status=1`/`Normal` at the
latest returned timestamp.

The technical result is limited to valid Shine-bound FC03/FC04 rewriting,
continued Shine polling, and no observed new cloud sample. The semantic result
for I3000 remains the complete GII-MIN-RE-3 mapping; this report does not
promote a second or conflicting status interpretation.

## Semantic oracle findings

The cloud API is a useful semantic oracle for field names and relationships,
but it is not yet a reliable response-injection oracle for this device because
the history/current endpoints returned a stale or device-time-offset snapshot
and the injection was not held through a complete five-minute upload.

The following correlations are supported at the cloud-field level and remain
consistent with the canonical GII evidence:

| Cloud field group | Interpretation supported by this run | Physical mapping state |
|---|---|---|
| `status`, `status_text` | inverter status enum/text pair | I3000 low-byte meanings are covered by GII-MIN-RE-3; no new cloud correlation here |
| `operating_mode` | separate inverter operating-mode field | not conflated with I3000 without a fresh paired sample |
| `bdc1_status`, `bdc1_mode`, `bdc_derate_reason` | BDC status/mode/derating namespace | consistent with I3165/I3166 family evidence; no new canonical change |
| `bdc1_ibat` | BDC/storage-side current magnitude | consistent with I3170 and HA-GII-4B |
| `bms_ibat` | directional BMS current | consistent with I3217 and HA-GII-4B |
| `bms_*` voltage/status/error fields | BMS namespace distinct from BDC | no new physical mapping promoted |
| `warn_code`, `fault_type`, `sys_fault_word*` | cloud status/fault namespaces | not equated to I3110/I3111 by this run |
| FC20 payload | proprietary telemetry/report namespace | kept separate from input-register semantics |

No canonical GII record was edited by RE-4. In particular, I3000, I3165,
I3110/I3111, I3211, I3170, I3217, or any status/fault/warning record was not
silently reinterpreted.

## Remaining mapping disposition

The remaining candidate cycles were completed technically, but none produced a
fresh cloud observation. Therefore the cycles establish only that these
registers can be rewritten in valid Shine-bound FC03/FC04 responses; they do
not establish the cloud field corresponding to any injected value. No canonical
GII or HA mapping change is justified by this run.

The next useful experiment requires a demonstrably fresh cloud observation
window (a portal/API timestamp that advances during the run) before another
injection is started. The five-minute hold rule and one-field-at-a-time design
should be retained. I3000 remains covered by GII-MIN-RE-3 and must not be
repeated. FC20 remains a separate opaque experiment namespace and must not be
inferred from ordinary I-register offsets.

The current result is therefore useful evidence and a reusable injection
mechanism, but not sufficient for canonical reconciliation or a new HA
mapping.
