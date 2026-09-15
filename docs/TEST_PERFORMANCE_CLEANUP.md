# Bounded pytest performance cleanup

Date: 2026-09-15

This is a test-only performance pass. It keeps the full test gate and does not
change the canonical register specification, runtime code, or production
configuration.

## Measurements

The baseline was measured before the cleanup with the requested commands:

```text
PYTHONPATH=. pytest -q --durations=30
real 398.18s
user 379.07s
sys   15.93s
124 passed; pytest-reported duration 391.53s

PYTHONPATH=. pytest --durations=0 -vv
real 398.53s
user 380.86s
sys   15.33s
124 passed; pytest-reported duration 391.53s
```

The second command was retained as `/tmp/gii-pytest-before-vv.txt` during the
investigation. The expensive work was concentrated in repeated historical
PIPELINE-6 through PIPELINE-11 enumeration/build/determinism calls, authority
coverage construction, and full generated-spec/reference validation.

The main repeated-call inventory was:

| Work | Before | After |
| --- | ---: | ---: |
| PIPELINE-6 cohort build | 3 | 1 module-fixture result |
| FC04 closure build | 3 | 1 module-fixture result |
| FC04 source-research build | 3 | 1 module-fixture result |
| FC04 migration `build_all()` | 2 | 1 module-fixture result |
| PIPELINE-9 candidate enumeration in tests | 3 | 2, retained in one determinism check |
| PIPELINE-10 fresh enumeration | 2 | 0, checked from the committed artifact |
| PIPELINE-11 fresh enumeration | 3 | 0, checked from the committed artifact |
| Large generic-claims JSON loads in claim/pipeline modules | repeated per test | one cached load per module |

The two-build determinism checks for PIPELINE-7, PIPELINE-8, PIPELINE-10,
PIPELINE-11, and the reconciliation shadow remain deliberate slow checks.

## Changes

- Added the registered `slow` marker in `pyproject.toml`. The normal
  development command is now:

  ```text
  PYTHONPATH=. pytest -q -m "not slow"
  ```

- Added module-scoped fixtures for immutable results in the PIPELINE-6,
  FC04-closure, FC04-source-research, FC04-migration, and authority-coverage
  tests. Each module now builds its expensive result once when several tests
  inspect the same result.
- Added one-process cached loaders for the large generic-claims dataset in
  the claim and pipeline test modules.
- Converted repeated historical invariant checks to read the committed
  generated artifact where regeneration is not the subject of the test.
  This includes the repository-wide scope/range checks in PIPELINE-9 through
  PIPELINE-11 and the repeated PIPELINE-6 invariant check.
- Kept one explicit generator/determinism or integration check for each
  relevant generator. Those checks remain in the full gate and are marked
  `slow`; no coverage was removed from the full suite.

No test was made to pass by weakening an assertion. Generated artifacts were
only rechecked; the existing generated timestamp was left unchanged so the
authority input hash remains reproducible.

## After measurements

```text
PYTHONPATH=. pytest -q -m "not slow"
real 60.30s
user 53.99s
sys   4.83s
101 tests passed

PYTHONPATH=. pytest -q -m slow --durations=30
real 255.87s
user 241.80s
sys  10.40s
23 tests passed

PYTHONPATH=. pytest -q --durations=30
real 291.37s
user 276.74s
sys  12.38s
124 tests passed
```

The full-suite wall time fell by 106.81 seconds, from 398.18 s to 291.37 s
(26.8%). The default development suite is 60.30 s, well below the old full
suite cost. The separately measured slow suite accounts for the intentionally
retained historical rebuild and determinism coverage.

## Slowest tests before

