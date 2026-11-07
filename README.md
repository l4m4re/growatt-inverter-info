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

The end-to-end evidence, review, consolidation, and Home Assistant consumer
workflow is documented in
[`docs/REGISTER_KNOWLEDGE_WORKFLOW.md`](docs/REGISTER_KNOWLEDGE_WORKFLOW.md).
Consumer repositories must record the exact GII commit they use and must not
edit the generated `spec/` products as a separate source of truth.

The VPP V2.01 and ZABA22 firmware correlation is imported with:

```bash
python tools/import_vpp_and_firmware_analysis.py
python tools/build_spec.py
python tools/validate_spec.py
```

This adds the normalized 30000+/31000+ VPP source rows and the derived
firmware evidence without redistributing firmware. The companion
`Growatt_ModbusTCP` repository can export a GII consumer snapshot with
`python tools/export_gii_register_source.py`; both repositories retain source
revisions and hashes for reconciliation. The firmware projection includes the
hash-pinned 121-case executable legacy-provider subset and the six-replay
capture-conformance aggregate; both remain explicitly bounded by their
confidence limits and do not contain firmware or raw captures. Each VPP
register in the generated spec also carries an `evidence.other_evidence`
record linking its documented name to the hash-pinned ARM access-matrix row;
the route confidence is separate from `semantic_name_confidence`, which stays
`source_correlation_only` unless firmware evidence proves more. Legacy rows
also carry a scoped word-level ARM confidence record: recovered provider
matches are distinguished from explicit `unresolved` absence in the current
firmware artifact set, rather than being silently treated as read-only or
implemented.

The controlled MIN 6000TL-XH portal Battery Settings mapping is retained in
[`sources/evidence/min-6000tl-xh-portal-battery-settings-20261107.json`](sources/evidence/min-6000tl-xh-portal-battery-settings-20261107.json).
It is scoped to the portal-reported communication firmware
`AL1.0/ALBA180101/ZABA-0022/S3EB08D00T00P0FU01M003C`; the ZABA component is
the communication processor and ALBA is retained as the separate
power-control processor identity.

Home Assistant runtime audits and polling-plan reviews are retained with the
register evidence in [`docs/consolidation/`](docs/consolidation/). These
reports describe how the reviewed register knowledge is consumed by the
Growatt integration; they do not make the integration repository a second
register-knowledge store.
