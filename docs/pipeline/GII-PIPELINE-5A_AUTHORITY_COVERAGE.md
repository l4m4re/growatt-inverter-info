# GII-PIPELINE-5A: canonical authority coverage

Final disposition:

`GII_PIPELINE_AUTHORITY_COVERAGE_ACCEPTED_WITH_FOLLOW_UP`

The current canonical authority surface is quantitatively inventoried and a
bounded migration path is defined. Follow-up remains because the reviewed
PIPELINE-4A declarative layer is not merged into `main`, and most property
authority is still supplied by the compatibility/legacy path.

This task does not cut over canonical generation and does not change any
register semantics, Home Assistant code, broker behavior, hardware or
production configuration.

## Repaired lineage metadata

| Item | Value |
|---|---|
| Repair branch | `repair/gii-pipeline-5a-5d-lineage-20260913` |
| Accepted base | `8ceb8cd94f50235af4fc10b44ad8cbb355919518` (PIPELINE-4A) |
| Original stage commit | `3357ce56b445c1d4783d8d5888b31d75052c6d3e` |
| Replayed stage commit | `5bc715e035612c57e03252f2e7f03c2796d1698c` |
| Repaired artifact commit | `755986d03f74cc4fdebe30f7a91a4d6d384c73fc` |
| Canonical modified | `false` |

## Starting point

| Item | Value |
| --- | --- |
| Starting branch | `repair/gii-pipeline-5a-5d-lineage-20260913` |
| Starting SHA | `8ceb8cd94f50235af4fc10b44ad8cbb355919518` |
| Canonical artifact | `spec/growatt-register-spec.json` |
| Canonical SHA-256 | `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` |
| Declarative diagnostic reference | `8ceb8cd94f50235af4fc10b44ad8cbb355919518` |
| Working tree | clean at start |

The repaired branch contains the reviewed 4A declarative source and keeps it
non-authoritative for the canonical generator. A future migration must still
promote it only through the reviewed authority gates.

## Authority diagram

Target architecture:

```text
vendor / implementation / live evidence
                 |
                 v
        generic source claims
                 |
                 v
 declarative reconciliation + provenance
                 |
                 v
 validated pure expansion / serialization
                 |
                 v
       canonical JSON + Markdown
```

Current bypasses:

```text
source graph -> consolidated audit -> build_resolved_register_reference.py
                                      -> compatibility JSON
                                      -> build_register_spec.py -> canonical

build_register_spec.py also contains register-specific Python mappings,
overrides, fallback semantic rules and policy rules.
```

The compatibility JSON and Python mappings are useful migration evidence, but
they must not remain independent semantic authorities after the eventual
cutover.

## Starting-gate validation

Canonical validation was run successfully before inventory generation:

```text
python3 tools/validate_resolved_register_reference.py
ok: true, records: 4048, write_verified: 0

python3 tools/validate_register_spec.py
ok: true, records: 4048, unique_semantics: 978, runtime_unique_findings: 22, human_docs: 11
```

The canonical file was not rewritten. Its starting SHA-256 is retained above
and the final canonical SHA-256 is unchanged.

## What the 4,048 records represent

The canonical artifact contains 4,048 family-expanded records:

| Measure | Count |
| --- | ---: |
| Canonical records | 4,048 |
| Holding records | 1,805 |
| Input records | 2,243 |
| Distinct `(family, table, address, length)` targets | 4,048 |
| Distinct bus physical `(table, address, length)` units | 1,791 |
| Distinct `(table, address)` units | 1,790 |
| Distinct semantic concepts | 1,064 |
| Family/semantic assignments with a key | 2,506 |
| Records with an assigned semantic key | 3,471 |
| Generated logical fields | 550 |
| Compatibility records | 4,048 |

Thus `4,048` is not the number of independent bus locations. The useful
physical migration unit is normally a bus unit plus family/scope and semantic
interpretation. There are 1,791 bus-level units, with 1,044 shared by more
than one family and expanded to 3,301 family records. The current expansion
ratio is 2.26 family records per bus unit.

The artifact also retains the explicit family-level identity, so two families
sharing an address are not incorrectly collapsed into one universal semantic
record.

## Declarative coverage

The repaired PIPELINE-4A reconciliation contains 29 decisions:

| Measure | Count |
| --- | ---: |
| Declarative decision records | 29 |
| Physical MODBUS targets | 18 |
| Logical targets | 10 |
| FC0x20 logical target | 1 |
| Matching repaired canonical family records | 18 |

The 18 physical targets are the reviewed MIN/TL-XH subjects at H3036, H3037,
H3046-H3049, H3081-H3082, I3000, I3101, I3110-I3111, I3165-I3166, I3170,
I3211-I3212 and I3217. They are measured as a diagnostic coverage slice, not
as the current canonical authority.

Declarative property coverage below is measured against the 4,048
family-expanded records. A semantic decision can cover several canonical
properties, so these columns intentionally do not sum to a record total.

