# GII PIPELINE-5A through 5D lineage repair

## Disposition

`GII_PIPELINE_LINEAGE_REPAIR_ACCEPTED`

This branch reconstructs PIPELINE-5A through 5D on the accepted PIPELINE-4A
architecture. The original historical branches were not rewritten and the
canonical register specification was not changed.

Repair branch:

`repair/gii-pipeline-5a-5d-lineage-20260913`

Starting SHA:

`8ceb8cd94f50235af4fc10b44ad8cbb355919518`

The verified implementation tip before LINEAGE-REPAIR-1A metadata
normalization was `0c31a66e2bd6203dfa7a9cf81f1ac434b6ea3611`; the final branch
tip is reported in the handoff together with its remote SHA.

## Replayed history

The six historical pipeline commits were cherry-picked in order:

| Stage | Original commit | Repaired replay |
|---|---|---|
| 5A authority coverage | `3357ce56b445c1d4783d8d5888b31d75052c6d3e` | `5bc715e035612c57e03252f2e7f03c2796d1698c` |
| 5B FC04 migration | `fee9a0ec1348937af853148d95b948e9a0540b24` | `bfee1377750690d200c76c3454596312d0a7ffd5` |
| 5C semantic closure | `4eb8b10364751e4d29243481501c4c72b6def69a` | `969431af1a117b5423eef821eb2bd3b500e32f55` |
| 5D source-research implementation | `4c820ce` | `4429472de51d18b44d36ecf672957f563e04e963` |
| 5D checkpoint | `6bce92a` | `cf6a3def77c1f636e2900ea3912c0aabeefc8d42` |
| 5D final report | `08975f2` | `717468b26ec8d06fb261b128f4b96b742672d053` |

The replay required repair commits because the original generated artifacts
embedded the canonical SHA and claim/reconciliation assumptions from the
wrong lineage. The additional repair commits are `755986d` (5A snapshot),
`fade859` (5B contracts), `6f664ff` (5C contracts), `638b061` (5D contracts),
and `6214202` (single integrated shadow claim projection).

## Conflict and architecture resolution

The three expected 5B content conflicts were resolved semantically:

- `reconciliation/schema.json` retains the strict PIPELINE-4A decision,
  property-support, packed-field and review contract. It now also accepts the
  5C `classified` status while retaining all 4A statuses and requirements.
- `sources/claims/schema.json` remains the generic property-level claims
  schema. It accepts both the 4A source-registry reference string and the
  5B/5D source-array projection, plus evidence grades and property-level source
  hashes. No weaker parallel claims schema replaced it.
- The accepted 4A cloud-oracle evidence was retained; the 5B replay added no
  duplicate or conflicting oracle record.
- `sources/manifest.json` is the semantic union. The only manifest addition is
  the 5D evidence pattern; the source registry now contains 20 unique source
  IDs, including the bounded 5B and 5D projections.

The 5B and 5D scoped claims are explicitly included by
`tools/build_generic_claims.py` in `sources/claims/generic-claims.json`.
Consequently the existing reconciliation builder can validate all stage
references through one claim model. The combined shadow contains 4,762
generic claims and 725 decisions; the canonical reconciliation remains a
shadow-only artifact.

The 5B physical-decision builder was also corrected to reference the logical
source claim rather than a reconciliation decision ID. 5D reconciliation
support was normalized to claim arrays, contradiction strings were retained as
structured conflicts, and the 4A review/rationale contract was preserved.

## Stage results on the repaired base

### PIPELINE-5A

The repaired authority snapshot is generated against the 4A canonical output:

- 4,048 canonical records and 1,791 distinct bus physical units;
- 49,867 canonical property cells;
- 49,632 legacy-authoritative cells (99.53%);
- 41 legacy-exclusive cells;
- 18 declarative diagnostic targets.

These are not semantic edits to the canonical spec; they are the authority
inventory of the accepted 4A tree.

### PIPELINE-5B

The bounded MIN/TL-XH FC04 input cohort remains unchanged in scope:

- 250 physical addresses (`I3000`–`I3249`), with 250/250 physical parity;
- 180 logical source decisions;
- 447 source claims;
- 121 exact source-name matches;
- 129 explicitly unresolved semantic parity items.

The repaired artifact now validates against the 4A reconciliation and claims
schemas without weakening either schema.

### PIPELINE-5C

All 129 5B unresolved targets remain covered exactly once:

- 3 `EXISTING_EVIDENCE_SUFFICIENT`;
- 54 `COUNTER_AVOID_ACTIVE_INJECTION`;
- 4 `DERIVED_OR_AGGREGATE`;
- 17 `SOURCE_RESEARCH_CANDIDATE`;
- 51 `INSUFFICIENT_EVIDENCE`.

No new live experiment, response injection, inverter write or canonical change
was introduced.

### PIPELINE-5D

All 17 source-research candidates remain covered at property level:

- 14 `FULLY_RESOLVED_AT_PROTOCOL_ROLE_SCOPE`;
- 3 `PARTIALLY_RESOLVED`;
- 137 claims and 137 reconciliation decisions;
- 69 source-supported property findings.

The 5D canonical parity target was regenerated from the repaired 4A/5C tree:

`e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`

The source-research conclusions are unchanged. Canonical generator authority
was not cut over.

## Canonical and safety invariants

The canonical specification is byte-identical to the accepted 4A start:

`spec/growatt-register-spec.json` SHA-256:
`e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`

No HA, broker, inverter, runtime or production configuration was changed.
No token, private cloud identifier or write capability was introduced. All
5B–5D artifacts continue to declare `canonical_modified: false`; the 5C/5D
safety boundaries remain no-experiment and no-inverter-write boundaries.

## Validation

The following checks pass on the repaired branch:

```text
python3 tools/validate_authority_coverage.py
python3 tools/validate_fc04_migration.py
python3 tools/validate_fc04_closure.py
python3 tools/validate_fc04_source_research.py
python3 tools/validate_reconciliation.py
python3 tools/validate_claims.py
python3 -m pytest -q
```

The generated 5B, 5C and 5D claims/reconciliation artifacts also pass the
merged JSON Schemas. No `git clean`, force-push, merge, canonical rewrite or
second worktree was used.

## Follow-up

This repair is ready for review and for a later controlled merge decision. The
remaining semantic gaps and the still-large legacy authority surface remain
explicit. This task does not start HA-GII-5 or perform a canonical generator
cutover.
