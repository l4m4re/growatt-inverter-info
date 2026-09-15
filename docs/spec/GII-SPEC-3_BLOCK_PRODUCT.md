# GII SPEC-3 — Block-oriented machine specification and human projection

## Disposition

`GII_SPEC3_BLOCK_PRODUCT_ACCEPTED`

This product projection was built on the accepted C2B `main` tip:

- C2B merge/start SHA: `ed9a9dcd29755d8ba068279f0cd1dc2570530b75`
- SPEC-3 branch: `consolidation/gii-spec3-block-product-20260915`
- implementation SHA: recorded after commit in this report

The frozen historical canonical specification remains unchanged and has SHA-256
`e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`.

## Product model

`spec/v2/register-spec-v2.json` is the sole machine-readable V2 product. The
generator constructs one in-memory model and renders both that JSON and all
Markdown projections from it. The hierarchy is:

`source-native blocks → shared consolidated blocks → physical register definitions → applicability paths → family projections`

Register definitions live once in their containing block. Family pages contain
references and filtered projections, not family-expanded copies. Applicability
can select a block or a declared range, but never creates a register.

Source-native provenance retains the vendor block ID, raw heading, page range,
source claim/row references, table, function code and address expression. The
V1.24 declarations are represented generically for every family/table/range
present in the accepted candidate; the active V1.24 projection currently
contains six unique family IDs because two vendor declaration labels resolve to
the same `tl3_max_mid_mac` family identity.

## Reserved and legacy material

The product contains two first-class compact reserved ranges:

- H3115–H3124, explicit vendor reserved range;
- I3281–I3374, vendor-declared range with no individual semantic rows and the
  accepted Shine/runtime all-zero corroboration.

I3250–I3280 is not classified as reserved. Reserved words are not emitted as
active semantic register definitions.

The old canonical specification is retained as explicitly labelled
`legacy_material`, including the 611 historical physical records and 27
logical fields that are not projected into the current block product, plus
historical family/protocol/source context. This is compatibility/provenance
material, not a competing V2 authority. The V1.24 protocol constraints and the
non-V1.24 V3.14/3.15 constraints remain visible in `PROTOCOLS.md`.

## Generated product and metrics

| Metric | Result |
|---|---:|
| Source-native blocks | 15 |
| Shared consolidated blocks | 15 |
| Active block-scoped register definitions | 1,484 |
| Reserved ranges / words | 2 / 104 |
| Applicability declarations / paths | 7 / 39 |
| Active V1.24 family projections | 6 |
| Logical fields | 523 |
| Enum/bitfield/packed fields | 37 |
| Unresolved candidate registers | 117 |
| Conflicts retained in current candidate | 0 |
| Legacy physical records retained explicitly | 611 |
| Legacy logical fields retained explicitly | 27 |

## Generated files

- `spec/v2/register-spec-v2.json`
- `spec/v2/register-spec-v2.schema.json`
- `spec/v2/README.md`
- `spec/v2/BLOCK_INDEX.md`
- `spec/v2/PROTOCOLS.md`
- `spec/v2/SEMANTIC_INDEX.md`
- `spec/v2/blocks/*.md`
- `spec/v2/families/*.md`

The build and validator are `tools/build_register_spec_v2.py` and
`tools/validate_register_spec_v2.py`. Representative checks are in
`tests/test_register_spec_v2.py`, including frozen-canonical preservation,
shared-block identity, reserved-range boundaries, machine/Markdown agreement,
and deterministic generation.

## Validation boundary

The V2 build, schema/custom validator and four focused SPEC-3 tests passed.
No slow, historical, legacy, full-suite, HA-runtime or broker tests were run;
that was intentional for this bounded product-projection task. No HA/runtime
code, canonical legacy JSON, vendor PDF, inverter, broker or production
configuration was changed.