| Canonical property | Family records covered | Coverage |
| --- | ---: | ---: |
| Physical identity | 0 | 0.00% |
| Length | 0 | 0.00% |
| Signedness | 12 | 0.30% |
| Scale | 0 | 0.00% |
| Unit | 9 | 0.22% |
| Physical quantity | 11 | 0.27% |
| Human description | 9 | 0.22% |
| Enum definitions | 4 | 0.10% |
| Packed/bitfield layout | 3 | 0.07% |
| Access | 0 | 0.00% |
| Model applicability | 0 | 0.00% |
| Aliases | 0 | 0.00% |
| Provenance/support decision | 1 | 0.02% |
| Normalization | 9 | 0.22% |
| Write semantics | 0 | 0.00% |

This is why replacing the current generator with the 18-target layer would
not be a safe cutover.

## Current authority origins

The machine-readable inventory records one entry for every canonical physical
record and property-level origin details. The repaired output has 49,867
non-empty property cells. Of those, 49,632 (99.53%) still involve either a
legacy Python or compatibility-rule origin. Forty-one cells are exclusively
legacy-Python supplied; most other cells combine source/compatibility data
with generator transformations. Unknown origin cells are explicitly counted
as zero by this inventory, but that does not mean their provenance is complete
or that their semantics are declaratively migrated.

The most important current origin classifications are:

| Property | Current origin pattern |
| --- | --- |
| Identity and length | compatibility record plus deterministic generator projection |
| Signedness, scale and unit | compatibility data, with register-specific Python overrides where present |
| Quantity and canonical name | Python rename/fallback/normalization logic plus compatibility fields |
| Enums and packed layouts | source data parsed by Python, with keyed Python overrides for selected records |
| Access and aliases | compatibility record fields |
| Applicability | compatibility/family rules plus source applicability |
| Provenance and resolution | compatibility fields assembled from source/evidence and Python policy |
| Write policy | Python text/policy rules plus compatibility access/name data |
| Logical fields | Python component markers, adjacency and field expansion |

The distinction between “origin known” and “declaratively authoritative” is
deliberate. Existing canonical values are not converted into claims merely
because they are already present.

## Legacy Python inventory

The following paths contribute semantic information today:

| Path/symbols | Classification | Future disposition |
| --- | --- | --- |
| `tools/build_register_spec.py::semantic_quantity`, `canonical_name`, `subsystem`, `instance_metadata`, `logical_fields` | `LEGACY_PYTHON` | Move decisions and data to declarative records; retain only generic expansion/serialization algorithms. |
| `SEMANTIC_RENAMES`, `BITFIELD_OVERRIDES`, `PACKED_FIELD_OVERRIDES`, `ENUM_OVERRIDES`, `NORMALIZED_OVERRIDES` | `LEGACY_PYTHON` | Replace with claim-supported declarative properties and remove the constants. |
| `evidence`, `resolution_from_evidence`, `write_policy` | `MULTIPLE_SOURCES` | Keep generic aggregation; move policy and supported property decisions into explicit data. |
| `tools/generate_consolidated_ref.py` collectors | `DERIVED_GENERATOR` | Retain as source aggregation/intermediate generation, with no hidden precedence. |

Pure generator infrastructure is allowed after cutover. A function is not
pure merely because it emits JSON: a hardcoded register name, scale, enum,
applicability rule or write meaning remains semantic authority.

## Compatibility-semantic inventory

| Layer | Classification | Current role | Required migration action |
| --- | --- | --- | --- |
| `knowledge/audit/consolidated-register-reference.json` | `DERIVED_GENERATOR` | Graph-derived source aggregation and datatype evidence | Retain as source/intermediate material without precedence. |
| `tools/build_resolved_register_reference.py` | `COMPATIBILITY_RULE` | Semantic matching, MIN overlays, resolution, family handling and read-plan policy | Migrate semantic rules; retain only generic compatibility projection/inheritance infrastructure. |
| `knowledge/compatibility/growatt-register-reference.json` | `COMPATIBILITY_RULE` | Expanded 4,048-record compatibility view consumed by the canonical generator | Make downstream-only and generate it from canonical output in the later compatibility phase. |
| `tools/build_register_spec.py` input path | `COMPATIBILITY_RULE` | Reads the compatibility view directly | Remove this dependency before authority cutover. |

The compatibility record count matching the canonical record count does not
prove independence: it is the direct input surface of the current canonical
generator.

## Migration classes

The per-record inventory classifies the current surface as follows:

| Migration class | Family records |
| --- | ---: |
| `PARTIAL_DECLARATIVE` | 18 |
| `COMPATIBILITY_DERIVED` | 1,675 |
| `EVIDENCE_GATED` | 656 |
| `LEGACY_ONLY_COMPLEX` | 494 |
| `SYNTHETIC_OR_GENERATED` | 1,205 |

