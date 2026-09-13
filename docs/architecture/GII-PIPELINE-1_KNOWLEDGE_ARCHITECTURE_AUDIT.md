# GII-PIPELINE-1 — Knowledge architecture and provenance audit

## Scope and disposition

This is an architecture and provenance audit of the RE-4 tip
`4a404a6eacdd434f376b9c258594ff2f0ea1f16e` (`research/gii-min-re-4-cloud-semantic-oracle-20260913`).
The audit was performed on 2026-09-13. It did not change Home Assistant, the
broker, the inverter, production configuration, or any register semantics.

The current product is useful and already retains materially valuable vendor,
implementation, runtime and live/cloud evidence. It is not yet a fully
reproducible claim-level knowledge pipeline. The principal follow-ups are to
repair the vendor extraction, move register-specific decisions out of Python,
and make the canonical build independent of the compatibility projection.

**Final disposition: `GII_PIPELINE_ARCHITECTURE_ACCEPTED_WITH_FOLLOW_UP`**

## 1. Current real data flow

The README describes the following route, which is substantially correct but
omits the semantic authority hidden in the final builder and the extra
model-specific inputs:

```text
sources/vendor/growatt-v1.24-tables.json
sources/curated/*
sources/external/*snapshot.json
sources/runtime/ha-local-registers.snapshot.json
sources/evidence/*
        │
        ├── tools/build_register_graph.py
        │       └── knowledge/graph/register-graph.gpickle
        │
        └── [legacy direct-source path, diagnostic only]

knowledge/graph/register-graph.gpickle
        │
        └── tools/generate_consolidated_ref.py
                └── knowledge/audit/consolidated-register-reference.json

knowledge/audit/consolidated-register-reference.json
        + sources/evidence/min-6000tl-xh-*.json
        + external/runtime overlays and policy in Python
        │
        └── tools/build_resolved_register_reference.py
                └── knowledge/compatibility/
                    growatt-register-reference.json
                    GROWATT_REGISTER_REFERENCE.md

knowledge/compatibility/growatt-register-reference.json
        + sources/evidence/min-6000tl-xh-block-validation.json
        + register-specific overrides in Python
        │
        └── tools/build_register_spec.py
                ├── spec/growatt-register-spec.json
                ├── spec/README.md
                ├── spec/PROTOCOLS.md
                ├── spec/SEMANTIC_INDEX.md
                └── spec/families/*.md

spec/growatt-register-spec.json
        └── tools/build_min_tlxh_audit_matrix.py
                └── docs/reverse-engineering/GII-2_MIN_TL_XH_AUDIT_MATRIX.md
```

The first important architectural fact is that the current implementation is
not actually `sources → canonical spec → compatibility`. The final builder
sets `SOURCE_PATH` to
`knowledge/compatibility/growatt-register-reference.json`; therefore the
compatibility representation is a required semantic input to the current
canonical product. The generated compatibility metadata correctly says that
it is non-canonical, but the build dependency points in the opposite
direction.

The graph has useful source payloads and conflict information, but its primary
register nodes are keyed by `register:<table>:<address>`. Vendor payloads from
different rows are attached under broad source buckets such as `vendor`, not
as durable source-claim identities. The graph therefore improves retention
over the older flat merge without yet providing claim-level provenance.

## 2. Intended architecture

```text
retained source claims
  vendor PDF extraction + manual PDF verification
  curated interpretations
  external implementations
  HA/runtime snapshots
  physical/live/cloud evidence
        │
        ├── extraction and claim validation
        ├── scope-aware reconciliation
        └── reviewed declarative decisions
                │
                ▼
        canonical register specification
          physical identity
          semantic identity
          decoding and transport
          assertions, conflicts, evidence
                │
        ┌───────┼────────┬─────────────┐
        ▼       ▼        ▼             ▼
     human    HA       compatibility  other
     docs     adapter   projections    consumers
```

The canonical artifact must be project-independent. HA metadata and code can
be evidence and a consumer contract, but neither should be able to define
canonical meaning merely by being the easiest input to a builder.

## 3. Where semantic facts are currently created, changed, or lost

