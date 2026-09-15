# Pipeline tools

The supported deterministic pipeline is:

```bash
python3 tools/build_register_graph.py
python3 tools/generate_consolidated_ref.py --validate-schema
python3 tools/build_resolved_register_reference.py
python3 tools/validate_resolved_register_reference.py
python3 tools/build_register_spec.py
python3 tools/validate_register_spec.py
python3 tools/build_min_tlxh_audit_matrix.py
python3 tools/validate_min_tlxh_metadata.py
```

The scripts use repository-relative paths and checked-in snapshots. The
extractors are optional refresh tools for local HA or third-party checkouts;
they are not required to build this repository and should not be run against
production systems as part of normal validation.

The vendor-native V1.24 block consolidation is a review candidate and does not
replace the frozen canonical specification:

```bash
python3 tools/build_gii_consolidation.py \
  --pdf ../Homeassistant-Growatt-Local-Modbus/doc/Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf
python3 tools/validate_gii_consolidation.py
```

The builder verifies the original PDF hash and the canonical specification
hash, preserves vendor-native blocks and applicability paths, and emits the
candidate, register matrix, block inventory, conflict queue, unresolved queue
and MIN/TL-XH projection. Manual visual-review claims remain linked evidence;
they are not counted as duplicate source rows.

The GII-2 matrix is a generated audit projection of the canonical spec plus
the MIN/TL-XH review overlay. It is not an additional canonical register map.
The metadata validator is a bounded consistency check for the MIN/TL-XH
consumer projection; it reports valid holding/input address overlaps as
informational and fails only on obvious contradictions.

The Home Assistant read-side reconciliation is run explicitly against a
consumer extractor snapshot:

```bash
python3 tools/audit_homeassistant_consumer.py \\
  --ha-snapshot /path/to/ha-register-snapshot.json \\
  --consumer-commit <consumer-commit> \\
  --output docs/consumers/homeassistant/HA-GII-1_READ_SIDE_FINDINGS.json
```

The snapshot is an input artifact, not a public runtime configuration dump;
private Home Assistant state must remain outside the repository.
