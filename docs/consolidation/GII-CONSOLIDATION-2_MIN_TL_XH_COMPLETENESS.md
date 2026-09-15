# GII-CONSOLIDATION-2 — MIN/TL-XH completeness pass

This bounded, offline pass classifies the original C1 MIN/TL-XH physical gaps. The canonical specification remains frozen; the V1.24 candidate remains a review artifact.

## Lineage and scope

- C1 baseline/replay SHA: `a799c16d2b4e523a1304dd45d91a09d10da7b3a7`
- Frozen canonical SHA: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`
- V1.24 PDF SHA-256: `fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320`
- No PDF, canonical specification, HA, broker, inverter, cloud or production configuration was modified.

## MIN/TL-XH physical coverage

| Measure | C1 baseline | After generic extraction repair |
|---|---:|---:|
| Canonical physical keys | 895 | 895 |
| Candidate physical keys (range spans) | 518 | 648 |
| Covered canonical keys | 518 | 648 |
| Missing canonical keys | 377 | 247 |
| Canonical logical register keys | 0 | 0 |
| Canonical logical fields (separate layer) | 132 | 132 |

The original 377 missing keys are represented exactly once in the classification artifact. Range spans are expanded for physical coverage; logical fields are reported separately and are not counted as physical registers.

## Disjoint gap classification

| Category | Count |
|---|---:|
| `CANONICAL_ONLY_PHYSICAL_REGISTER` | 8 |
| `DIFFERENT_PROTOCOL_OR_SOURCE_REQUIRED` | 94 |
| `OUTSIDE_VENDOR_V124_APPLICABILITY` | 145 |
| `RESOLVED_BY_LOCAL_EXTRACTION_REPAIR` | 130 |
| **Total** | **377** |

The local parser repair resolves split/continued source ranges generically. Remaining canonical-only and outside-applicability keys are fully classified rather than called unexplained. Final unexplained count: **0**.

## Source and conflict review

- Ambiguous source addresses: **81 → 22**; the remaining rows are retained in the vendor review queue and are outside the selected MIN projection.
- Vendor rows without a canonical match: **96 → 95** in the rolling artifact; these are non-MIN V1.24 scopes, not MIN completeness gaps.
- Original C1 conflicts reviewed: **23**; dispositions: `{'RESOLVED_COMPATIBLE_VENDOR_WRITABLE_MARKER': 17, 'RETAINED_ACCESS_CONFLICT_REVIEW': 4, 'RETAINED_SEMANTIC_CONFLICT_REVIEW': 2}`.
- The 17 compatible access-marker cases are resolved as writable markers under the V1.24 `Write Value or not` heading. Four read/write capability conflicts remain. Both H3085 semantic conflicts remain explicit; no external-meter meaning is inferred.

## Read/write readiness

Read readiness is reported as disjoint status counts plus overlapping property flags. Documented writability is not live-write verification and does not authorize HA writes. The selected candidate contains no write-verified record.

- After repair disjoint read status: `{'CONFLICT_BLOCKED': 4, 'NEEDS_METADATA': 85, 'READY_READ': 504, 'RESERVED_OR_UNSUPPORTED': 55}`.
- Before repair disjoint read status: `{'CONFLICT_BLOCKED': 6, 'NEEDS_METADATA': 85, 'READY_READ': 402, 'RESERVED_OR_UNSUPPORTED': 25}`; `READY_READ` therefore changes 402 → 504.
- After repair quality flags: `{'NEEDS_SCALE': 360, 'NEEDS_SEMANTIC_REVIEW': 38, 'NEEDS_SIGNEDNESS': 464, 'NEEDS_UNIT': 298}`.
- After repair write readiness: `{'physical_keys_evaluated': 648, 'documented_writable': 216, 'safe_ha_write_candidate': 57, 'live_write_verified': 0, 'note': 'Documented writability is not live-write verification or an authorization to write.'}`.
- Before repair write readiness: `{'physical_keys_evaluated': 518, 'documented_writable': 114, 'safe_ha_write_candidate': 56, 'live_write_verified': 0, 'note': 'Documented writability is not live-write verification or an authorization to write.'}`.
- Logical field coverage: `{'canonical_logical_fields': 132, 'canonical_logical_field_components': 331, 'fully_covered': 88, 'partially_covered': 1, 'not_covered': 43}`.

## Research queue and disposition

The queue contains only evidence-dependent follow-up: H3085 semantic identity and canonical-only physical tails. Outside-applicability rows are explained and are not queued as MIN work.

`GII_MIN_TLXH_CONSOLIDATION_COMPLETENESS_ACCEPTED_WITH_FOLLOW_UP`

## Verification

- Full suite: `PYTHONPATH=. pytest -q --durations=25` — all 120 collected tests passed; the command emitted the slowest 25 list recorded for handoff.
- Focused consolidation/extraction suite: 21 passed.
- Validators: claims, vendor claims, canonical spec, resolved reference, MIN metadata, reconciliation, authority coverage, FC04 closure/migration/source research, C1 and C2 all passed.
- Two consecutive C1/C2 generation replays produced byte-identical artifacts.

## Generated artifacts

- `docs/consolidation/data/GII-CONSOLIDATION-2_MIN_TL_XH_GAP_CLASSIFICATION.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2_MIN_TL_XH_PROJECTION.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2_CONFLICTS.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2_UNRESOLVED.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2_RESEARCH_QUEUE.json`
- `spec/growatt-register-spec-v2-candidate.json` (regenerated C1 candidate, not canonical)