| Stage | Current behavior | Audit consequence |
|---|---|---|
| Vendor JSON | Stores 582 holding and 875 input rows with page and text columns | Useful baseline, but no document/section/claim identity or extraction method |
| `build_register_graph.py` | Parses ranges, creates `(table,address)` nodes, merges payloads, synthesizes datatype nodes and links families/blocks | Numeric identity is retained; row-level context and competing claims are compressed into graph attributes |
| `generate_consolidated_ref.py` | Normalizes text, parses ranges, expands inclusive ranges, and emits source summaries, alternatives and conflicts | Raw register expressions and some row context are not preserved in the emitted summary; heuristic digit parsing can turn malformed input into a misleading address |
| `build_resolved_register_reference.py` | Applies MIN family maps, semantic review, live/block evidence and cloud validation, then classifies records | Important reviewed knowledge is retained, but mainly as record-level provenance and fixed policy branches |
| `build_register_spec.py` | Maps names to semantic keys, applies enums/bitfields/packed fields/signedness and emits canonical JSON and Markdown | A substantial amount of Growatt domain knowledge is executable Python rather than source claims or declarative reconciliation |
| Human docs and audit matrix | Generated from the spec | Correctly downstream, but cannot show claim-level “why this field/scale/label” provenance yet |

Known good evidence is not absent. The current spec already retains the RE-4
cloud/Shine observations, including I3110, I3111, I3165, I3166, I3211 and
I3212, and the accepted I3170/I3101 signedness corrections. The issue is that
the route by which those facts become assertions is not yet transparent or
uniform.

## 4. Domain knowledge embedded in generator code

`tools/build_register_spec.py` contains the following classes of
register-specific knowledge:

* `SEMANTIC_RENAMES` maps source-shaped names such as `battery_current`,
  `bdc_derating_mode` and `grid_import_power` to stable semantic namespaces.
* `CANONICAL_NAME_ALIASES` repairs known source spellings and malformed names.
* `BITFIELD_OVERRIDES` defines concrete meanings for MIN/TL-XH addresses such
  as holding 1 and input 3104, 3187 and 3211.
* `PACKED_FIELD_OVERRIDES` defines the packed layouts for input 3000 and 3166
  and holding schedule/date words.
* `ENUM_OVERRIDES` contains domain codebooks, including input 3165's complete
  BDC derating codebook and input 3212's BMS status enum.
* `NORMALIZED_OVERRIDES` forces particular raw types and decoding properties.
* `build()` contains evidence-backed signedness and semantic decisions for
  I3170, I3101 and I3217, as well as source/evidence policy.
* The resolved builder also contains model-specific classification and
  overlay policy; `build_register_data_types.py` remains a curated datatype
  source in the source catalog.

The first two items are mostly generic normalization policy, although their
mapping tables contain domain vocabulary. The bitfield, packed-field, enum,
per-register datatype and signedness entries are domain facts. For example,
`(min_tl_xh, input, 3165)` is not a generic algorithm. It is a reviewed
assertion about Growatt firmware and must be inspectable as data.

### Recommended replacement

Introduce a public-safe declarative reconciliation area, for example:

```text
sources/reconciliation/
  semantic-aliases.json
  min-tl-xh-register-decisions.json
  protocol-decisions.json
```

A decision record should contain at least:

```yaml
physical_id: min_tl_xh:input:3165
canonical:
  semantic_key: bdc.derating_mode
  canonical_name: BDC derating mode
  raw_type: u16 enum
  signed: false
  scale: 1
claims:
  - vendor_v124_pdf_verified:i3165
  - min_cloud_oracle:i3165
decision:
  status: resolved_with_notes
  confidence: high
  rationale: ...
```

The builder may retain generic schema validation, sorting and normalization
algorithms, but should load this data and report unknown or duplicate decision
keys. Temporary migration overrides should be explicitly labelled and have a
removal issue/phase rather than silently becoming permanent policy.

## 5. Vendor PDF extraction audit

### Source verification

The original vendor PDF was not modified. Its SHA-256 was checked against
`sources/manifest.json`:

```text
fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320
```

The source is retained as metadata/local-only material according to the
manifest; the public GII repository retains the structured derivative and
source metadata rather than publishing the PDF.

Extraction tooling used for this audit:

```text
pdftotext 25.03.0
pdfinfo   25.03.0
pdftoppm  25.03.0
```

Commands and temporary outputs:

```bash
pdftotext -layout <V1.24.pdf> /tmp/gii-pipeline-1/v124-layout.txt
pdftotext -raw    <V1.24.pdf> /tmp/gii-pipeline-1/v124-raw.txt
pdftoppm -f 77 -l 81 -png -r 120 <V1.24.pdf> /tmp/gii-pipeline-1/render/suspect
```

The temporary files and rendered pages are outside Git. `qpdf`, MuPDF and
PyMuPDF were not required for this audit and were not installed. Embedded
text was usable, so OCR was not treated as an authority or applied to the
whole document.

### Findings

The retained JSON was introduced in commit `8489cc2` as a 16,033-line
history-filtered extraction. Repository history and the current `tools/`
tree do not retain a reproducible PDF-to-JSON extraction command. Existing
extractors are overlays for HA or third-party implementations, not a complete
vendor-PDF extractor.

The JSON contains:

```text
holding: 582 rows, pages 9–47
input:   875 rows, pages 47–83
```

Measured quality signals include 23 empty holding variable names, 89 empty
input variable names, 52 holding register expressions containing range or
algebraic punctuation, 323 holding variable values with internal spaces and
160 input variable values with internal spaces. These are review signals, not
automatic proof that every row is wrong.

The original rendered pages establish the following concrete discrepancies:

* **I3165:** page 77 begins the `BDCDeratingMode` cell with values 0–4;
  page 78 continues it with values 5, 6, reserved 7–15, and 16–24, with
  reserved 25–29. The retained vendor JSON ends at the first 0–4 segment.
  The canonical complete enum is therefore currently supplied by manual
  review/code rather than reproducibly by the retained vendor extraction.
* **I3211:** the `BattNeedCharge RequestFlag` cell starts on page 80 and
  continues on page 81. Its bit descriptions are visibly wrapped and split
  across the page boundary. A row parser that treats a page as a record can
  truncate the bitfield.
* **I3111:** the original row visibly contains the split rendering
  `uwPresentFFTVa lue [CHANNEL_A]`; the source datatype column says
  `bitfield` but supplies no bit definitions. This must remain a raw source
  claim plus a separate canonical “unsigned diagnostic word” assertion.
* **Repeated addresses/context:** the PDF contains repeated numeric addresses
  in different table/family contexts. Pages 42 and 55/75 also show that
  similarly named PresentFFT/module fields occur in different sections. A
  number alone is not a source-claim identity.
* **Malformed ranges:** expressions such as `3165-3 166` and
  `3212-3 213` are mechanical layout/extraction failures or ambiguous range
  renderings. The current parser may extract digits heuristically; algebraic
  expressions are deliberately left without a numeric address in some paths.
  Both behaviors need explicit diagnostics rather than silent interpretation.

Native `pdftotext -layout`, `pdftotext -raw` and rendered-page inspection
agree on the substantive I3165/I3166/I3211 content, while disagreeing in
spacing, cell wrapping and continuation layout. This is precisely a signal to
retain geometry/continuation metadata, not to choose the cleanest-looking
text stream and discard the other representation.

### Required extraction design

Use embedded text first, then layout/geometry-aware table extraction for
suspect pages, with OCR only for a demonstrably unreadable region. Preserve
both literal and reconstructed forms. A future extraction tool should accept
the local PDF and expected SHA-256, for example:

```bash
python tools/extract_vendor_pdf.py \
  --pdf /local/path/vendor-v1.24.pdf \
  --expected-sha256 fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320
```

The tool should emit source claims, not prematurely canonical registers, and
should fail or warn on page-continuation and suspicious-address conditions.

## 6. Source-claim model

The current row shape (`register`, `variable`, `description`, access/value/
unit/initial/note/page) is a useful compatibility input but insufficient as
an auditable claim. The target source-claim record is:

```json
{
  "claim_id": "vendor_v124_pdf:p78:input:i3165:continuation-1",
  "document_id": "growatt_modbus_v1_24_english",
  "document_revision": "V1.24",
  "source_kind": "vendor_pdf_extraction",
  "document_sha256": "...",
  "page": 78,
  "section_id": "tl_x_tl_xh_battery_telemetry",
  "section_title": "TL-X/TL-XH battery telemetry",
  "family_scope": ["TL-X", "TL-XH", "TL-XH-US", "MIN"],
  "table": "input",
  "source_row_id": "p78-row-3165",
  "raw_address_expression": "3165",
  "address": 3165,
  "raw_variable": "BDCDeratingMo\nde",
  "raw_description": "...",
  "raw_value_text": "5: High temperature ... 24: ...",
  "raw_unit_text": "",
  "raw_access_text": "",
  "raw_note": "",
  "extraction_method": "embedded_text+layout_review",
  "extraction_confidence": "high",
  "source_status": "literal_with_continuation"
}
```