There are currently no `READY_DECLARATIVE` records. These classes are
migration planning categories, not semantic quality judgements. In
particular, `EVIDENCE_GATED` records must migrate with an explicit unresolved
state rather than being silently promoted.

## Schema-gap analysis

The existing reconciliation schema is useful for reviewed property decisions,
but is not yet a complete declarative model for the canonical product.

| Missing concept | Concrete need | Minimal extension |
| --- | --- | --- |
| Property-level claim support | I3000 and H3082 have several promoted properties with different evidence | Add per-property `decision_id` and `claim_ids`/evidence references. |
| Family/model applicability | H3036 and shared addresses have model/region/protocol scope | Add scoped predicates plus explicit inheritance/override relationships. |
| Logical fields | Multi-word counters and XH schedule slots are not safe adjacency heuristics | Add declarative components, roles, word order and encoding-template references. |
| Normalization transform | H3082 ratio-to-percentage must remain auditable | Add source unit, target unit, operation and factor/offset with support. |
| Generated expansion | One bus unit expands across families and scopes | Add base/family templates and deterministic expansion relationships. |
| Evidence-gated unknowns | Reserved fields and H3036 value `255` must stay unresolved | Require per-property resolution state and unresolved rationale. |

These are the minimum observed gaps; no general-purpose DSL is proposed.

## Migration cohorts

The tool measures bounded cohorts from the actual canonical structure:

| Cohort | Family records | Physical units | Semantic records |
| --- | ---: | ---: | ---: |
| MIN/TL-XH all | 895 | 895 | 760 |
| MIN/TL-XH FC04 input 3000–3249 | 250 | 250 | 234 |
| MIN/TL-XH FC04 input 3000–3124 | 125 | 125 | 120 |
| MIN/TL-XH BMS input 3164–3231 | 68 | 68 | 60 |
| All holding | 1,805 | 665 | 1,623 |
| All input | 2,243 | 1,126 | 1,848 |
| Legacy 3.15/SPF families | 39 | 32 | 39 |
| Structured enum/bitfield/logical records | 1,503 | 594 | 1,416 |

### Recommended first cohort

`min_tl_xh_fc04_input_3000_3249`

This is the recommended next bounded implementation cohort. It contains one
modern V1.24 family and two vendor-native 125-word input pages, with strong
vendor/live evidence and 250 records. It exercises status, enums, packed
fields, BMS semantics, property provenance and family expansion without
requiring migration of every family or all holding controls.

The implementation task should first add explicit claim-backed property
records and logical templates for this cohort, then prove exact parity for
the cohort and no diff elsewhere. It must not use the current canonical JSON
as evidence for new meanings.

## Future cutover criteria

PIPELINE-5 should not be retried until all of the following are machine-checkable:

1. Every emitted canonical property has declarative authority, or is produced
   only by deterministic non-semantic expansion/serialization.
2. `legacy_authoritative_property_cells == 0`; remaining Python and
   compatibility code is demonstrated to be infrastructure only.
3. The canonical generator no longer reads
   `knowledge/compatibility/growatt-register-reference.json`.
4. Full generated output reproduces the retained pre-cutover canonical
   semantics, including unresolved statuses.
5. Two clean generation runs are byte-identical and use no time, locale,
   network, private runtime state or host-specific path.
6. Every supported promoted property has claim/evidence traceability and
   every unresolved property retains its unresolved rationale.
7. A generated-output check fails when a contributor edits the canonical file
   without regenerating from declarative input.

## Tooling and tests

Added:

* `tools/build_authority_coverage.py` — deterministic inventory generator;
* `tools/validate_authority_coverage.py` — stale-output and completeness
  validator;
* `docs/pipeline/data/GII-PIPELINE-5A_AUTHORITY_COVERAGE.json` — generated
  per-record/property coverage matrix;
* `tests/test_authority_coverage.py` — coverage, 18-target recognition and
  deterministic-output regressions.

Validation performed:

```text
python3 tools/build_authority_coverage.py
generated authority coverage: 4048 records, 1791 bus units, 18 declarative targets

python3 tools/validate_authority_coverage.py
valid: canonical authority coverage is current and complete

python3 -m pytest -q tests/test_authority_coverage.py
3 passed
```

The canonical artifact remained byte-identical to the repaired starting SHA. No live
hardware, cloud API, Home Assistant, broker or inverter state was accessed or
changed.

## Remaining risks and follow-up

* The declarative layer is present on this repair branch rather than `main`;
  it remains a reviewed, non-authoritative migration input.
* Property-origin classification is exact for the known generator paths, but
  source-level provenance is not yet uniformly property-granular in the
  canonical schema.
* Compatibility expansion, family inheritance and logical-field generation
  must be represented before shared bus units can be migrated safely.
* `EVIDENCE_GATED` and `UNKNOWN_RESERVED` records must not be converted to
  resolved semantic facts by bulk migration.
* The final cutover still needs a temporary full-output parity fixture and a
  post-cutover generated-file protection check.

No further pipeline stage was started automatically.
