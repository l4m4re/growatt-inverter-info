#!/usr/bin/env python3
"""Inventory canonical authority origins and declarative migration coverage."""

from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

try:
    from tools.property_cell_provenance import supported_property_cells
except ModuleNotFoundError:
    from property_cell_provenance import supported_property_cells

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = ROOT / "spec" / "growatt-register-spec.json"
COMPATIBILITY_PATH = ROOT / "knowledge" / "compatibility" / "growatt-register-reference.json"
OUTPUT_PATH = ROOT / "docs" / "pipeline" / "data" / "GII-PIPELINE-5A_AUTHORITY_COVERAGE.json"

# PIPELINE-4A is intentionally loaded as a diagnostic snapshot when this
# branch is based on main, where that non-authoritative layer is not merged.
DECLARATIVE_REF = "8ceb8cd94f50235af4fc10b44ad8cbb355919518"
DECLARATIVE_PATH = "reconciliation/min_tl_xh.json"
ORIGIN_CATEGORIES = {
    "DECLARATIVE",
    "LEGACY_PYTHON",
    "COMPATIBILITY_RULE",
    "CANONICAL_ONLY",
    "DERIVED_GENERATOR",
    "REFERENCE_SOURCE",
    "MULTIPLE_SOURCES",
    "UNKNOWN",
}
PROPERTY_NAMES = (
    "physical_identity",
    "length_words",
    "signedness",
    "scale",
    "unit",
    "physical_quantity",
    "human_description",
    "enum_definitions",
    "packed_layout",
    "access",
    "model_applicability",
    "aliases",
    "provenance_support",
    "normalization",
    "write_semantics",
)
DECISION_PROPERTY_MAP = {
    "semantic_mapping": {
        "physical_quantity",
        "human_description",
        "signedness",
        "unit",
        "normalization",
    },
    "signedness": {"signedness"},
    "enum": {"enum_definitions"},
    "bitfield": {"packed_layout"},
    "packed_encoding": {"packed_layout", "enum_definitions", "physical_quantity"},
    "status": {"provenance_support"},
}


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_declarative() -> tuple[dict[str, Any] | None, dict[str, Any]]:
    local_path = ROOT / DECLARATIVE_PATH
    if local_path.is_file():
        return load_json(local_path), {
            "status": "local_non_authoritative_input",
            "source": DECLARATIVE_PATH,
        }
    result = subprocess.run(
        ["git", "show", f"{DECLARATIVE_REF}:{DECLARATIVE_PATH}"],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        return json.loads(result.stdout), {
            "status": "historical_non_authoritative_snapshot",
            "source": f"git:{DECLARATIVE_REF}:{DECLARATIVE_PATH}",
        }
    return None, {
        "status": "unavailable",
        "source": f"git:{DECLARATIVE_REF}:{DECLARATIVE_PATH}",
    }


def decision_index(data: dict[str, Any] | None) -> dict[tuple[str, str, int], set[str]]:
    indexed: dict[tuple[str, str, int], set[str]] = defaultdict(set)
    if data is None:
        return indexed
    for item in data.get("decisions", []):
        target = item.get("target", {})
        if target.get("namespace") != "MODBUS" or not isinstance(target.get("address"), int):
            continue
        family = target.get("canonical_family")
        table = target.get("table")
        property_name = target.get("property")
        if isinstance(family, str) and table in {"holding", "input"} and isinstance(property_name, str):
            indexed[(family, table, target["address"])].add(property_name)
    return indexed


def property_decision_index(data: dict[str, Any] | None) -> dict[tuple[str, str, int], set[str]]:
    """Index only canonical property cells with explicit claim support."""
    indexed: dict[tuple[str, str, int], set[str]] = defaultdict(set)
    if data is None:
        return indexed
    claims = load_json(ROOT / "sources" / "claims" / "generic-claims.json")["claims"]
    claims_by_id = {claim["claim_id"]: claim for claim in claims}
    for decision in data.get("decisions", []):
        target = decision.get("target", {})
        if target.get("namespace") != "MODBUS" or not isinstance(target.get("address"), int):
            continue
        family = target.get("canonical_family")
        table = target.get("table")
        if isinstance(family, str) and table in {"holding", "input"}:
            indexed[(family, table, target["address"])].update(
                supported_property_cells(decision, claims_by_id)
            )
    return indexed


def physical_key(record: dict[str, Any]) -> tuple[str, int, int]:
    return record["table"], record["address"], record["length_words"]


def canonical_authority_origins(record: dict[str, Any], override_keys: dict[str, set[tuple[str, str, int]]]) -> dict[str, dict[str, Any]]:
    key = (record["family"], record["table"], record["address"])
    origins: dict[str, list[str]] = {
        "physical_identity": ["COMPATIBILITY_RULE", "DERIVED_GENERATOR"],
        "length_words": ["COMPATIBILITY_RULE", "DERIVED_GENERATOR"],
        "signedness": ["COMPATIBILITY_RULE", "DERIVED_GENERATOR"],
        "scale": ["COMPATIBILITY_RULE", "DERIVED_GENERATOR"],
        "unit": ["COMPATIBILITY_RULE", "DERIVED_GENERATOR"],
        "physical_quantity": ["LEGACY_PYTHON", "COMPATIBILITY_RULE"],
        "human_description": ["LEGACY_PYTHON", "COMPATIBILITY_RULE"],
        "enum_definitions": ["REFERENCE_SOURCE", "DERIVED_GENERATOR"],
        "packed_layout": ["REFERENCE_SOURCE", "DERIVED_GENERATOR"],
        "access": ["COMPATIBILITY_RULE"],
        "model_applicability": ["COMPATIBILITY_RULE", "REFERENCE_SOURCE"],
        "aliases": ["COMPATIBILITY_RULE"],
        "provenance_support": ["COMPATIBILITY_RULE", "REFERENCE_SOURCE"],
        "normalization": ["LEGACY_PYTHON", "COMPATIBILITY_RULE"],
        "write_semantics": ["LEGACY_PYTHON", "COMPATIBILITY_RULE"],
    }
    if key in override_keys["normalized"]:
        for name in ("signedness", "scale", "unit", "normalization"):
            origins[name] = ["LEGACY_PYTHON"]
    if key in override_keys["semantic"]:
        origins["physical_quantity"] = ["LEGACY_PYTHON"]
    if key in override_keys["enum"]:
        origins["enum_definitions"] = ["LEGACY_PYTHON"]
    if key in override_keys["bitfield"]:
        origins["packed_layout"] = ["LEGACY_PYTHON"]
    if key in override_keys["packed"]:
        origins["packed_layout"] = ["LEGACY_PYTHON"]
    if not record["enums"]:
        origins.pop("enum_definitions")
    if not record["bitfields"] and not record.get("packed_fields"):
        origins.pop("packed_layout")
    if record["semantic_identity"].get("quantity") is None:
        origins.pop("physical_quantity")
    if record["normalized"].get("unit") is None:
        origins.pop("unit")
    if not record.get("source_aliases"):
        origins.pop("aliases")
    return {
        name: {
            "classification": "MULTIPLE_SOURCES" if len(set(values)) > 1 else values[0],
            "origins": sorted(set(values)),
        }
        for name, values in origins.items()
    }


def override_keys() -> dict[str, set[tuple[str, str, int]]]:
    tree = ast.parse((ROOT / "tools" / "build_register_spec.py").read_text(encoding="utf-8"))
    result: dict[str, set[tuple[str, str, int]]] = defaultdict(set)
    for node in tree.body:
        if not isinstance(node, ast.Assign) or len(node.targets) != 1:
            continue
        target = node.targets[0]
        if not isinstance(target, ast.Name) or target.id not in {
            "SEMANTIC_RENAMES",
            "BITFIELD_OVERRIDES",
            "PACKED_FIELD_OVERRIDES",
            "ENUM_OVERRIDES",
            "NORMALIZED_OVERRIDES",
        }:
            continue
        if target.id == "SEMANTIC_RENAMES":
            continue
        try:
            value = ast.literal_eval(node.value)
        except (ValueError, TypeError, SyntaxError):
            continue
        if not isinstance(value, dict):
            continue
        label = {
            "BITFIELD_OVERRIDES": "bitfield",
            "PACKED_FIELD_OVERRIDES": "packed",
            "ENUM_OVERRIDES": "enum",
            "NORMALIZED_OVERRIDES": "normalized",
        }[target.id]
        for key in value:
            if isinstance(key, tuple) and len(key) == 3 and isinstance(key[0], str) and isinstance(key[1], str) and isinstance(key[2], int):
                result[label].add(key)
    return result


def code_path_inventory() -> list[dict[str, Any]]:
    return [
        {
            "path": "tools/build_register_spec.py",
            "symbols": ["semantic_quantity", "canonical_name", "subsystem", "instance_metadata", "logical_fields"],
            "purpose": "Constructs semantic identity, naming, subsystem/instance classification and logical multi-word fields.",
            "properties": ["physical_quantity", "human_description", "model_applicability", "aliases"],
            "classification": "LEGACY_PYTHON",
            "future_disposition": "Migrate decisions/data; retain only deterministic expansion and serialization algorithms.",
        },
        {
            "path": "tools/build_register_spec.py",
            "symbols": ["SEMANTIC_RENAMES", "BITFIELD_OVERRIDES", "PACKED_FIELD_OVERRIDES", "ENUM_OVERRIDES", "NORMALIZED_OVERRIDES"],
            "purpose": "Register-specific semantic, enum, packed-layout and normalization overrides.",
            "properties": ["physical_quantity", "signedness", "scale", "unit", "enum_definitions", "packed_layout", "normalization"],
            "classification": "LEGACY_PYTHON",
            "future_disposition": "Become claim-supported declarative records; remove from Python.",
        },
        {
            "path": "tools/build_register_spec.py",
            "symbols": ["evidence", "resolution_from_evidence", "write_policy"],
            "purpose": "Derives evidence levels, resolution states and write-risk policy from source fields and hardcoded rules.",
            "properties": ["provenance_support", "write_semantics"],
            "classification": "MULTIPLE_SOURCES",
            "future_disposition": "Keep evidence aggregation generic; migrate policy decisions and property support to declarative data.",
        },
        {
            "path": "tools/build_resolved_register_reference.py",
            "symbols": ["semantic_match", "semantic_for_record", "apply_min_overlay", "apply_semantic_review", "add_min_legacy_bridges", "build_read_plans", "classify"],
            "purpose": "Creates the compatibility records and applies semantic, model, resolution and read-plan rules before canonical generation.",
            "properties": ["physical_quantity", "model_applicability", "scale", "unit", "provenance_support", "write_semantics"],
            "classification": "COMPATIBILITY_RULE",
            "future_disposition": "Compatibility view must become downstream-only; migrate semantic rules and retain only projection/inheritance infrastructure.",
        },
        {
            "path": "tools/generate_consolidated_ref.py",
            "symbols": ["build_canonical_registers", "collect_register_data", "collect_enum_values", "collect_bitflags"],
            "purpose": "Merges graph/source adapters into the audit intermediate and synthesizes shared register data types.",
            "properties": ["physical_identity", "length_words", "human_description", "enum_definitions", "packed_layout", "provenance_support"],
            "classification": "DERIVED_GENERATOR",
            "future_disposition": "Retain as source aggregation only; no independent semantic precedence.",
        },
        {
            "path": "knowledge/compatibility/growatt-register-reference.json",
            "symbols": ["records", "semantic_model", "read_plans", "resolution_model"],
            "purpose": "Generated compatibility view currently consumed as the immediate canonical generator input.",
            "properties": ["physical_identity", "length_words", "physical_quantity", "scale", "unit", "model_applicability", "provenance_support"],
            "classification": "COMPATIBILITY_RULE",
            "future_disposition": "Generate strictly downstream from canonical output; retire as canonical input.",
        },
    ]


def origin_summary(records: list[dict[str, Any]], override_map: dict[str, set[tuple[str, str, int]]]) -> tuple[dict[str, Any], dict[str, dict[str, Any]]]:
    counts: dict[str, Counter[str]] = {name: Counter() for name in PROPERTY_NAMES}
    legacy_exclusive = Counter()
    all_cells = 0
    legacy_cells = 0
    unknown_cells = 0
    for record in records:
        origins = canonical_authority_origins(record, override_map)
        for name, detail in origins.items():
            counts[name][detail["classification"]] += 1
            all_cells += 1
            if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]:
                legacy_cells += 1
            if "UNKNOWN" in detail["origins"]:
                unknown_cells += 1
            if detail["classification"] == "LEGACY_PYTHON":
                legacy_exclusive[name] += 1
    metrics = {
        "canonical_property_cells": all_cells,
        "legacy_authoritative_property_cells": legacy_cells,
        "legacy_authoritative_property_cell_percentage": round(100 * legacy_cells / all_cells, 2),
        "legacy_exclusive_property_cells": sum(legacy_exclusive.values()),
        "unknown_origin_property_cells": unknown_cells,
        "by_property": {
            name: {
                "cells": sum(counter.values()),
                "current_origin_counts": dict(sorted(counter.items())),
                "legacy_exclusive_cells": legacy_exclusive[name],
            }
            for name, counter in counts.items()
        },
    }
    return metrics, {record["physical_id"]: canonical_authority_origins(record, override_map) for record in records}