The exact source wording must remain available, including mechanical spaces
and unreadable/ambiguous flags. A later normalized field can say
`BDCDeratingMode` and `BDC derating mode` without overwriting the literal
claim.

## 7. Canonical assertions and claim-level provenance

A canonical physical record should retain physical identity
`family + table + address`, while each important property points to the
claims/evidence that justify it:

```json
{
  "physical_id": "min_tl_xh:input:3165",
  "scope": {"family": ["min_tl_xh"], "protocol": ["v1.24"]},
  "semantic_key": "bdc.derating_mode",
  "canonical_name": "BDC derating mode",
  "encoding": "u16_enum",
  "assertions": {
    "address": {"value": 3165, "claim_refs": ["vendor_v124_pdf:p77-row-3165"]},
    "enum_values": {"value": "...", "claim_refs": ["vendor_v124_pdf:p77-row-3165", "vendor_v124_pdf:p78-row-3165", "min_cloud_oracle:i3165"]},
    "semantic_key": {"value": "bdc.derating_mode", "claim_refs": ["min_cloud_oracle:i3165", "grott:i3165"], "review_ref": "reconciliation:min_tlxh:i3165"}
  },
  "conflicts": [],
  "alternatives": [],
  "resolution": {"status": "resolved_with_notes", "confidence": "high"}
}
```

This handles the current examples correctly: I3165's machine extraction is
incomplete, manual original-PDF verification supplies the continuation, and
cloud injection correlates the physical word with `bdc_derate_reason`. They
are three distinct evidence items, not one overwritten source field. The
same model can retain I3111's vendor “bitfield” notation separately from the
canonical raw-unsigned diagnostic interpretation and provisional cloud
correlation.

## 8. Evidence vocabulary and reconciliation

The current vocabulary is a good start (`source_documented`,
`implementation_correlated`, `read_observed`, `value_plausible`,
`semantic_verified`, `write_accepted`, `write_reversible`,
`behavior_verified`), but it needs explicit contracts and more precise names.
The target vocabulary should distinguish at least:

```text
vendor_documented
external_implementation_observed
runtime_consumer_observed
physical_read_observed
physical_value_plausible
cloud_correlated
semantic_behavior_verified
manual_original_document_verified
write_observed
write_accepted
write_reversible
```

“Source says X”, “hardware returned X”, “changing X caused Y” and “cloud
field X changed to Y” must never be represented by one generic confidence
flag. The current validators correctly prevent unsupported
`semantic_verified` claims and retain `write_verified = 0`; that policy must
remain intact during migration.

Reconciliation should be scope-aware and evidence-weighted, not “vendor
always wins”. Vendor material can be incomplete or model-specific; external
projects can copy one another; firmware can supersede a document. Preserve
unresolved conflicts and alternatives, including the source, scope and
property in conflict. A source precedence rule may be used as a tie-breaker,
but not as silent overwrite policy.

## 9. Scope, identity, namespaces and names

* Physical identity remains `(family, table, address)`. Holding and input
  spaces never merge merely because the number is equal.
* Semantic identity remains independent. Multiple physical records may share
  a semantic key, and one physical word may contain multiple packed fields.
* Scope must be first-class on claims and assertions: family, model, firmware
  where known, protocol revision, hardware variant, region where relevant,
  table and proprietary namespace.
* `GROWATT_FC0x20` must be represented as a proprietary namespace with
  function code, addressing/payload schema and evidence, not as an FC03/FC04
  register. The model should allow future proprietary namespaces without
  polluting ordinary register identity.
* Naming needs four layers: literal `raw_name`, GII `canonical_name`, stable
  `semantic_key`, and consumer presentation name. Consumer names/entity IDs
  must not silently become canonical semantics.

## 10. Schema review

`spec/growatt-register-spec.schema.json` currently validates the 4048-record
canonical shape and covers physical identity, normalized decoding, semantic
identity, enums, bitfields, relationships, resolution, evidence, write
policy, logical fields and native read blocks. It does not yet formally
express the following adequately:

