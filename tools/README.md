# Pipeline tools

The supported deterministic pipeline is:

```bash
python3 tools/build_register_graph.py
python3 tools/generate_consolidated_ref.py --validate-schema
python3 tools/build_resolved_register_reference.py
python3 tools/validate_resolved_register_reference.py
python3 tools/build_register_spec.py
python3 tools/validate_register_spec.py
```

The scripts use repository-relative paths and checked-in snapshots. The
extractors are optional refresh tools for local HA or third-party checkouts;
they are not required to build this repository and should not be run against
production systems as part of normal validation.
