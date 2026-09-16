# Growatt Inverter Info

This repository contains a consolidated Growatt Modbus register specification
built from vendor documents and corroborating source and evidence records.

## Products

- [`spec/growatt-register-spec.json`](spec/growatt-register-spec.json) is the
  authoritative machine-readable specification.
- [`spec/growatt-register-spec.md`](spec/growatt-register-spec.md) is the
  generated human-readable protocol reference.
- [`spec/growatt-register-spec.schema.json`](spec/growatt-register-spec.schema.json)
  validates the JSON structure.

The JSON defines shared register blocks once and connects product families to
them through applicability paths. Declared family ranges do not imply that
every address has a semantic register.

## Rebuild and validate

With Python and the project dependencies installed:

```bash
python tools/build_spec.py
python tools/validate_spec.py
```

Install the package and test dependency in a new environment with
`python -m pip install -e '.[test]'`.

## Sources and changes

The retained vendor, implementation, runtime, and reviewed evidence corpus is
under [`sources/`](sources/). The accepted consolidated block input is
`sources/consolidated/register-blocks.json`; retained legacy compatibility
material is under `sources/legacy/` and is included explicitly in the JSON.

Read [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md) before adding or correcting
register knowledge. [`docs/REVERSE_ENGINEERING.md`](docs/REVERSE_ENGINEERING.md)
covers safe evidence collection boundaries.