1. claim IDs and per-property claim references;
2. document revision, SHA, section and source-row location;
3. manual verification as a typed source claim;
4. full model/firmware/protocol/hardware scope dimensions;
5. structured contradictory assertions and alternative candidates;
6. confidence/status per assertion rather than mainly per record;
7. raw versus normalized enum/bitfield labels;
8. typed cloud/API mappings and their observation times;
9. a proprietary namespace and FC20 payload model.

The minimal schema evolution is to add reusable `source_claim`, `scope`,
`assertion`, `claim_ref`, `conflict` and `namespace` definitions, then add
`claims`, `assertions`, `scope` and `conflicts` to canonical records and
logical fields. Do not make every historical optional field required in one
release. The existing compatibility schema should remain a separate legacy
projection schema.

## 11. Reproducibility and CI

The JSON generators sort many records and collections deterministically, and
the validators deliberately ignore generated timestamps for some checks. The
pipeline is not byte-for-byte reproducible today because
`generate_consolidated_ref.py` and `build_resolved_register_reference.py`
write `datetime.now(...).isoformat()` into generated metadata. More
importantly, the PDF-to-JSON step is not retained as a reproducible tool.

The target build should:

1. record input paths, expected SHA-256, extraction tool/version and claim
   schema in the manifest;
2. use stable ordering and either remove generated timestamps or make them an
   explicitly ignored metadata field;
3. provide `build-all`, `validate-all` and `--check`/dry-run modes;
4. rebuild into a temporary directory and fail CI if tracked generated files
   differ, except an explicitly allowlisted provenance timestamp;
5. validate that compatibility is not read by the canonical builder;
6. detect duplicated decision keys, missing claim references and undeclared
   source files.

Semantic graph comparisons may remain useful for a NetworkX intermediate, but
they should not be the only reproducibility test for the public JSON product.

## 12. Extraction validators and golden set

PIPELINE-2 should add diagnostics for:

* suspicious internal word breaks and empty variables;
* cells ending in a partial enum/bitfield;
* unbalanced bit ranges and continuation rows;
* duplicate numeric addresses in distinct sections;
* missing page/table/family context;
* algebraic/range expressions reduced to one address;
* apparent unit/value column swaps and impossible access values;
* rows split over page boundaries;
* repeated holding/input addresses that must remain separate.

The bounded manually checked golden set should include:

```text
V1.24 pages 42, 44–45: repeated/odd range and module rows
page 55: legacy PresentFFT rows 239/240
page 75: I3101, I3104, I3110, I3111
pages 77–78: I3165 continuation and I3166 packed word
pages 80–81: I3211 continuation and I3212 enum
one multi-register scalar and one explicit range
one non-MIN family section
```

Each golden case should store the expected structured source claim, source
location, extraction method and a rendered-page review note. The acceptance
criterion is fidelity to the visible logical table, not the apparent
cleanliness of OCR or a text stream.

## 13. Compatibility and generated documentation

`knowledge/compatibility/` should be a strictly downstream generated view
for legacy consumers. It must not be independently edited and must not be an
input to canonical generation after migration. During transition, the
current compatibility input is a bounded migration dependency and should be
labelled as such in CI and documentation.

Human Markdown should remain generated from canonical data. For each useful
record it should show canonical interpretation, raw vendor wording, aliases,
scope, evidence/confidence and conflicts/notes where present. This gives
normal users readable documentation without erasing the source language.

The original vendor PDFs and raw captures remain local-only. Their document
metadata, hashes and safe structured claims may be public according to the
manifest; private HA state, broker configuration, firmware dumps and raw
serial captures must remain excluded.

## 14. Staged migration plan

### PIPELINE-2 — repair vendor extraction

Add a local-PDF extractor using embedded text/layout first, preserve
continuations and raw text, add the golden audit set, and regenerate only the
vendor source derivative after review. Keep the old JSON as a migration
comparison until parity is measured.

### PIPELINE-3 — source claims

Introduce claim schema and source catalog records with document hash, scope,
section, page, raw fields, extraction method and claim IDs. Adapt graph
ingestion to retain claim nodes/edges instead of only source buckets.

### PIPELINE-4 — declarative reconciliation

