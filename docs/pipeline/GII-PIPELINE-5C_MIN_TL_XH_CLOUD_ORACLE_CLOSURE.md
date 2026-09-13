# GII-PIPELINE-5C — MIN/TL-XH FC04 Cloud/Shine semantic closure

## Disposition

`GII_PIPELINE_FC04_SEMANTIC_CLOSURE_ACCEPTED_WITH_FOLLOW_UP`

5C classifies every one of the 129 5B parity-unresolved FC04 targets. Existing
Cloud/Shine evidence was exhausted first. Three targets are closed by the
already retained oracle evidence; the remainder are explicitly bounded as
counters, possible aggregates, source-research items or insufficient evidence.
No new live experiment was necessary or started. Canonical output remains
frozen.

## Repaired lineage metadata

| Item | Value |
|---|---|
| Repair branch | `repair/gii-pipeline-5a-5d-lineage-20260913` |
| Accepted base | `8ceb8cd94f50235af4fc10b44ad8cbb355919518` (PIPELINE-4A) |
| Repaired 5B parent | `fade85974d658c7d487c44a48821263010f685b7` |
| Original stage commit | `4eb8b10364751e4d29243481501c4c72b6def69a` |
| Replayed stage commit | `969431af1a117b5423eef821eb2bd3b500e32f55` |
| Repaired contract commit | `6f664fff6b1523bf1a485b420dc8d4d3237eb1e0` |
| Canonical SHA-256 | `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` |

Starting SHA: `fade85974d658c7d487c44a48821263010f685b7`
Branch: `repair/gii-pipeline-5a-5d-lineage-20260913`
Canonical modified: `false`

Machine-readable outputs:

- `docs/pipeline/data/GII-PIPELINE-5C_FC04_CLOSURE.json`;
- `reconciliation/min_tl_xh_fc04_closure_20260913.json`;
- `tools/build_fc04_closure.py`;
- `tools/validate_fc04_closure.py`.

## Before/after classification

The original 5B unresolved set is exactly 129 targets. The direct semantic
closure count decreases from 129 to 68 items requiring further source or
semantic work. A further 58 items are not called resolved, but are now bounded
as safe non-probe classes: 54 counters/history quantities and four possible
derived or aggregate quantities. This distinction avoids presenting “do not
inject” as if it were semantic proof.

| Classification | Count | Meaning |
|---|---:|---|
| `EXISTING_EVIDENCE_SUFFICIENT` | 3 | I3110, I3111 and I3166 are covered by retained Cloud/Shine oracle evidence |
| `COUNTER_AVOID_ACTIVE_INJECTION` | 54 | Energy/runtime/cumulative-like fields; use passive correlation or sources |
| `DERIVED_OR_AGGREGATE` | 4 | Cloud value may be calculated or aggregated; no one-register claim assumed |
| `SOURCE_RESEARCH_CANDIDATE` | 17 | Incomplete source/layout evidence; source research has priority |
| `INSUFFICIENT_EVIDENCE` | 51 | Physical/source mapping exists, but semantic closure is not demonstrated |
| **Total** | **129** | Every 5B unresolved target has one classification |

All 129 target records include independent dimensions for physical mapping,
scale, signedness, unit, numeric interpretation, semantic interpretation,
enum information and applicability. This is not collapsed into one confidence
value. Current dimension summary:

| Dimension | Resolved/source-bounded | Unknown or unresolved |
|---|---:|---:|
| Physical | 108 resolved, 4 candidate | 17 source-only |
| Scale | 112 source-declared | 17 unknown |
| Signedness | 10 source-declared | 119 unknown/not established |
| Unit | 107 source-declared | 22 not applicable/unknown |
| Semantic | 3 oracle-bounded, 54 counter-bounded, 4 aggregate candidates | 51 unresolved, 17 unknown |
| Enum | 5 source-declared | 124 not applicable/unknown |
| Applicability | 112 family-scoped | 17 unknown |

The full address-by-address inventory and rationale is in the JSON artifact;
the reconciliation file contains one claim-linked decision for each target.

## Evidence reused before experimentation

No new API query, response injection or inverter interaction was performed in
5C. The following retained evidence was sufficient for this bounded closure:

- V1.24 vendor input-table claims;
- curated reviewed source mappings;
- bounded live FC04 observations;
- the sanitized RE-4 Cloud/API field inventory;
- the six existing Shine-bound oracle cycles carried into 5B;
- prior negative/non-attributable results for I3166, I3211 and I3212.