def declarative_metrics(
    records: list[dict[str, Any]],
    decisions: dict[tuple[str, str, int], set[str]],
    decision_record_count: int,
) -> dict[str, Any]:
    physical_targets = set(decisions)
    covered_records = [record for record in records if (record["family"], record["table"], record["address"]) in physical_targets]
    by_property: dict[str, set[str]] = defaultdict(set)
    for key, properties in decisions.items():
        for property_name in properties:
            by_property[property_name].add(key)
    result = {
        "physical_targets": len(physical_targets),
        "canonical_family_target_matches": len(covered_records),
        "decision_record_count": decision_record_count,
        "physical_decision_property_count": sum(len(properties) for properties in decisions.values()),
        "by_canonical_property": {},
    }
    for property_name in PROPERTY_NAMES:
        keys = by_property.get(property_name, set())
        matched = sum(1 for record in records if (record["family"], record["table"], record["address"]) in keys)
        result["by_canonical_property"][property_name] = {
            "covered_family_records": matched,
            "total_family_records": len(records),
            "percentage": round(100 * matched / len(records), 2),
        }
    return result


def migration_class(record: dict[str, Any], declared_properties: set[str], origins: dict[str, dict[str, Any]]) -> str:
    if declared_properties and {"physical_quantity", "length_words"}.issubset(declared_properties):
        return "READY_DECLARATIVE"
    if declared_properties:
        return "PARTIAL_DECLARATIVE"
    if record["resolution"]["status"] in {"unknown_reserved", "conflicted"}:
        return "EVIDENCE_GATED"
    if record.get("component_of") or record.get("logical_field_id"):
        return "SYNTHETIC_OR_GENERATED"
    if record["enums"] or record["bitfields"] or record.get("packed_fields") or record["relationships"]:
        return "LEGACY_ONLY_COMPLEX"
    if any(detail["classification"] == "COMPATIBILITY_RULE" for detail in origins.values()):
        return "COMPATIBILITY_DERIVED"
    return "LEGACY_ONLY_SIMPLE"


