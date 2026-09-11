# Growatt Inverter Info

`growatt-inverter-info` is a project-independent knowledge product for Growatt
Modbus inverter families. It consolidates vendor tables, implementation
snapshots, semantic interpretations and bounded hardware evidence into a
machine-readable register specification and generated human reference.

Home Assistant, brokers, Grott-like decoders and other tools are consumers of
this information. The Home Assistant mapping is retained as evidence and a
compatibility input; it is not the canonical truth.

## Pipeline

```text
sources/                    retained, classified source corpus
    -> tools/build_register_graph.py
knowledge/graph/            graph and provenance relationships
    -> tools/generate_consolidated_ref.py
knowledge/audit/            consolidated audit/intermediate view
    -> tools/build_resolved_register_reference.py
knowledge/compatibility/    resolved compatibility view
    -> tools/build_register_spec.py
spec/                       canonical machine-readable and Markdown product
```

The canonical artifact is [`spec/growatt-register-spec.json`](spec/growatt-register-spec.json).
The generated compatibility view is
[`knowledge/compatibility/growatt-register-reference.json`](knowledge/compatibility/growatt-register-reference.json).
Holding and input tables remain separate. Physical identity is
`(family, table, address)` and semantic identity is represented independently,
so alternate or legacy physical registers can share one semantic concept.

## Quick start

```bash
python3 -m pip install -e '.[test]'
python3 tools/build_register_graph.py
python3 tools/generate_consolidated_ref.py --validate-schema
python3 tools/build_resolved_register_reference.py
python3 tools/validate_resolved_register_reference.py
python3 tools/build_register_spec.py
python3 tools/validate_register_spec.py
python3 -m pytest
```

The checked-in generated outputs should be reproducible. The build uses only
the retained corpus in this repository and does not require a Home Assistant,
broker, inverter or third-party checkout.

## Evidence and scope

The strongest current hardware evidence is read-only validation for a MIN
6000TL-XH. It preserves the known corrections for the H3047/H3048/H3049,
H3081/H3082 and I3047/I3081 spaces, and distinguishes storage/converter-side
I3170 current from BMS I3217 current. No write behavior is claimed by this
release. Native block-read and transport constraints remain family-specific.

Shine/proprietary traffic is kept as a separate research concern and is not
forced into the ordinary register specification. The broker source and raw
captures are deliberately not part of this repository.

See [`sources/manifest.json`](sources/manifest.json) for provenance and
publication classification, [`external/README.md`](external/README.md) for
third-party relationships, and
[`MIGRATION_FROM_HOMEASSISTANT_GROWATT_LOCAL.md`](MIGRATION_FROM_HOMEASSISTANT_GROWATT_LOCAL.md)
for consumers migrating from the former HA repository layout.
