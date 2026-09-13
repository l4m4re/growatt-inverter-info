# GII-PIPELINE-2 — Vendor PDF source claims

## Disposition

`GII_PIPELINE_VENDOR_EXTRACTION_ACCEPTED_WITH_FOLLOW_UP`

This phase adds a public-safe, provenance-rich transcription layer for the
three explicitly identified Growatt protocol documents. It does not alter the
canonical GII specification, Home Assistant, the broker, the inverter, or
production configuration. The old flat V1.24 derivative remains in place as a
migration/comparison baseline.

Starting point: `audit/gii-pipeline-1-20260913` at
`f6106ad9156010e87ea275de33398aa6d6bd95cc`.

## Corpus inventory

| Document ID | Title / revision | Date | SHA-256 | Pages | Claim artifact |
|---|---|---|---|---:|---|
| `vendor_growatt_v305_2013` | Growatt PV Inverter Modbus RS485 RTU Protocol, V3.05 | 2013-04-25 | `dcdedc30edc61178de53b661a4087de6b20091864ddcd0187269c948ca0b05bc` | 15 | `sources/claims/vendor/vendor_growatt_v305_2013.json` |
| `vendor_growatt_v314_2016` | Growatt PV Inverter Modbus RS485 RTU Protocol, V3.14 | 2016-09-27 | `599cb825d3e8f83f88043b41a144d8b4f4d1f5697c7e30f2041e9f9080b00006` | 32 | `sources/claims/vendor/vendor_growatt_v314_2016.json` |
| `vendor_growatt_v124_2020` | Growatt Inverter Modbus RTU Protocol, V1.24 | first visible change record 2020-04-28 | `fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320` | 85 | `sources/claims/vendor/vendor_growatt_v124_2020.json` |

The V3.05 file is recorded conservatively as a user-retained Growatt website
download with unknown/unretained original URL. The V3.14 and V1.24 files are
user-retained vendor PDFs in the HA workspace. The originals are local-only;
only metadata and structured claims are committed.

Adjacent copies in external research checkouts were not silently promoted to
additional canonical documents. Their differing hashes remain a future
corpus-review input.

The machine-readable inventory is
`sources/claims/vendor/document-inventory.json`; the same source identities
and hashes are also recorded in `sources/manifest.json`.

## Extraction method

The extractor uses embedded PDF text with Poppler layout preservation:

```text
pdftotext 25.03.0 -layout -enc UTF-8
pdfinfo    25.03.0
pdftoppm  25.03.0 (used for visual review, temporary files only)
```

No OCR was needed for these three documents. The generic bulk pass collects
raw page lines, detects holding/input table context, keeps section headings,
and parses only safe simple numeric addresses. Ranges, algebraic expressions
and suspicious layout fragments remain unparsed with diagnostics.

The parser is intentionally not treated as the authority for pathological
table geometry. `sources/claims/vendor/reviews/` contains explicit
visual-review sidecars for the difficult V1.24 rows. The extractor merges
those sidecars deterministically and marks the resulting claims with
`source_kind: manual_original_document_verified` and
`extraction_method: native_text+agent_visual_review`.

This preserves both visible/literal wording and reviewed reconstruction. For
example, I3165 retains `BDCDeratingMo de` in `raw_variable` and
`BDCDeratingMode` in `reconstructed_variable`; this is not canonical
normalization.

Reproducible commands, with the local PDF paths substituted as necessary:

```bash
python3 tools/extract_vendor_pdf.py \
  --pdf "1KW-50KW Modbus RS485 RTU Protocol.pdf" \
  --expected-sha256 dcdedc30edc61178de53b661a4087de6b20091864ddcd0187269c948ca0b05bc \
  --document-id vendor_growatt_v305_2013 \
  --family-scope "1KW-50KW Growatt PV inverter protocol" \
  --profile sources/vendor/profiles/vendor_growatt_v305_2013.json \
  --output vendor_growatt_v305_2013.json

python3 tools/extract_vendor_pdf.py \
  --pdf Growatt-PV-Inverter-Modbus-RS485-RTU-Protocol-V3-14.pdf \
  --expected-sha256 599cb825d3e8f83f88043b41a144d8b4f4d1f5697c7e30f2041e9f9080b00006 \
  --document-id vendor_growatt_v314_2016 \
  --family-scope "Growatt PV inverter families listed in the document" \
  --profile sources/vendor/profiles/vendor_growatt_v314_2016.json \
  --output vendor_growatt_v314_2016.json

python3 tools/extract_vendor_pdf.py \
  --pdf Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf \
  --expected-sha256 fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320 \
  --document-id vendor_growatt_v124_2020 \
  --family-scope "MIN/TL-X/TL-XH; TL3-X; MAX; MOD TL3-XH; MIX; SPA; SPH as listed by the document" \
  --profile sources/vendor/profiles/vendor_growatt_v124_2020.json \
  --review sources/claims/vendor/reviews/vendor_growatt_v124_2020.json \
  --output vendor_growatt_v124_2020.json
```