The inherited active cycles were already isolated to the Shine-bound response
copy. They changed neither the inverter response sent to local consumers nor
the local ground-truth cache, recomputed CRCs, and produced no intentional
inverter write. 5C adds no artificial values and injects no counters,
identity, SOC limits or configuration.

Within the 129-item set, the retained causal/Cloud evidence closes:

| Register | Evidence result | Closure status |
|---|---|---|
| I3110 | distinctive Shine-bound marker reached Cloud/API `sys_fault_word3` | physical cloud correlation retained; warning-bit meanings remain unresolved |
| I3111 | marker reached provisional Cloud/API `sys_fault_word4` | provisional mapping; vendor FFT diagnostic identity retained, no bit decoder invented |
| I3166 | packed `257` experiment was not attributable | vendor upper-byte mode/lower-byte status definition remains authoritative; cloud mapping not promoted |

I3165, I3211 and I3212 already had source-name parity in the 5B shadow and
therefore are not part of the 129-target remainder. Their existing vendor and
Cloud/Shine evidence remains claim-backed in the 5B claim set.

The I3110/I3111/I3166 results are represented with separate physical mapping
and semantic claims. A Cloud field name is not treated as proof of a direct
single-register source, and a causal mapping is not treated as a complete
Growatt enum/bitfield definition.

## Cloud/API inventory and timing

The existing sanitized API inventory exposes these relevant groups:

- inverter: `status`, `status_text`, `operating_mode`, `real_op_percent`;
- BDC: `bdc1_status`, `bdc1_mode`, `bdc1_ibat`, `bdc1_vbat`, charge/discharge
  powers and totals, fault/warning fields and `bdc_derate_reason`;
- BMS: `bms_status`, `bms_ibat`, `bms_vbat`, SOC/SOH and error/warning fields;
- system words: `warn_code`, `new_warn_code`, `fault_type`,
  `sys_fault_word` through `sys_fault_word7`, `warn_text`;
- grid/load/energy: `pac`, `p_system`, `pac_to_local_load`, grid/export and PV
  fields;
- winter mode: `win_mode`, `win_request`, `win_on_grid_soc`,
  `win_off_grid_soc` and window timestamps.

Observed example values retained in the earlier evidence include
`status=1`/`Normal`, BDC/BMS status values, zero fault/warning values, and
the separate BDC/BMS current conventions. Values are not automatically
declared to be direct FC04 sources; aggregate and derived fields remain
classified accordingly.

The retained timing evidence measured the following regime:

- Shine publication cadence: approximately one cloud update per five minutes;
- marker hold windows: approximately five to seven minutes;
- API history acceptance: only assessed after a newer history timestamp;
- retained marker-to-history timestamp separation: approximately 115–124
  minutes in the oracle run.

The latter is not claimed as pure network propagation: device/API clock offset
and Shine/cloud backlog were observed, so the measured interval is a bounded
observation of the usable acceptance regime, not a universal latency promise.
The required rule remains: a marker must span a publication boundary and the
API must show a newer timestamp before attribution.

## Negative and stopped investigations

- I3166, I3211 and I3212 marker values were non-unique in Cloud/API output;
  their experiments did not establish physical mappings beyond the vendor
  definitions.
- Cumulative energy/runtime quantities were not manipulated because fake
  values would pollute cloud history.
- Identity, firmware, plant/account and configuration fields were not
  manipulated.
- No target was probed when the retained evidence indicated source research,
  opaque diagnostic treatment or a likely aggregate was more reliable than a
  blind one-register test.
- No unexpected FC06, FC10, proprietary write or mode change occurred in the
  inherited oracle evidence, and no new outbound Shine reaction was created.

No canonical correction candidate was demonstrated by 5C. Potential future
corrections must still be handled as separate bounded review tasks; this task
does not alter canonical values or hide parity differences.

## Offline validation

The closure artifacts are generated entirely offline from hashed local source
inputs. The validator checks:

- exactly the 129 5B targets are covered;
- one ordered reconciliation decision per target;
- every support reference resolves to a committed claim;
- no secret/token material is present;
- Shine-bound/local-ground-truth safety flags remain intact;
- deterministic rebuild output;
- canonical freeze.

Commands passed:

```text
python3 tools/build_fc04_closure.py --check
python3 tools/validate_fc04_closure.py
python3 tools/validate_fc04_migration.py
python3 tools/validate_resolved_register_reference.py
python3 tools/validate_register_spec.py
python3 tools/validate_authority_coverage.py
python3 -m pytest -q
```

No Home Assistant, broker, inverter or canonical-generator runtime behavior
was changed. The next step is a review decision on the 68 remaining semantic
source gaps, not another broad migration or a global canonical cutover.
