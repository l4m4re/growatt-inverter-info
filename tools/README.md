# Tools

## `build_spec.py`

Builds the current register JSON and its single Markdown projection.

- Inputs: `sources/consolidated/register-blocks.json` and
  `sources/legacy/compatibility-registers.json`.
- Outputs: `spec/growatt-register-spec.json` and
  `spec/growatt-register-spec.md`.
- Normal invocation: `python tools/build_spec.py`.
- Optional `--output-dir PATH` writes both generated files to another
  directory for clean rebuild checks.

## `validate_spec.py`

Validates the current JSON against its schema and checks block, applicability,
register, reserved-range, and Markdown coverage invariants.

- Input: `spec/growatt-register-spec.json`.
- Normal invocation: `python tools/validate_spec.py`.
- Optional positional spec path plus `--schema PATH` and `--legacy-source
  PATH` can validate a temporary clean build.

## `extract_vendor_pdf.py`

Optional source utility. It extracts layout-preserving claim rows from a local
vendor PDF; it does not assign semantics or participate in normal product
generation. It requires Poppler's `pdfinfo` and `pdftotext` commands.

- Input: a local PDF provided with `--pdf PATH`.
- Output: a source-claims JSON file provided with `--output PATH`.
- Example: `python tools/extract_vendor_pdf.py --pdf /path/to/manual.pdf --output /tmp/vendor-claims.json`.