| Time | Test |
| ---: | --- |
| 78.51s | `tests/test_pipeline10.py::test_pipeline10b_lineage_keeps_immutable_start_and_repair_roles` |
| 72.78s | `tests/test_pipeline11.py::test_lineage_canonical_freeze_and_determinism` |
| 25.47s | `tests/test_pipeline9.py::test_candidate_ranking_is_deterministic_and_repository_wide` |
| 24.54s | `tests/test_pipeline10.py::test_fresh_enumeration_remains_repository_wide_and_deterministic` |
| 15.33s | `tests/test_pipeline8.py::test_pipeline8_selects_bounded_cohort_and_is_deterministic` |
| 12.87s | `tests/test_pipeline11.py::test_all_scopes_and_ranges_remain_in_fresh_enumeration` |
| 12.82s | `tests/test_pipeline9.py::test_enumeration_covers_all_v124_source_scopes_and_ranges` |
| 11.64s | `tests/test_register_spec.py::test_canonical_spec_validates_and_preserves_table_identity` |
| 10.17s | `tests/test_pipeline8.py::test_generic_claims_validate` |
| 9.78s | `tests/test_generic_claims.py::test_generic_claims_validate` |
| 9.58s | setup `tests/test_pipeline7_cohort.py::test_pipeline7_ranks_and_selects_one_bounded_cohort` |
| 9.37s | `tests/test_pipeline7_cohort.py::test_pipeline7_is_deterministic_and_keeps_canonical_frozen` |
| 6.38s | `tests/test_register_spec.py::test_generated_human_docs_persist_and_regenerate_deterministically` |
| 4.49s | `tests/test_fc04_closure.py::test_closure_artifacts_rebuild_deterministically` |
| 4.32s | `tests/test_fc04_closure.py::test_closure_preserves_evidence_and_safety_boundaries` |
| 3.81s | `tests/test_authority_coverage.py::test_authority_inventory_is_deterministic_and_current` |
| 3.68s | `tests/test_fc04_migration.py::test_fc04_artifacts_are_current_and_safe` |
| 3.31s | `tests/test_pipeline6_cohort.py::test_pipeline6_reduces_legacy_authority_without_changing_record_count` |
| 3.11s | `tests/test_pipeline6_cohort.py::test_pipeline6_is_bounded_and_physical_complete` |
| 3.01s | `tests/test_pipeline6_cohort.py::test_pipeline6_output_is_reproducible_and_canonical_is_untouched` |
| 2.85s | `tests/test_fc04_migration.py::test_offline_rebuild_matches_committed_artifacts` |
| 2.83s | `tests/test_pipeline8.py::test_applicability_respects_source_scope_and_qualifiers` |
| 2.83s | `tests/test_fc04_migration.py::test_fc04_cohort_and_i3000_regression` |
| 2.43s | `tests/test_resolved_register_reference.py::test_resolved_reference_is_valid_and_reproducible` |
| 1.94s | `tests/test_pipeline8.py::test_v124_all_declared_ranges_are_preserved` |
| 1.94s | `tests/test_vendor_pdf_extraction.py::test_claim_artifacts_validate` |
| 1.69s | `tests/test_pipeline8.py::test_v124_all_family_declarations_are_projected` |
| 1.68s | `tests/test_vendor_pdf_extraction.py::test_validator_catches_broken_continuation_and_duplicate_id` |
| 1.42s | `tests/test_pipeline9.py::test_duplicate_paths_do_not_double_count_authority_reduction` |

## Slowest tests after

| Time | Test |
| ---: | --- |
| 77.26s | `tests/test_pipeline10.py::test_pipeline10b_lineage_keeps_immutable_start_and_repair_roles` |
| 48.10s | `tests/test_pipeline11.py::test_lineage_canonical_freeze_and_determinism` |
| 26.18s | `tests/test_pipeline9.py::test_candidate_ranking_is_deterministic_and_repository_wide` |
| 16.61s | `tests/test_pipeline8.py::test_pipeline8_selects_bounded_cohort_and_is_deterministic` |
| 11.06s | `tests/test_pipeline8.py::test_generic_claims_validate` |
| 10.50s | `tests/test_register_spec.py::test_canonical_spec_validates_and_preserves_table_identity` |
| 9.65s | `tests/test_generic_claims.py::test_generic_claims_validate` |
| 9.29s setup `tests/test_pipeline7_cohort.py::test_pipeline7_ranks_and_selects_one_bounded_cohort` |
| 8.39s | `tests/test_pipeline7_cohort.py::test_pipeline7_is_deterministic_and_keeps_canonical_frozen` |
| 6.44s | `tests/test_register_spec.py::test_generated_human_docs_persist_and_regenerate_deterministically` |
| 5.00s | `tests/test_fc04_closure.py::test_closure_covers_all_5b_unresolved_targets` |
| 4.71s setup `tests/test_fc04_closure.py::test_closure_covers_all_5b_unresolved_targets` |
| 3.99s | `tests/test_fc04_migration.py::test_fc04_artifacts_are_current_and_safe` |
| 3.64s setup `tests/test_pipeline6_cohort.py::test_pipeline6_is_bounded_and_physical_complete` |
| 3.33s setup `tests/test_fc04_migration.py::test_fc04_cohort_and_i3000_regression` |
| 2.84s | `tests/test_vendor_pdf_extraction.py::test_claim_artifacts_validate` |
| 2.78s | `tests/test_resolved_register_reference.py::test_resolved_reference_is_valid_and_reproducible` |
| 2.18s | `tests/test_authority_coverage.py::test_authority_inventory_is_deterministic_and_current` |
| 1.76s | `tests/test_vendor_pdf_extraction.py::test_validator_catches_broken_continuation_and_duplicate_id` |
| 1.53s | `tests/test_pipeline9.py::test_duplicate_paths_do_not_double_count_authority_reduction` |
| 1.28s | `tests/test_register_spec.py::test_min_metadata_consistency_checker_catches_unit_collisions` |
| 0.99s | `tests/test_reconciliation.py::test_shadow_regeneration_is_deterministic` |
| 0.99s | `tests/test_pipeline9.py::test_selected_decisions_have_scope_consistent_applicability_support` |
| 0.92s | `tests/test_pipeline9.py::test_path_level_evidence_keys_do_not_collide` |
| 0.92s | `tests/test_register_spec.py::test_canonical_coverage_exposes_structures_and_enums` |
| 0.86s | `tests/test_pipeline9.py::test_every_selected_decision_has_explicit_scope_and_source_support` |
| 0.84s | `tests/test_gii_consolidation.py::test_generated_consolidation_is_valid` |
| 0.80s | `tests/test_pipeline11.py::test_selected_properties_have_capable_noncanonical_support` |
| 0.74s | `tests/test_vendor_pdf_extraction.py::test_golden_cases` |

## Result

The cleanup meets the bounded goal: the fast suite is substantially cheaper,
the full suite remains the merge gate, and the expensive generator checks are
still executed explicitly in the slow group.
