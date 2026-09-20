# Methodology

The published register specification is a reviewed consolidation of vendor
tables and corroborating evidence. The current build starts from retained
source data; it does not replay historical extraction and migration stages.

```text
vendor documents and other retained sources
                    ↓
source-native register blocks
                    ↓
structural normalization
                    ↓
correlation with implementations and runtime evidence
                    ↓
reviewed corrections and conflict resolution
                    ↓
shared consolidated block model
                    ↓
family and model applicability
                    ↓
machine-readable JSON
                    ↓
generated Markdown projection
```

## Current build inputs

- `sources/consolidated/register-blocks.json` contains the accepted reviewed
  block model, including current register rows, applicability, and reserved
  ranges.
- `sources/legacy/compatibility-registers.json` preserves the frozen former
  family-oriented specification. Its retained records and context are
  projected under `legacy_material` so legacy and non-V1.24 knowledge remains
  available without acting as a second current authority.
- `sources/` retains vendor claims, implementation snapshots, runtime
  snapshots, structured evidence, and reviewed overlays used to trace current
  claims.

`python tools/build_spec.py` loads those inputs into one in-memory model and
writes the JSON and Markdown products. `spec/growatt-register-spec.json` is
authoritative; the schema is maintained at
`spec/growatt-register-spec.schema.json`. Run
`python tools/validate_spec.py` to check the schema, cross references, block
identity, reserved ranges, and projection coverage.

## Modelling rules

1. Vendor block structure is the primary structural evidence.
2. Family range declarations are applicability envelopes. They do not prove
   that every address in a range contains a semantic register.
3. Shared layouts are represented once.
4. Family and model applicability references shared blocks.
5. Genuine family differences use overrides instead of duplicated blocks.
6. Source wording is preserved separately from normalized semantics.
7. Other implementations and runtime observations can enrich or corroborate
   vendor documentation; they do not silently replace it.
8. Conflicts and unresolved fields are legitimate states and remain visible.
9. Reviewed corrections can supersede extraction mistakes without rewriting
   retained historical source records.
10. Reserved ranges are represented compactly and are not expanded into
    invented semantic rows.
11. JSON is authoritative. Markdown is generated from the same model.
12. A current build never requires replaying the historical PIPELINE-1 through
    PIPELINE-11 migration sequence.

The accepted access model retains reviewed read/write corrections. A vendor
`W` marker in the V1.24 write-capability column means writable; by itself it
does not establish write-only access. Current retained access conflicts are
zero. Recorded defaults, including H3085 default 1, remain in the machine
specification.

For the practical procedure used when adding new observations, including
portal and Recorder correlations and the hand-off to Home Assistant, see
[`REGISTER_KNOWLEDGE_WORKFLOW.md`](REGISTER_KNOWLEDGE_WORKFLOW.md).

## Historical predecessor

The former family-oriented canonical file was frozen at SHA-256
`e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`. The Git
commit that last changed that file is
`4a404a6eacdd434f376b9c258594ff2f0ea1f16e`. The exact file is retained at
`sources/legacy/compatibility-registers.json`, with the same SHA-256. The
current block product is based on accepted SPEC-3 commit
`743a9a1bef09b07c502e9306882f6c516e233c67`.
