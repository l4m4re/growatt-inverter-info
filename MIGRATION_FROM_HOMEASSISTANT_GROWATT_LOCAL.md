# Migration from Homeassistant-Growatt-Local-Modbus

This repository was extracted from the register-specification consolidation
line of `l4m4re/Homeassistant-Growatt-Local-Modbus`. The extraction was made
from the consolidation branch only; the HA checkout and its other research
branches were not modified.

## Path changes

| Former HA path | New path | Role |
| --- | --- | --- |
| `doc/register_graph.gpickle` | `knowledge/graph/register-graph.gpickle` | generated graph |
| `doc/consolidated_register_ref.json` | `knowledge/audit/consolidated-register-reference.json` | audit/intermediate export |
| `doc/growatt_register_reference.json` | `knowledge/compatibility/growatt-register-reference.json` | compatibility view |
| `doc/register-spec/` | `spec/` | canonical specification and generated human views |
| `doc/HA_local_registers.json` | `sources/runtime/ha-local-registers.snapshot.json` | HA evidence snapshot |
| `doc/min_6000tl_xh_*` | `sources/evidence/min-6000tl-xh-*.json` | bounded model evidence |
| `doc/*register*.json` | `sources/` | classified source corpus |
| `doc/build_*.py` | `tools/` | reusable pipeline tools |

The public repository does not contain Home Assistant runtime code, broker
code, vendor PDFs, firmware, raw captures, credentials or live installation
identifiers. Existing HA entity identity/statistics remain an integration
compatibility concern and are intentionally not silently migrated here.

## Consumer migration

Consumers should read `spec/growatt-register-spec.json` and use the
`physical_id`, family/table/address, semantic quantity, applicability,
relationship and evidence fields. The compatibility JSON is useful while a
consumer is being migrated, but it is generated and is not a second semantic
source of truth.

The extraction deliberately does not change HA or broker consumers. A later
consumer migration must preserve existing Home Assistant entity IDs, unique
IDs, units, sign conventions, counter semantics and long-term statistics.