def cohort_summary(records: list[dict[str, Any]], unit_records: dict[tuple[str, int, int], list[dict[str, Any]]]) -> dict[str, Any]:
    predicates = {
        "min_tl_xh_all": lambda r: r["family"] == "min_tl_xh",
        "min_tl_xh_fc04_input_3000_3249": lambda r: r["family"] == "min_tl_xh" and r["table"] == "input" and 3000 <= r["address"] <= 3249,
        "min_tl_xh_fc04_input_3000_3124": lambda r: r["family"] == "min_tl_xh" and r["table"] == "input" and 3000 <= r["address"] <= 3124,
        "min_tl_xh_bms_input_3164_3231": lambda r: r["family"] == "min_tl_xh" and r["table"] == "input" and 3164 <= r["address"] <= 3231,
        "holding_all_families": lambda r: r["table"] == "holding",
        "input_all_families": lambda r: r["table"] == "input",
        "legacy_families": lambda r: r["family"] in {"legacy_inverter_315", "spf_offgrid"},
        "structured_encoding": lambda r: bool(r["enums"] or r["bitfields"] or r.get("packed_fields") or r.get("logical_field_id")),
    }
    result = {}
    for name, predicate in predicates.items():
        selected = [record for record in records if predicate(record)]
        units = {physical_key(record) for record in selected}
        result[name] = {
            "family_records": len(selected),
            "physical_units": len(units),
            "semantic_records": sum(bool(record["semantic_identity"].get("quantity")) for record in selected),
            "source_provenance_records": sum(bool(record.get("source_provenance")) for record in selected),
        }
    result["shared_bus_units"] = {
        "physical_units": sum(1 for unit in unit_records.values() if len({record["family"] for record in unit}) > 1),
        "expanded_family_records": sum(len(unit) for unit in unit_records.values() if len({record["family"] for record in unit}) > 1),
    }
    return result


