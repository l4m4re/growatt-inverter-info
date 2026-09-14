# GII-PIPELINE-10 — Next repository-wide V1.24 cohort

Disposition: `GII_PIPELINE_NEXT_REPOSITORY_WIDE_COHORT_MIGRATION_ACCEPTED`

## Baseline

- Current merged `main`: `c8a95b6bdcdc566dd6cac2ce5b64879c679bc4b5`; PIPELINE-9/9A is an ancestor.
- Canonical SHA-256: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`; `canonical_modified=false`.
- Accepted PIPELINE-9 decisions included in baseline: 6.

## Repository-wide source-scope coverage

Fresh ranking uses all seven V1.24 source scopes and all 33 retained FC03/FC04 range claims.

| Scope | Family | Ranges | Records | Candidates | Qualified/unresolved | Best reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: |
| `max_1500v_max_x_lv` | `tl3_max_mid_mac` | 5 | 625 | 583 | 0 | 30 |
| `min_tl_xh` | `min_tl_xh` | 6 | 750 | 477 | 35 | 30 |
| `mod_tl3_xh` | `mod_tl3_xh` | 4 | 500 | 470 | 0 | 30 |
| `storage_mix` | `storage_mix` | 4 | 500 | 449 | 0 | 30 |
| `storage_spa` | `storage_spa` | 5 | 625 | 438 | 0 | 30 |
| `storage_sph` | `storage_sph` | 5 | 625 | 516 | 0 | 30 |
| `tl3_max_mid_mac` | `tl3_max_mid_mac` | 4 | 500 | 464 | 0 | 30 |

## Ranking after PIPELINE-9

The previous rank-1 H123 cohort is now accounted for; its fresh expected reduction is 0. The new rank-1 is `v124-row-holding-10-row-010-0011`. Ranks 2+ shifted: `True`.

Candidate universe: 1312 bounded candidates (1023 shared-row, 835 with non-MIN scope).

| Rank | Candidate | Semantic key | Address | Physical | Paths | Reduction | Evidence | Qualifiers |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| 1 | `v124-row-holding-10-row-010-0011` | `field.firmware` | `holding:10` | 6 | 7 | 30 | 14 | 0 |
| 2 | `v124-row-holding-100-row-014-0101` | `control.power_factor_curve_lock_out_voltage` | `holding:100` | 6 | 7 | 30 | 14 | 0 |
| 3 | `v124-row-holding-107-row-015-0108` | `control.q_v_response_delay` | `holding:107` | 6 | 7 | 30 | 14 | 0 |
| 4 | `v124-row-holding-108-row-015-0109` | `control.over_frequency_derating_delay` | `holding:108` | 6 | 7 | 30 | 14 | 0 |
| 5 | `v124-row-holding-109-row-015-0110` | `control.maximum_reactive_power_magnitude` | `holding:109` | 6 | 7 | 30 | 14 | 0 |
| 6 | `v124-row-holding-11-row-010-0012` | `field.firmware` | `holding:11` | 6 | 7 | 30 | 14 | 0 |
| 7 | `v124-row-holding-110-row-015-0111` | `control.pf_curve_point_1_load` | `holding:110` | 6 | 7 | 30 | 14 | 0 |
| 8 | `v124-row-holding-112-row-015-0113` | `control.pf_curve_point_2_load` | `holding:112` | 6 | 7 | 30 | 14 | 0 |
| 9 | `v124-row-holding-114-row-015-0115` | `control.pf_curve_point_3_load` | `holding:114` | 6 | 7 | 30 | 14 | 0 |
| 10 | `v124-row-holding-116-row-015-0117` | `control.pf_curve_point_4_load` | `holding:116` | 6 | 7 | 30 | 14 | 0 |
| 11 | `v124-row-holding-12-row-010-0013` | `field.firmware` | `holding:12` | 6 | 7 | 30 | 14 | 0 |
| 12 | `v124-row-holding-13-row-010-0014` | `field.firmware` | `holding:13` | 6 | 7 | 30 | 14 | 0 |

## Previous H123 state

`v124-row-holding-123-row-015-0124` was PIPELINE-9 rank 1 with reduction 30. With its accepted decisions included, it is `accepted_authority_included; no fresh reducible candidate` and contributes no fresh reduction.

## Selected cohort

Fresh rank-1 `v124-row-holding-10-row-010-0011` is semantic `field.firmware` at `holding:10` across: `max_1500v_max_x_lv`, `min_tl_xh`, `mod_tl3_xh`, `storage_mix`, `storage_spa`, `storage_sph`, `tl3_max_mid_mac`.
Canonical physical targets: 6/6; applicability paths: 7/7. Physical parity is 100% and path coverage is 100%.

## Physical targets vs applicability paths

The repaired PIPELINE-9A path identity is retained. Physical authority is deduplicated by canonical family/table/address; applicability evidence is keyed by canonical family/table/address/source scope/source declaration. Multiple paths therefore produce one property promotion per physical target.

## Property-level evidence and provenance consistency

The selected cohort produces 6 property decisions. Every promoted property has noncanonical support: `True`. Applicability path consistency is 7/7.

## Semantic parity

Semantic parity is computed over 6 unique physical targets: `{'PARITY_MATCH': 6}`. It is not inflated by duplicate applicability paths.

## Authority movement

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Repository legacy-authoritative cells | 49471 | 49441 | -30 |
| Repository declarative-authoritative cells | 210 | 240 | +30 |
| Repository legacy-exclusive cells | 41 | 41 | +0 |
| Selected cohort legacy-authoritative cells | 78 | 48 | -30 |
| Selected cohort declarative-authoritative cells | 0 | 30 | +30 |
| Selected cohort legacy-exclusive cells | 0 | 0 | +0 |

## Deferred opportunities

Only the current rank-1 bounded cohort is migrated. The remaining ranked candidates are retained in the machine-readable artifact. H3085 remains deferred as `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`.

## Safety and validation

No inverter write, Shine/cloud experiment, broker change, Home Assistant change or global cutover was performed. Maintained validators and the full pytest suite were run offline after generation; the archived missing-fixture validator remains non-gating.

Generated by `tools/build_pipeline10_cohort.py`; no canonical register specification was modified.