## Claim model and difficult rows

Every claim retains document identity, SHA-256, revision, page/page-end,
section/table, family scope, source row identity, all raw source columns,
reconstructed text where applicable, extraction method/confidence, status,
fragments and diagnostics. A continuation is one logical claim with explicit
page fragments and resolvable continuation references.

The manually reviewed V1.24 golden cases establish:

* I3000 across pages 70–71;
* I3104 and the sparse/ambiguous I3110/I3111 PresentFFT context on page 75;
* I3165 across pages 77–78, including the complete visible 0–29 codebook;
* packed I3166 on page 78;
* I3211 across pages 80–81, including bits 0, 1, 2, 8 and 9;
* I3212 on page 81.

The source claim says what the vendor document says. It does not assign
semantic keys, choose a revision, or apply the existing canonical enum/
bitfield overrides. In particular, I3111 remains a bitfield-labelled source
claim with no invented bit meanings.

Duplicate numeric addresses are never merged merely because table and address
match; section/document claim identity remains separate. Ambiguous expressions
such as the V1.24 layout fragments around `3165-3 166` remain unparsed and are
diagnosed rather than coerced to a number.

## Run results

| Revision | Pages | Claims | Continuation fragments | Ambiguous addresses | Manual visual claims |
|---|---:|---:|---:|---:|---:|
| V3.05 | 15 | 154 | 5 | 9 | 0 |
| V3.14 | 32 | 482 | 12 | 44 | 0 |
| V1.24 | 85 | 1501 | 36 | 81 | 8 |

The V1.24 artifact contains 602 holding-table and 899 input-table claims
(including reviewed source claims). The old derivative contains 582 and 875
rows; the difference is a source-model/extraction difference, not a canonical
register-count assertion.

V1.24 diagnostic counts include 156 blank-variable claims, 772 internal split
word candidates, 52 suspicious layout addresses, 27 unparsed addresses, 125
enum/bitfield candidates and 32 page-spanning claims. These are visible review
signals, not silently repaired semantics. V3.05 and V3.14 have analogous
diagnostics recorded in their extraction metadata.

## Comparisons

The historical flat derivative comparison is retained in:

* `sources/claims/vendor/comparisons/v124-vs-historical.json`
* `docs/architecture/GII-PIPELINE-2_V124_HISTORICAL_COMPARISON.md`

It reports 1,457 old rows and 1,501 new claims with these descriptive
classifications:

```text
same                             63
reconstructed_word_split        269
new_continuation_recovered       14
content_changed_or_layout_shift 632
old_row_ambiguous               479
```

These counts are migration signals. They do not claim that every textual
difference is a semantic difference.

Independent cross-document comparison is in
`sources/claims/vendor/comparisons/cross-document.json`: 342 address/table
overlaps were found and retained as `identical_claim`,
`wording_or_layout_difference` or `apparent_unresolved_difference`. No winner
or `supersedes` relationship is inferred. Revision relationships and family
scope reconciliation are PIPELINE-3/4 work.

## Validation and tests

```bash
python3 tools/validate_vendor_claims.py \
  --claims sources/claims/vendor/vendor_growatt_v305_2013.json \
  --claims sources/claims/vendor/vendor_growatt_v314_2016.json \
  --claims sources/claims/vendor/vendor_growatt_v124_2020.json
python3 -m pytest -q tests/test_vendor_pdf_extraction.py
```

The validator checks the shared JSON Schema, stable document hashes, table
namespaces, required raw fields, unique claim IDs, document consistency and
continuation references. The tests cover hash mismatch, all reviewed golden
cases, duplicate separation, malformed-address safety, deterministic
comparison, and validator failures for duplicate IDs/broken continuations.

## Known limitations and PIPELINE-3 inputs

The embedded text column parser still reports many internal word splits and
some blank variable cells in ordinary rows. These are retained as diagnostics;
they are not a reason to invent values. A later pass can add more explicit
visual-review claims for rows selected by the golden audit or by reconciliation
need. Family applicability is currently document/table scope wording, not a
canonical family decision.

PIPELINE-3 should consume these claims to move reviewed source assertions into
declarative reconciliation, compare the three documents by family scope and
physical register identity, and only then make canonical semantic decisions.
No such migration is performed here.
