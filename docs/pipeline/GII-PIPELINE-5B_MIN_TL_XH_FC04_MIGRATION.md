# GII-PIPELINE-5B — MIN/TL-XH FC04 declarative migration

## Disposition

`GII_PIPELINE_MIN_TLXH_FC04_MIGRATION_ACCEPTED_WITH_FOLLOW_UP`

This bounded migration creates an offline declarative shadow for FC04 input
registers `3000–3249` of the `MIN/TL-XH` family. The accepted canonical
specification was not regenerated or changed. The shadow is usable as the
next reviewed authority input, but 129 semantic parity items remain explicitly
unresolved and must not silently replace existing canonical semantics.

## Repaired lineage metadata

| Item | Value |
|---|---|
| Repair branch | `repair/gii-pipeline-5a-5d-lineage-20260913` |
| Accepted base | `8ceb8cd94f50235af4fc10b44ad8cbb355919518` (PIPELINE-4A) |
| Repaired 5A parent | `755986d03f74cc4fdebe30f7a91a4d6d384c73fc` |
| Original stage commit | `fee9a0ec1348937af853148d95b948e9a0540b24` |
| Replayed stage commit | `bfee1377750690d200c76c3454596312d0a7ffd5` |
| Repaired contract commit | `fade85974d658c7d487c44a48821263010f685b7` |
| Canonical SHA-256 | `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` |

Starting SHA: `755986d03f74cc4fdebe30f7a91a4d6d384c73fc`
PIPELINE-5A SHA: `755986d03f74cc4fdebe30f7a91a4d6d384c73fc`
Branch: `repair/gii-pipeline-5a-5d-lineage-20260913`
Canonical modified: `false`

## Scope and result

| Measure | Result |
|---|---:|
| Physical FC04 bus units | 250 (`I3000–I3249`) |
| Existing canonical records in scope | 250 |
| Existing canonical semantic records | 234 |
| Existing canonical semantic concepts | 184 |
| Declarative logical source decisions | 180 |
| Declarative physical decisions | 250 |
| Generic source claims | 447 |
| Physical parity | 250/250 |
| Exact source-name parity with canonical names | 121/250 |
| Explicitly unresolved semantic parity items | 129 |

The 250 addresses are not treated as 250 independent quantities. The
declarative logical decisions preserve multiword spans and continuation words;
reserved/unmapped holes remain physical records without an invented semantic
entity.

The generated artifacts are:

- `sources/claims/gii-pipeline-5b-fc04.json` — bounded generic source claims;
- `reconciliation/min_tl_xh_fc04_3000_3249.json` — physical and logical
  reconciliation decisions;
- `docs/pipeline/data/GII-PIPELINE-5B_FC04_SHADOW.json` — candidate/parity
  result;
- `sources/claims/schema.json` and `reconciliation/schema.json` — bounded
  validation schemas.

`tools/build_fc04_migration.py` is deterministic and has no network/API
dependency. `tools/validate_fc04_migration.py` checks the cohort boundary,
claim references, evidence separation, deterministic artifacts, physical
parity and public-safety constraints.

## Authority and evidence model

The migration uses the following queryable source types:

`VENDOR_DOCUMENT_CLAIM`, `EXTERNAL_IMPLEMENTATION_CLAIM`,
`RUNTIME_IMPLEMENTATION_CLAIM`, `LIVE_MODBUS_OBSERVATION`,
`STOCK_SHINE_OBSERVATION`, `SHINE_BOUND_INJECTION_OBSERVATION`,
`GROWATT_CLOUD_API_OBSERVATION`, and `HUMAN_REVIEW_CLAIM`.

This cohort contains 250 V1.24 vendor-row claims, 180 bounded reviewed
semantic-source claims, eight read-only live FC04 observations, six retained
Shine-bound injection observations and three attributable Growatt Cloud/API
observations. The vocabulary includes the broader project classes so future
stock-Shine and implementation claims can enter the same system without a new
evidence taxonomy.

The earlier sanitized RE-4 oracle was migrated into a local public-safe source
artifact before claim generation. No token, cookie, account/device identifier,
private endpoint or raw private cloud response is included.

Physical and semantic assertions are deliberately separate. For example, the
I3165 Shine-bound change is represented as a physical/cloud mapping claim
(grade P1 for the synchronized high-confidence cycle), while the V1.24
`BDCDeratingMode` codebook remains a separate vendor semantic claim (grade S2).
Likewise, a Cloud/API field observation does not automatically become a direct
Modbus-register assertion.

Retained oracle coverage includes:

