# Source and evidence corpus

This directory contains the retained inputs used to trace and extend the
current specification.

- `consolidated/register-blocks.json` is the accepted current block model read
  by the product builder.
- `legacy/compatibility-registers.json` preserves the frozen predecessor and
  the legacy/non-V1.24 knowledge carried into the current JSON.
- `vendor/` contains vendor-native block structures and profiles.
- `claims/vendor/` contains structured source rows and their provenance.
- `claims/implementation/`, `external/`, and `runtime/` retain
  implementation and runtime snapshots for correlation.
- `evidence/` contains reviewed, structured evidence records.
- `curated/` contains reviewed source overlays and normalization data.

The root `manifest.json` records source publication and handling policy. Raw
vendor PDFs, firmware, portal exports, and unreviewed live captures are not
redistributed here.

For adding new evidence, recording human review, updating the consolidated
model, and handing an accepted result to Home Assistant, follow
[`../docs/REGISTER_KNOWLEDGE_WORKFLOW.md`](../docs/REGISTER_KNOWLEDGE_WORKFLOW.md).