Move `SEMANTIC_RENAMES`, enum/bitfield/packed overrides, signedness decisions
and reviewed MIN/cloud assertions into versioned reconciliation artifacts.
Leave only generic projection algorithms in Python.

### PIPELINE-5 — canonical-first build

Build canonical records directly from source claims plus reconciliation. Add
reference validation so every important canonical property has a claim or
evidence reference and every assertion has scope.

### PIPELINE-6 — compatibility projection

Generate the old compatibility JSON/Markdown strictly from canonical output.
Freeze its legacy shape, compare it against the migration baseline, and
remove the reverse dependency from `build_register_spec.py`.

### PIPELINE-7 — consumer adapters

Make HA, broker, Grott-like and other consumers consume canonical GII through
explicit adapters. Preserve public HA entity identity/statistical contracts
in the HA adapter; consumer presentation remains downstream metadata.

## 15. Files and bounded implementation impact

Likely files to add or change in later phases:

```text
sources/claims/                         source-claim records
sources/reconciliation/                 reviewed declarative decisions
tools/extract_vendor_pdf.py             reproducible local-PDF extraction
tools/validate_source_claims.py         claim/extraction diagnostics
tools/build_register_graph.py           claim-aware ingestion
tools/build_register_spec.py            generic canonical projection only
spec/growatt-register-spec.schema.json  claim/assertion/scope schema
tools/validate_pipeline.py              build/check orchestration
tests/golden_vendor_pdf/                bounded expected cases
```

Regenerate `knowledge/audit/`, `knowledge/compatibility/`, `spec/` and the
generated Markdown only after each migration phase is reviewed. Historical
legacy scripts under `tools/legacy/` and old `docs/registers/` notes should be
marked archival or removed only after their consumers are confirmed. Do not
delete the 4048-record corpus or the accepted live/cloud evidence.

Main risks are accidental physical-ID changes, loss of raw source wording,
scope broadening from MIN/TL-XH to unrelated families, compatibility drift,
and HA consumer metadata changes. Each phase should compare record counts,
physical IDs, conflict counts, evidence references, generated outputs and
consumer snapshots before promotion.

## 16. Acceptance questions

1. **Where does each canonical semantic fact originate?** — Today this is
   distributed across source payloads, overlays, evidence and generator
   constants; after PIPELINE-3/4 it will be explicit claim/evidence references.
2. **Can the original raw claim be inspected?** — Partly today, because raw
   rows and source snapshots remain; not reliably for every continuation or
   source context. PIPELINE-2/3 closes this gap.
3. **Can poor source English be improved without losing provenance?** — Yes in
   the intended layered naming model; current raw preservation is incomplete
   for some extracted continuations.
4. **Can conflicts coexist without silent overwrite?** — Partly: graph and
   current outputs retain many alternatives/conflicts, but claim/property
   granularity is missing.
5. **Can model-specific knowledge remain model-specific?** — Yes in current
   family overlays and scope policy, but source claims need first-class scope
   to prevent accidental generalization.
6. **Is the canonical artifact independent of HA?** — Conceptually yes and
   the output is project-independent; HA is still an input/evidence path and
   must remain non-authoritative.
7. **Is compatibility downstream only?** — No, not yet: the current spec
   builder reads compatibility. PIPELINE-5/6 must correct this.
8. **Can a clean checkout regenerate canonical artifacts?** — The retained
   JSON pipeline can rebuild with local dependencies, but the original PDF
   extraction cannot currently be reproduced from a retained tool and the
   generated timestamp policy is not byte-stable.
9. **Are register-specific semantics data rather than hidden Python logic?**
   — No, not yet; this is the main PIPELINE-4 follow-up.
10. **Can future consumers use the canonical spec without historical HA
    knowledge?** — The current spec is designed for that and already carries
    useful consumer-neutral fields, but claim-level provenance and a clean
    canonical-first build are still required for trustworthy long-term use.

## 17. Final recommendation

Accept the current architecture as a staged, useful foundation with explicit
follow-up gates. Do not perform a wholesale rewrite in this audit. The next
implementation should repair and test the PDF extraction, then introduce
claim-level provenance and declarative reconciliation before changing the
canonical/compatibility build direction.

**`GII_PIPELINE_ARCHITECTURE_ACCEPTED_WITH_FOLLOW_UP`**
