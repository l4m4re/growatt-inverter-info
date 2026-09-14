# GII-PIPELINE-9 — Repository-wide V1.24 next cohort

Disposition: `GII_PIPELINE_REPOSITORY_WIDE_NEXT_COHORT_MIGRATION_ACCEPTED`

## Baseline

- Starting merged `main`: `99f36b3b1cde76f757aae7ae9d2c72f44eb30830`.
- Canonical SHA-256: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` before and after; `canonical_modified=false`.
- Authority before: legacy 49501, declarative 180, legacy-exclusive 41.

## Repository-wide V1.24 coverage

The enumerator retains canonical family, source scope, declaration, table, address and qualifier as separate fields. It consumed all seven V1.24 source scopes and all 33 retained range claims.

| Source scope | Family | Ranges | Applicable records | Partly declarative | Legacy cells | Candidates | Qualified/unresolved | Best reduction |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `max_1500v_max_x_lv` | `tl3_max_mid_mac` | 5 | 625 | 0 | 7717 | 584 | 0 | 30 |
| `min_tl_xh` | `min_tl_xh` | 6 | 750 | 18 | 9001 | 478 | 35 | 30 |
| `mod_tl3_xh` | `mod_tl3_xh` | 4 | 500 | 0 | 6319 | 471 | 0 | 30 |
| `storage_mix` | `storage_mix` | 4 | 500 | 0 | 6185 | 450 | 0 | 30 |
| `storage_spa` | `storage_spa` | 5 | 625 | 0 | 7338 | 439 | 0 | 30 |
| `storage_sph` | `storage_sph` | 5 | 625 | 0 | 7591 | 517 | 0 | 30 |
| `tl3_max_mid_mac` | `tl3_max_mid_mac` | 4 | 500 | 0 | 6220 | 465 | 0 | 30 |

## Candidate generation and ranking

Candidates are derived by joining each retained V1.24 vendor row claim to every explicitly applicable canonical family/source-scope path at the same physical table/address. Exact row identity and canonical semantic identity are grouping keys; source scopes are never inferred from canonical family membership. Candidates are bounded to at most eight physical targets.

The universe contains 1313 bounded candidates, including 1024 shared-vendor-row candidates and 835 candidates with a non-MIN source scope.

| Rank | Candidate | Kind | Scope(s) | Family(s) | Address | Physical units | Paths | Expected reduction | Evidence score | Qualifiers |
| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | `v124-row-holding-123-row-015-0124` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:123 | 6 | 7 | 30 | 28 | 0 |
| 2 | `v124-row-holding-10-row-010-0011` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:10 | 6 | 7 | 30 | 14 | 0 |
| 3 | `v124-row-holding-100-row-014-0101` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:100 | 6 | 7 | 30 | 14 | 0 |
| 4 | `v124-row-holding-107-row-015-0108` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:107 | 6 | 7 | 30 | 14 | 0 |
| 5 | `v124-row-holding-108-row-015-0109` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:108 | 6 | 7 | 30 | 14 | 0 |
| 6 | `v124-row-holding-109-row-015-0110` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:109 | 6 | 7 | 30 | 14 | 0 |
| 7 | `v124-row-holding-11-row-010-0012` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:11 | 6 | 7 | 30 | 14 | 0 |
| 8 | `v124-row-holding-110-row-015-0111` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:110 | 6 | 7 | 30 | 14 | 0 |
| 9 | `v124-row-holding-112-row-015-0113` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:112 | 6 | 7 | 30 | 14 | 0 |
| 10 | `v124-row-holding-114-row-015-0115` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:114 | 6 | 7 | 30 | 14 | 0 |
| 11 | `v124-row-holding-116-row-015-0117` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:116 | 6 | 7 | 30 | 14 | 0 |
| 12 | `v124-row-holding-12-row-010-0013` | shared_vendor_row | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | holding:12 | 6 | 7 | 30 | 14 | 0 |

## Selected cohort

The selected cohort is rank 1 from the fresh repository-wide ranking: `v124-row-holding-123-row-015-0124`. It was not selected by a MIN-specific address list. It is a bounded `shared_vendor_row` at `holding:123` with semantic key `control.export_limit_power_setpoint` and 6 physical canonical targets across: `max_1500v_max_x_lv`, `min_tl_xh`, `mod_tl3_xh`, `storage_mix`, `storage_spa`, `storage_sph`, `tl3_max_mid_mac`.

Every target retains its own source-scope applicability and source declaration. Duplicate physical identities reached through multiple declarations are not counted twice in physical parity or authority reduction.

Canonical physical targets: 6; applicability paths: 7 (coverage 100%).
Physical parity: overall 100%; per family: `min_tl_xh` 100%, `mod_tl3_xh` 100%, `storage_mix` 100%, `storage_spa` 100%, `storage_sph` 100%, `tl3_max_mid_mac` 100%.

## PIPELINE-9A path-vs-physical identity repair

The original generator keyed evidence and property structures only by `family:table:address`. That collapsed the two legitimate paths to `tl3_max_mid_mac:holding:123`: the generic `tl3_max_mid_mac` declaration and the `max_1500v_max_x_lv` declaration. The repaired path key includes canonical family, table, address, source scope and source declaration. Physical authority and parity use a separate deduplicated canonical key.

The resulting H123 cohort therefore has 6 canonical physical targets and 7 applicability paths. The TL3 physical target is promoted once, while its two valid source paths remain independently inspectable and are aggregated explicitly in the reconciliation scope. Every cited applicability claim matches its own source-scope/source-declaration path; cross-scope support is rejected by regression tests.


## Evidence and semantic parity

Each selected target records physical applicability, semantic row, access, enum/packed layout, unit/scale, row-local qualifier, independent corroboration, source conflict, runtime/live evidence, write documentation, live-write verification and unresolved property count. Promoted properties reference vendor-row and explicit applicability claims; canonical parity is used only for comparison, not as evidence.

Semantic parity summary: `{'PARITY_MATCH': 6}`. Qualified applicability remains qualified; no qualified range was promoted to unconditional.

## Authority movement

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Repository legacy-authoritative cells | 49501 | 49471 | -30 |
| Repository declarative-authoritative cells | 180 | 210 | +30 |
| Repository legacy-exclusive cells | 41 | 41 | +0 |
| Selected cohort legacy-authoritative cells | 78 | 48 | -30 |
| Selected cohort legacy-exclusive cells | 0 | 0 | +0 |

The machine-readable artifact contains selected before/after property-cell metrics per family. The selected cohort reduces legacy authority; repository legacy authority also decreases.

## Deferred opportunities and correction candidates

Only one cohort is migrated. Larger shared-row opportunities remain ranked and are deferred for later reviewed cohorts rather than silently discarded. H3085 remains `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`; canonical is unchanged.

## Safety and validation

No inverter write, reset, HA/runtime change, broker change, global cutover or live experiment was performed. This is shadow declarative authority only; no live-write verification is invented.

The maintained validators and full pytest suite are the acceptance gates. The archived `tools/legacy/validate_min_6000tl_xh_map.py` remains non-gating because its historical fixture `tools/legacy/min_6000tl_xh_register_map.json` is absent; it was not recreated.

Generated by `tools/build_pipeline9_cohort.py`; all ranking and report values are derived from the checked-in canonical/spec, claims, applicability and authority data.
