# GII-PIPELINE-11 — Next property-backed repository-wide cohort

Disposition: `GII_PIPELINE_NEXT_PROPERTY_BACKED_COHORT_MIGRATION_ACCEPTED`

## Lineage

- Merged `main` used as the starting point: `94df0ab9f5eee2310766f1b66f1dac9f3f114aa3`.
- Accepted PIPELINE-10 tip verified in ancestry: `50c8028b2112644a41ba95b3a589a7dac1d1d24f`.
- Generation tip recorded: `94df0ab9f5eee2310766f1b66f1dac9f3f114aa3`.

## Accepted authority transition

The accepted-authority registry grew from 5 to 6 sources and from 43 to 49 accepted decisions. PIPELINE-10 is now accepted through the registry; PIPELINE-11 is not registered before its own migration.

## Property-cell baseline after PIPELINE-10 acceptance

| Metric | Value |
| --- | ---: |
| Legacy-authoritative property cells | 49500 |
| Declarative-authoritative property cells | 135 |
| Legacy-exclusive property cells | 41 |

This is the accepted baseline. The registry update itself is not counted as a PIPELINE-11 gain.

## H123/H100 zero-reduction proof

- H123 (`reconciliation/pipeline9_repository_wide_next_cohort.json`): fresh reduction `0`; already accepted.
- H100 (`reconciliation/pipeline10_next_repository_wide_cohort.json`): fresh reduction `0`; already accepted.

Both disappear naturally from the reducible candidate enumeration because accepted property cells are loaded from the registry; no address blacklist or pipeline-specific exclusion is used.

## Repository-wide source-scope coverage

The ranking retains all seven V1.24 source scopes and all 33 declared ranges.

| Scope | Ranges | Records | Accepted declarative cells | Remaining legacy cells | Candidates | Qualified/unresolved | Best candidate | Reduction |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `max_1500v_max_x_lv` | 5 | 625 | 2 | 7709 | 574 | 0 | `v124-row-holding-107-row-015-0108` | 24 |
| `min_tl_xh` | 6 | 750 | 31 | 9040 | 420 | 32 | `v124-row-holding-107-row-015-0108` | 24 |
| `mod_tl3_xh` | 4 | 500 | 2 | 6311 | 380 | 0 | `v124-row-holding-107-row-015-0108` | 24 |
| `storage_mix` | 4 | 500 | 2 | 6177 | 424 | 0 | `v124-row-holding-107-row-015-0108` | 24 |
| `storage_spa` | 5 | 625 | 2 | 7330 | 408 | 0 | `v124-row-holding-107-row-015-0108` | 24 |
| `storage_sph` | 5 | 625 | 2 | 7583 | 486 | 0 | `v124-row-holding-107-row-015-0108` | 24 |
| `tl3_max_mid_mac` | 4 | 500 | 2 | 6212 | 455 | 0 | `v124-row-holding-107-row-015-0108` | 24 |

## Fresh candidate ranking

The previous PIPELINE-10 winner was `v124-row-holding-100-row-014-0101`; its fresh reduction is 0. The previous rank 2 was `v124-row-holding-107-row-015-0108`. Fresh rank 1 is `v124-row-holding-107-row-015-0108` and fresh rank 2 is `v124-row-holding-108-row-015-0109`. Ordering changed beyond satisfying the previous winner: `False`.