| Register | Existing evidence carried into claims | Disposition |
|---|---|---|
| I3000 | V1.24 vendor row and read-only live FC04 observation | Existing status smoke-test semantics are not reopened |
| I3110 | Shine-bound injection plus Cloud/API `sys_fault_word3` observation | Physical cloud correlation retained; bit meanings unresolved |
| I3111 | Shine-bound injection plus provisional Cloud/API `sys_fault_word4` observation | Provisional only; numeric FFT diagnostic is not converted to a bit decoder |
| I3165 | Shine-bound injection plus Cloud/API `bdc_derate_reason`; V1.24 codebook | Runtime consistency and vendor semantic evidence retained |
| I3166 | Shine-bound injection attempt; V1.24 packed mode/status definition | Non-attributable cloud result; vendor packed definition remains authoritative |
| I3211 | Shine-bound injection attempt; V1.24 request-bit definition | Non-attributable cloud result; vendor bits remain authoritative |
| I3212 | Shine-bound injection attempt; V1.24 BMS enum | Non-attributable cloud result; vendor enum remains authoritative |

Evidence grades remain lossless in the claim layer:

- `P1`: controlled physical mapping;
- `P2`: strong passive/live physical correlation;
- `S1`: Growatt semantic/API observation;
- `S2`: vendor semantic interpretation;
- `C`: candidate/correlation only;
- `X`: contradicted.

## Growatt API inventory reused

No new API or live manipulation was performed for PIPELINE-5B. Existing
sanitized RE-4 evidence was sufficient and was used first, as required. The
available V4 read-side inventory exposes these relevant groups:

- inverter: `status`, `status_text`, `operating_mode`, `real_op_percent`;
- BDC: `bdc1_status`, `bdc1_mode`, `bdc1_ibat`, `bdc1_vbat`, charge/discharge
  power and totals, fault/warning fields, `bdc_derate_reason`;
- BMS: `bms_status`, `bms_ibat`, `bms_vbat`, SOC/SOH and error/warning fields;
- status words: `warn_code`, `new_warn_code`, `fault_type`,
  `sys_fault_word` through `sys_fault_word7`, `warn_text`;
- grid/load/energy: `pac`, `p_system`, `pac_to_local_load`, grid/export and
  PV energy fields;
- winter mode: `win_mode`, `win_request`, `win_on_grid_soc`,
  `win_off_grid_soc` and window timestamps.

The retained API evidence records the V4 device/detail/current/history
operations and field names but intentionally omits private identifiers and
credentials. It does not make Cloud/API values automatic wire truth. FC20 is
not part of this cohort and remains a separate proprietary namespace.

## Canonical parity and authority reduction

The candidate was compared with the current canonical output without using
that output as claim support. Physical `(table,address)` identity and one-word
bus shape match all 250 records. 121 source names match the current canonical
normalized names exactly and are classified as representation-only parity.
The remaining 129 semantic differences are classified `UNRESOLVED`; no
semantic correction was silently promoted.

The repaired PIPELINE-5A inventory reports 49,867 canonical property cells,
49,632 legacy-authoritative cells (99.53%) and 41 legacy-exclusive cells. The
new shadow explicitly declares 2,935
source-backed property cells across physical identity/layout, access,
applicability, aliases, provenance, read-only write semantics and available
logical source mappings. On the same projected cohort basis, legacy-dependent
cells reduce from 3,166 to a projected 231. These are shadow metrics: because
the global generator cutover is intentionally deferred, the current
repository-wide canonical inventory remains 49,632 legacy/compatibility
property cells until a later reviewed cutover.

The remaining follow-up is concrete: resolve the 129 semantic parity items,
especially the stable canonical semantic-key relationship for source entries
whose human labels differ, before using this cohort as a generator input.
Missing enum/bitfield meanings, reserved words and cloud-derived/aggregate
fields remain unresolved rather than being guessed.

## Safety and reproducibility

- No inverter writes or configuration writes were issued.
- No broker, Home Assistant, runtime or canonical generator behavior changed.
- No active response perturbation was started; the existing five-minute
  Shine/cloud timing evidence was reused.
- The full claim/reconciliation/shadow build and validation run offline.
- Canonical validator errors remain zero; existing compatibility/resolved
  validators pass; the full test suite passes.

Validation commands:

```text
python3 tools/build_fc04_migration.py --check
python3 tools/validate_fc04_migration.py
python3 tools/validate_resolved_register_reference.py
python3 tools/validate_register_spec.py
python3 tools/validate_authority_coverage.py
python3 -m pytest -q
```

Final disposition: `GII_PIPELINE_MIN_TLXH_FC04_MIGRATION_ACCEPTED_WITH_FOLLOW_UP`