def build(*, property_cell_accounting: bool = True) -> dict[str, Any]:
    canonical = load_json(CANONICAL_PATH)
    compatibility = load_json(COMPATIBILITY_PATH)
    records = canonical["registers"]
    declarative, declarative_source = load_declarative()
    decisions = property_decision_index(declarative) if property_cell_accounting else decision_index(declarative)
    decision_record_count = len(declarative.get("decisions", [])) if declarative else 0
    override_map = override_keys()
    origin_metrics, origins_by_record = origin_summary(records, override_map)
    unit_records: dict[tuple[str, int, int], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        unit_records[physical_key(record)].append(record)

    inventory = []
    migration_counts: Counter[str] = Counter()
    for record in records:
        decision_key = (record["family"], record["table"], record["address"])
        decision_properties = set()
        if property_cell_accounting:
            decision_properties.update(decisions.get(decision_key, set()))
        else:
            for decision_property in decisions.get(decision_key, set()):
                decision_properties.update(DECISION_PROPERTY_MAP.get(decision_property, set()))
        origins = origins_by_record[record["physical_id"]]
        classification = migration_class(record, decision_properties, origins)
        migration_counts[classification] += 1
        inventory.append({
            "unit_id": ":".join(str(item) for item in (record["family"], record["table"], record["address"], record["length_words"])),
            "physical_id": record["physical_id"],
            "family": record["family"],
            "table": record["table"],
            "address": record["address"],
            "length_words": record["length_words"],
            "canonical_record_count": 1,
            "semantic_keys": [record["semantic_identity"]["quantity"]] if record["semantic_identity"].get("quantity") else [],
            "declarative_properties": sorted(decision_properties),
            "legacy_dependencies": sorted({name for name, detail in origins.items() if "LEGACY_PYTHON" in detail["origins"]}),
            "compatibility_dependencies": sorted({name for name, detail in origins.items() if "COMPATIBILITY_RULE" in detail["origins"]}),
            "missing_declarative_properties": sorted(set(PROPERTY_NAMES) - decision_properties),
            "provenance_status": "canonical_source_provenance_present" if record.get("source_provenance") else "missing",
            "migration_class": classification,
            "migration_risk": "high" if classification in {"LEGACY_ONLY_COMPLEX", "EVIDENCE_GATED", "SYNTHETIC_OR_GENERATED"} else "medium" if classification == "PARTIAL_DECLARATIVE" else "low",
        })
    inventory.sort(key=lambda item: (item["family"], item["table"], item["address"], item["length_words"]))

    semantic_keys = {record["semantic_identity"]["quantity"] for record in records if record["semantic_identity"].get("quantity")}
    physical_address_units = {(record["table"], record["address"]) for record in records}
    semantic_family_units = {(record["family"], record["semantic_identity"]["quantity"]) for record in records if record["semantic_identity"].get("quantity")}
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_canonical_authority_coverage",
        "generated_by": "tools/build_authority_coverage.py",
        "inputs": {
            "canonical": {"path": "spec/growatt-register-spec.json", "sha256": sha256(CANONICAL_PATH)},
            "compatibility": {"path": "knowledge/compatibility/growatt-register-reference.json", "sha256": sha256(COMPATIBILITY_PATH), "role": "current legacy generator input, not future authority"},
            "declarative": declarative_source,
        },
        "authority_status": {
            "canonical_current_authority": "existing canonical specification plus legacy generation/compatibility machinery",
            "declarative_current_authority": "non_authoritative_diagnostic_input",
            "future_target": "declarative source -> validation/reconciliation -> pure expansion/generation -> canonical artifact",
        },
        "counts": {
            "canonical_records": len(records),
            "canonical_holding_records": sum(record["table"] == "holding" for record in records),
            "canonical_input_records": sum(record["table"] == "input" for record in records),
            "distinct_family_physical_targets": len({(record["family"], record["table"], record["address"], record["length_words"]) for record in records}),
            "distinct_bus_physical_units": len(unit_records),
            "distinct_table_address_units": len(physical_address_units),
            "distinct_semantic_concepts": len(semantic_keys),
            "semantic_family_units": len(semantic_family_units),
            "semantic_assigned_records": sum(bool(record["semantic_identity"].get("quantity")) for record in records),
            "logical_fields": len(canonical["logical_fields"]),
            "compatibility_records": len(compatibility["records"]),
            "expansion_ratio_family_records_per_bus_unit": round(len(records) / len(unit_records), 3),
        },
        "declarative_coverage": {
            "accounting_mode": "explicit_property_cell_support" if property_cell_accounting else "historical_decision_expansion",
            **declarative_source,
            **declarative_metrics(records, decisions, decision_record_count),
        },
        "authority_origin_metrics": origin_metrics,
        "legacy_code_inventory": code_path_inventory(),
        "compatibility_semantics_inventory": [
            {"path": "knowledge/audit/consolidated-register-reference.json", "classification": "DERIVED_GENERATOR", "semantic_role": "graph-derived source aggregation and datatype evidence", "disposition": "retain as source/intermediate input; no precedence rule"},
            {"path": "tools/build_resolved_register_reference.py", "classification": "COMPATIBILITY_RULE", "semantic_role": "semantic matching, MIN overlays, resolution and read-plan policy", "disposition": "migrate semantic rules; keep only projection/inheritance infrastructure"},
            {"path": "knowledge/compatibility/growatt-register-reference.json", "classification": "COMPATIBILITY_RULE", "semantic_role": "expanded 4,048-record compatibility surface consumed by canonical builder", "disposition": "generate downstream from canonical; prohibit canonical input use after migration"},
        ],
        "schema_gap_analysis": [
            {"concept": "property_level_claim_support", "examples": ["min_tl_xh:input:3000", "min_tl_xh:holding:3082"], "gap": "Current reconciliation decisions cite claims, but the canonical register schema has no property-to-decision/support reference.", "minimal_extension": "Add optional property_provenance keyed by canonical property with decision_id and claim_ids.", "kind": "semantic"},
            {"concept": "family_model_applicability", "examples": ["min_tl_xh:holding:3036", "tl3_max_mid_mac:input:3000"], "gap": "A list of applicability strings cannot express model, firmware, region and conditional scope without generator rules.", "minimal_extension": "Add scoped applicability predicates and explicit inheritance/override relationships.", "kind": "semantic"},
            {"concept": "logical_field_relationships", "examples": ["multi-word energy counters", "MIN/TL-XH schedule slots"], "gap": "Current logical fields are partly discovered by Python name/adjacency heuristics.", "minimal_extension": "Add declarative logical_field records containing component physical IDs, order, roles and encoding template references.", "kind": "semantic"},
            {"concept": "normalization_transform", "examples": ["min_tl_xh:holding:3082"], "gap": "source_unit is not an executable or auditable transformation description.", "minimal_extension": "Add explicit source_unit, target_unit, operation and factor/offset fields with claim support.", "kind": "semantic"},
            {"concept": "generated_expansion", "examples": ["shared table/address units across eight families", "family record matrix"], "gap": "The current decision schema targets a register but does not state how inheritance, family expansion or aliases produce records.", "minimal_extension": "Add declarative family/base templates and deterministic expansion relationships; keep expansion code generic.", "kind": "generative"},
            {"concept": "evidence_gated_unknown", "examples": ["reserved fields", "unresolved special values"], "gap": "Decision values can say unresolved, but generated canonical properties do not uniformly retain decision-level unresolved state.", "minimal_extension": "Require resolution status and unresolved rationale on every promoted property, without inventing a value.", "kind": "semantic"},
        ],
        "migration_cohorts": cohort_summary(records, unit_records),
        "recommended_first_cohort": {
            "id": "min_tl_xh_fc04_input_3000_3249",
            "reason": "One modern V1.24 family, two vendor-native 125-word input pages, strong vendor/live evidence, and a bounded 250-record family slice that exercises enums, packed fields, BMS semantics, provenance and expansion without migrating all families.",
            "required_before_implementation": ["claim-backed property records", "explicit family scope", "declarative logical-field templates", "full parity projection for this slice"],
        },
        "future_cutover_gates": {
            "coverage": "Every emitted canonical property has declarative authority or is produced by deterministic non-semantic expansion/serialization.",
            "legacy_authority": "legacy_authoritative_property_cells == 0; remaining legacy code paths are classified as pure infrastructure.",
            "compatibility": "canonical generator does not read knowledge/compatibility; compatibility output is downstream-only.",
            "reproduction": "Full generated canonical output matches the retained pre-cutover artifact structurally and semantically.",
            "determinism": "Two clean generation runs with identical source hashes produce byte-identical output.",
            "provenance": "Every supported semantic property has decision and claim/evidence traceability; unresolved facts remain unresolved.",
        },
        "migration_class_counts": dict(sorted(migration_counts.items())),
        "records": inventory,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    result = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"generated authority coverage: {result['counts']['canonical_records']} records, {result['counts']['distinct_bus_physical_units']} bus units, {result['declarative_coverage']['physical_targets']} declarative targets")


if __name__ == "__main__":
    main()
