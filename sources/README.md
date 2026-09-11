# Source corpus

Every retained source is classified in [`manifest.json`](manifest.json).

- `PUBLIC_SAFE`: suitable for the public repository.
- `METADATA_ONLY`: the source itself is not redistributed, but provenance and
  a checksum or descriptive metadata are retained.
- `LOCAL_ONLY`: intentionally excluded from this checkout; use the original
  local research workspace.
- `NEEDS_REVIEW`: do not publish or use as an authority until reviewed.

Vendor PDFs, firmware, portal exports, raw serial captures and installation
identifiers are not redistributed. Structured rows derived from vendor
documentation are retained with provenance and remain subject to the license
and redistribution terms of their source.
