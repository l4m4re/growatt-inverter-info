# GII-PIPELINE-10 — Next repository-wide V1.24 cohort

Disposition: `GII_PIPELINE_NEXT_REPOSITORY_WIDE_COHORT_MIGRATION_ACCEPTED`

## Baseline

- Current merged `main`: `c0ba1dea54fd170e1ecd1b22494b2a84d46b6eee`; PIPELINE-9/9A is an ancestor.
- Canonical SHA-256: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`; `canonical_modified=false`.
- Accepted PIPELINE-9 decisions included in baseline: 6.

## PIPELINE-10A property-cell provenance repair

The provisional PIPELINE-10 accounting expanded one `semantic_mapping` decision into a fixed set of five canonical properties. That decision-level shortcut allowed canonical comparison values, blank source fields and `source_semantics_preserved` normalization text to look like independent evidence. It has been removed from authority accounting.

The corrected model promotes only explicitly supported canonical property cells. Each promoted cell retains claim IDs and source types; applicability claims establish scope only and do not prove unit, signedness, scale, datatype or normalization. Canonical and compatibility values remain available for parity and migration-risk analysis, not as evidence.

The accepted registry contains 43 decisions. The audit removed 88 duplicate physical property cells from the previously implied accounting (75 decision-level implications).

| Accounting | Legacy-authoritative cells | Declarative-authoritative cells | Legacy-exclusive cells |
| --- | ---: | ---: | ---: |
| Old broad decision-level baseline | 49471 | 210 | 41 |
| Corrected explicit property-cell baseline | 49524 | 111 | 41 |

H123 retains 6 physical targets and 7 applicability paths. Its historical broad reduction was 30; the corrected property-supported reduction is 24. H10 is independently re-ranked: its historical broad reduction was 30, while its corrected reduction is 12. H10 is therefore not forced to remain rank 1.

## Repository-wide source-scope coverage

Fresh ranking uses all seven V1.24 source scopes and all 33 retained FC03/FC04 range claims.

| Scope | Family | Ranges | Records | Candidates | Qualified/unresolved | Best reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `max_1500v_max_x_lv` | `tl3_max_mid_mac` | 5 | 625 | 575 | 0 | 24 |
| `min_tl_xh` | `min_tl_xh` | 6 | 750 | 421 | 32 | 24 |
| `mod_tl3_xh` | `mod_tl3_xh` | 4 | 500 | 381 | 0 | 24 |
| `storage_mix` | `storage_mix` | 4 | 500 | 425 | 0 | 24 |
| `storage_spa` | `storage_spa` | 5 | 625 | 409 | 0 | 24 |
| `storage_sph` | `storage_sph` | 5 | 625 | 487 | 0 | 24 |
| `tl3_max_mid_mac` | `tl3_max_mid_mac` | 4 | 500 | 456 | 0 | 24 |

## Ranking after PIPELINE-9

The previous rank-1 H123 cohort is now accounted for; its fresh expected reduction is 0. The new corrected rank-1 is `v124-row-holding-100-row-014-0101`. Ranks 2+ shifted: `True`.

Candidate universe: 1195 bounded candidates (930 shared-row, 774 with non-MIN scope).

| Rank | Candidate | Semantic key | Address | Physical | Paths | Reduction | Evidence | Qualifiers |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `v124-row-holding-100-row-014-0101` | `control.power_factor_curve_lock_out_voltage` | `holding:100` | 6 | 7 | 24 | 14 | 0 |
| 2 | `v124-row-holding-107-row-015-0108` | `control.q_v_response_delay` | `holding:107` | 6 | 7 | 24 | 14 | 0 |
| 3 | `v124-row-holding-108-row-015-0109` | `control.over_frequency_derating_delay` | `holding:108` | 6 | 7 | 24 | 14 | 0 |
| 4 | `v124-row-holding-109-row-015-0110` | `control.maximum_reactive_power_magnitude` | `holding:109` | 6 | 7 | 24 | 14 | 0 |
| 5 | `v124-row-holding-110-row-015-0111` | `control.pf_curve_point_1_load` | `holding:110` | 6 | 7 | 24 | 14 | 0 |
| 6 | `v124-row-holding-112-row-015-0113` | `control.pf_curve_point_2_load` | `holding:112` | 6 | 7 | 24 | 14 | 0 |
| 7 | `v124-row-holding-114-row-015-0115` | `control.pf_curve_point_3_load` | `holding:114` | 6 | 7 | 24 | 14 | 0 |
| 8 | `v124-row-holding-116-row-015-0117` | `control.pf_curve_point_4_load` | `holding:116` | 6 | 7 | 24 | 14 | 0 |
| 9 | `v124-row-holding-17-row-010-0018` | `control.pv_start_voltage_threshold` | `holding:17` | 6 | 7 | 24 | 14 | 0 |
| 10 | `v124-row-holding-18-row-010-0019` | `control.start_up_delay` | `holding:18` | 6 | 7 | 24 | 14 | 0 |
| 11 | `v124-row-holding-19-row-010-0020` | `control.restart_delay` | `holding:19` | 6 | 7 | 24 | 14 | 0 |
| 12 | `v124-row-holding-52-row-012-0053` | `control.stage_1_undervoltage_limit` | `holding:52` | 6 | 7 | 24 | 14 | 0 |

## Previous H123 state

`v124-row-holding-123-row-015-0124` was PIPELINE-9 rank 1 with reduction 30. With its accepted decisions included, it is `accepted_authority_included; no fresh reducible candidate` and contributes no fresh reduction.

## Selected cohort

Fresh rank-1 `v124-row-holding-100-row-014-0101` is semantic `control.power_factor_curve_lock_out_voltage` at `holding:100` across: `max_1500v_max_x_lv`, `min_tl_xh`, `mod_tl3_xh`, `storage_mix`, `storage_spa`, `storage_sph`, `tl3_max_mid_mac`.
Canonical physical targets: 6/6; applicability paths: 7/7. Physical parity is 100% and path coverage is 100%.

## Physical targets vs applicability paths

The repaired PIPELINE-9A path identity is retained. Physical authority is deduplicated by canonical family/table/address; applicability evidence is keyed by canonical family/table/address/source scope/source declaration. Multiple paths therefore produce one property promotion per physical target.

## Property-level evidence and provenance consistency

The selected cohort produces 6 property decisions. Every promoted property has noncanonical support: `True`. Applicability path consistency is 7/7. The machine audit is `docs/pipeline/data/GII-PIPELINE-10A_PROPERTY_CELL_PROVENANCE_AUDIT.json`.

## Semantic parity

Semantic parity is computed over 6 unique physical targets: `{'PARITY_MATCH': 6}`. It is not inflated by duplicate applicability paths.

## Authority movement

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Repository legacy-authoritative cells | 49524 | 49500 | -24 |
| Repository declarative-authoritative cells | 111 | 135 | +24 |
| Repository legacy-exclusive cells | 41 | 41 | +0 |
| Selected cohort legacy-authoritative cells | 78 | 54 | -24 |
| Selected cohort declarative-authoritative cells | 0 | 24 | +24 |
| Selected cohort legacy-exclusive cells | 0 | 0 | +0 |

## Deferred opportunities

Only the current rank-1 bounded cohort is migrated. The remaining ranked candidates are retained in the machine-readable artifact. H3085 remains deferred as `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`.

## Safety and validation

No inverter write, Shine/cloud experiment, broker change, Home Assistant change or global cutover was performed. Maintained validators and the full pytest suite were run offline after generation; the archived missing-fixture validator remains non-gating.

Generated by `tools/build_pipeline10_cohort.py`; no canonical register specification was modified.