| Rank | Candidate | Semantic key | Address | Physical | Paths | Reduction | Evidence | Qualifiers | Conflicts |
| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | `v124-row-holding-107-row-015-0108` | `control.q_v_response_delay` | `holding:107` | 6 | 7 | 24 | 14 | 0 | False |
| 2 | `v124-row-holding-108-row-015-0109` | `control.over_frequency_derating_delay` | `holding:108` | 6 | 7 | 24 | 14 | 0 | False |
| 3 | `v124-row-holding-109-row-015-0110` | `control.maximum_reactive_power_magnitude` | `holding:109` | 6 | 7 | 24 | 14 | 0 | False |
| 4 | `v124-row-holding-110-row-015-0111` | `control.pf_curve_point_1_load` | `holding:110` | 6 | 7 | 24 | 14 | 0 | False |
| 5 | `v124-row-holding-112-row-015-0113` | `control.pf_curve_point_2_load` | `holding:112` | 6 | 7 | 24 | 14 | 0 | False |
| 6 | `v124-row-holding-114-row-015-0115` | `control.pf_curve_point_3_load` | `holding:114` | 6 | 7 | 24 | 14 | 0 | False |
| 7 | `v124-row-holding-116-row-015-0117` | `control.pf_curve_point_4_load` | `holding:116` | 6 | 7 | 24 | 14 | 0 | False |
| 8 | `v124-row-holding-17-row-010-0018` | `control.pv_start_voltage_threshold` | `holding:17` | 6 | 7 | 24 | 14 | 0 | False |
| 9 | `v124-row-holding-18-row-010-0019` | `control.start_up_delay` | `holding:18` | 6 | 7 | 24 | 14 | 0 | False |
| 10 | `v124-row-holding-19-row-010-0020` | `control.restart_delay` | `holding:19` | 6 | 7 | 24 | 14 | 0 | False |
| 11 | `v124-row-holding-52-row-012-0053` | `control.stage_1_undervoltage_limit` | `holding:52` | 6 | 7 | 24 | 14 | 0 | False |
| 12 | `v124-row-holding-53-row-012-0054` | `control.stage_1_overvoltage_limit` | `holding:53` | 6 | 7 | 24 | 14 | 0 | False |

## Selected cohort

Fresh rank 1 `v124-row-holding-107-row-015-0108` is `control.q_v_response_delay` at `holding:107`. It is bounded, has 6/6 unique physical targets and 7/7 applicability paths, and has an evidence-backed expected reduction of 24 property cells.

## Property-level evidence

Every promoted property has explicit noncanonical claim support: `True`. The machine artifact records property names, claim IDs, source types and support per physical target. No unsupported canonical or compatibility value is promoted.

## Physical targets vs applicability paths

Physical authority is deduplicated by canonical family/table/address; applicability evidence retains source-scope/source-declaration paths. The selected cohort therefore has separate physical and path counts, and duplicate paths do not double-count authority.

## Provenance consistency

All 7 applicability paths are in supported applicability states, and all selected decisions cite their retained paths. Property-cell support uses the existing PIPELINE-10A capability rules.

## Semantic parity

Parity is classified over 6 unique physical targets: `{'PARITY_MATCH': 6}`. Canonical SHA is `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` and `canonical_modified=false`.

## Authority movement

| Metric | Accepted baseline | Selected cohort before | Repository after | Selected cohort after |
| --- | ---: | ---: | ---: | ---: |
| Legacy-authoritative property cells | 49500 | 78 | 49476 | 54 |
| Declarative-authoritative property cells | 135 | — | 159 | — |
| Legacy-exclusive property cells | 41 | 0 | 41 | 0 |

The repository legacy count decreases and declarative count increases solely through the selected property-supported decisions; legacy-exclusive remains measured rather than forced.

## Deferred opportunities

Only one cohort is migrated. The top deferred candidates, including qualifiers/conflicts and their calculated reductions, remain in the machine artifact.

## Correction candidates

H3085 remains a `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`; no canonical correction is made here.

## Reusable runner/refactor

PIPELINE-11 reuses the repository-wide candidate enumerator, accepted-authority registry, property-cell support rules and PIPELINE-9 decision/authority mechanics. The small `tools/build_property_backed_cohort.py` module provides shared physical/path views and parity/support checks without introducing a second authority or claims model.

## Safety and validation

No inverter writes, Shine injection, cloud experiment, broker change, Home Assistant change, runtime deployment or global cutover was performed. PIPELINE-11 is an offline semantic-authority migration only.

Generated by `tools/build_pipeline11_cohort.py`; no canonical register specification was modified.
