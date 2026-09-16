#!/usr/bin/env python3
"""Build the consolidated Growatt register specification and Markdown view."""

from __future__ import annotations

from collections import defaultdict
import argparse
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
BLOCK_SOURCE = ROOT / "sources/consolidated/register-blocks.json"
LEGACY_SOURCE = ROOT / "sources/legacy/compatibility-registers.json"
OUTPUT = ROOT / "spec"
CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "unknown"


def path_id(path: dict[str, Any]) -> str:
    qualifier = f":{slug(path['qualifier'])}" if path.get("qualifier") else ""
    return ":".join(
        (
            path["source_block_id"],
            path["declaration_id"],
            path["table"],
            str(path["declared_start"]),
            str(path["declared_end"]),
            str(path["function_code"]),
        )
    ) + qualifier


def source_native_blocks(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    result = []
    for block in candidate["source_native_blocks"]:
        result.append(
            {
                "source_block_id": block["source_block_id"],
                "table": block["table"],
                "function_code": block["function_code"],
                "address_start": block["address_start"],
                "address_end": block["address_end"],
                "page_start": block["page_start"],
                "page_end": block["page_end"],
                "vendor_heading_raw": block.get("vendor_heading_raw"),
                "vendor_group_label_raw": block.get("vendor_group_label_raw"),
                "normalized_role": block.get("normalized_role"),
                "role_status": block.get("role_status"),
                "source_claim_refs": list(block.get("rows", [])),
                "source_row_ids": list(block.get("source_row_ids", [])),
                "reviewed_evidence_claims": list(block.get("reviewed_evidence_claims", [])),
                "address_bounds_status": block.get("address_bounds_status"),
            }
        )
    return result


def applicability(candidate: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, str]]:
    paths = []
    ids: dict[str, str] = {}
    for raw in candidate["applicability_paths"]:
        item = dict(raw)
        item["path_id"] = path_id(item)
        ids.setdefault(item["path_id"], item["path_id"])
        item["resolved_block_ref"] = item["consolidated_block_id"]
        paths.append(item)
    for item in paths:
        if not any(b["consolidated_block_id"] == item["resolved_block_ref"] for b in candidate["blocks"]):
            item["resolved_block_ref"] = None
    return paths, ids


def register_id_map(candidate: dict[str, Any]) -> dict[str, str]:
    counts: defaultdict[tuple[str, str, int | None], int] = defaultdict(int)
    for register in candidate["registers"]:
        counts[(register["consolidated_block_id"], register["table"], register.get("address"))] += 1
    result = {}
    for register in candidate["registers"]:
        block = register["consolidated_block_id"]
        address = register.get("address")
        if address is None or counts[(block, register["table"], address)] > 1:
            suffix = register["vendor"]["source_row_id"]
            identifier = f"{block}:{register['table']}:row:{suffix}"
        else:
            identifier = f"{block}:{register['table']}:{address}"
        result[register["register_id"]] = identifier
    return result


def semantic_category(semantic_key: str | None) -> str | None:
    return semantic_key.split(".", 1)[0] if semantic_key and "." in semantic_key else semantic_key


def product_register(register: dict[str, Any], ids: dict[str, str], paths: list[dict[str, Any]]) -> dict[str, Any]:
    consolidated = register.get("consolidated", {})
    end = register.get("address_end")
    length = end - register["address"] + 1 if isinstance(register.get("address"), int) and isinstance(end, int) else (1 if isinstance(register.get("address"), int) else None)
    aliases = sorted(
        {
            value
            for value in [register.get("vendor", {}).get("variable_raw")]
            + [item.get("name") for item in register.get("current_canonical", [])]
            if value
        }
    )
    applicable = []
    for ref in register.get("applicability_paths", []):
        applicable.extend(
            item["path_id"]
            for item in paths
            if item["source_scope"] == ref["source_scope"]
            and item["declared_start"] == ref["declared_start"]
            and item["declared_end"] == ref["declared_end"]
            and item.get("qualifier") == ref.get("qualifier")
        )
    return {
        "register_id": ids[register["register_id"]],
        "source_register_id": register["register_id"],
        "table": register["table"],
        "function_code": register["function_code"],
        "address": register.get("address"),
        "address_end": end,
        "length_words": length,
        "semantic_key": consolidated.get("semantic_key"),
        "canonical_name": consolidated.get("name"),
        "source_aliases": aliases,
        "datatype": {
            "encoding": next((item.get("raw_type") for item in register.get("current_canonical", []) if item.get("raw_type")), None),
            "signed": consolidated.get("signed"),
            "divisor": consolidated.get("divisor"),
            "scale": consolidated.get("scale"),
            "multiplier": consolidated.get("multiplier"),
            "unit": consolidated.get("unit"),
        },
        **({"default": consolidated["default"]} if consolidated.get("default") is not None else {}),
        "access": consolidated.get("access"),
        "semantic_category": semantic_category(consolidated.get("semantic_key")),
        "applicability_path_refs": sorted(set(applicable)),
        "evidence": {
            "validation_state": register.get("status"),
            "ha_readiness": register.get("ha_readiness"),
            "vendor_claim": register.get("vendor", {}),
            "current_canonical_matches": register.get("current_canonical", []),
            "other_evidence": register.get("other_evidence", []),
            "property_provenance": register.get("property_provenance", {}),
            "conflict_refs": register.get("conflict_refs", []),
        },
        "relationships": {
            "relationship_role": "supported",
            "supersedes": [],
            "superseded_by": [],
            "alternate_registers": [],
        },
        "source_provenance": {
            "source_native_block_ref": register["consolidated_block_id"].replace("cb-", "v124-", 1),
            "source_claim_ref": register["vendor"]["claim_id"],
            "source_row_id": register["vendor"]["source_row_id"],
            "vendor_heading_raw": None,
            "pages": [register["vendor"]["page"], register["vendor"]["page_end"]],
            "table": register["table"],
            "function_code": register["function_code"],
            "address_raw": register["vendor"].get("address_raw"),
        },
        "description": consolidated.get("description"),
        "range_raw": consolidated.get("range_raw"),
    }


def legacy_material(legacy: dict[str, Any], active_source_ids: set[str], active_logical_ids: set[str]) -> dict[str, Any]:
    outside_registers = [
        register for register in legacy["registers"] if register.get("physical_id") not in active_source_ids
    ]
    outside_fields = [field for field in legacy["logical_fields"] if field["id"] not in active_logical_ids]
    source_catalog = dict(legacy.get("source_catalog", {}))
    source_catalog.pop("graph_export", None)
    return {
        "role": "explicit_legacy_compatibility_material_not_active_v2_authority",
        "source_spec": {"path": "sources/legacy/compatibility-registers.json", "sha256": sha256(LEGACY_SOURCE)},
        "historical_non_projected_registers": outside_registers,
        "historical_non_projected_logical_fields": outside_fields,
        "historical_context": {
            "families": legacy.get("families", []),
            "protocols": legacy.get("protocols", {}),
            "source_catalog": source_catalog,
        },
        "note": "V1.24 block product records retain matched canonical evidence; records and logical fields not projected remain here so legacy/non-V1.24 knowledge is not silently discarded.",
    }


def enrich_canonical_relationships(
    products: dict[str, dict[str, Any]],
    candidate: dict[str, Any],
    legacy: dict[str, Any],
) -> None:
    """Project legacy semantic roles and relationships onto shared definitions."""
    canonical = {item.get("physical_id"): item for item in legacy["registers"]}
    canonical_to_product: dict[str, str] = {}
    for original in candidate["registers"]:
        product = products.get(original["register_id"])
        if product is None:
            continue
        for match in original.get("current_canonical", []):
            if match.get("physical_id"):
                canonical_to_product[match["physical_id"]] = product["register_id"]
    for original in candidate["registers"]:
        product = products.get(original["register_id"])
        if product is None:
            continue
        records = [canonical[item.get("physical_id")] for item in original.get("current_canonical", []) if item.get("physical_id") in canonical]
        roles = sorted({(item.get("semantic_identity") or {}).get("relationship_role") for item in records if (item.get("semantic_identity") or {}).get("relationship_role")})
        relationships: list[dict[str, Any]] = []
        for record in records:
            structured = {
                "physical_id": record.get("physical_id"),
                "enums": record.get("enums", []),
                "bitfields": record.get("bitfields", []),
                "packed_fields": record.get("packed_fields"),
            }
            if any(structured[key] for key in ("enums", "bitfields", "packed_fields")):
                product["datatype"].setdefault("structured", []).append(structured)
            for relation in record.get("relationships", []):
                item = dict(relation)
                target = item.pop("target", None)
                if target in canonical_to_product:
                    item["target_register_id"] = canonical_to_product[target]
                else:
                    item["target_legacy_physical_id"] = target
                relationships.append(item)
        unique: dict[str, dict[str, Any]] = {
            json.dumps(item, sort_keys=True): item for item in relationships
        }
        product["relationships"] = {
            "relationship_role": roles[0] if len(roles) == 1 else ("mixed" if roles else "unknown"),
            "roles": roles,
            "supersedes": sorted({item.get("target_register_id") for item in unique.values() if item.get("type") == "supersedes" and item.get("target_register_id")}),
            "superseded_by": sorted({item.get("target_register_id") for item in unique.values() if item.get("type") == "superseded_by" and item.get("target_register_id")}),
            "alternate_registers": sorted({item.get("target_register_id") for item in unique.values() if item.get("type") == "alternate" and item.get("target_register_id")}),
            "evidence_relationships": sorted(unique.values(), key=lambda item: json.dumps(item, sort_keys=True)),
        }


def build_model(root: Path = ROOT) -> dict[str, Any]:
    candidate = load(root / BLOCK_SOURCE.relative_to(ROOT))
    legacy_path = root / LEGACY_SOURCE.relative_to(ROOT)
    legacy = load(legacy_path)
    if sha256(legacy_path) != CANONICAL_SHA256:
        raise ValueError("frozen legacy canonical SHA-256 changed")
    path_list, _ = applicability(candidate)
    ids = register_id_map(candidate)
    explicit_reserved = [
        item
        for item in candidate["vendor_range_semantics"]["vendor_reserved_or_unassigned_ranges"]
        if item["status"] == "RESERVED"
    ]
    by_block: defaultdict[str, list[dict[str, Any]]] = defaultdict(list)
    products_by_source: dict[str, dict[str, Any]] = {}
    for register in candidate["registers"]:
        address = register.get("address")
        register_end = register.get("address_end") or address
        if address is not None and any(
            register["table"] == item["table"]
            and address <= item["end"]
            and register_end >= item["start"]
            for item in explicit_reserved
        ):
            continue
        product = product_register(register, ids, path_list)
        source_id = register["consolidated_block_id"].replace("cb-", "v124-", 1)
        product["source_provenance"]["vendor_heading_raw"] = next(
            item.get("vendor_heading_raw")
            for item in source_native_blocks(candidate)
            if item["source_block_id"] == source_id
        )
        by_block[register["consolidated_block_id"]].append(product)
        products_by_source[register["register_id"]] = product
    for values in by_block.values():
        values.sort(key=lambda x: (x["address"] is None, x["address"] if x["address"] is not None else -1, x["register_id"]))

    source_blocks = source_native_blocks(candidate)
    source_by_id = {x["source_block_id"]: x for x in source_blocks}
    reserved = []
    for item in candidate["vendor_range_semantics"]["vendor_reserved_or_unassigned_ranges"]:
        reserved.append(
            {
                **item,
                "range_id": f"{item['table']}:{item['start']}-{item['end']}",
                "block_ref": None,
                "source_provenance": {
                    "source": item.get("source"),
                    "source_artifact": item.get("source_artifact"),
                    "source_page_or_section": item.get("source_page_or_section"),
                    "source_pointer": item.get("source_pointer"),
                },
            }
        )
    blocks = []
    for raw in candidate["blocks"]:
        source_id = raw["consolidated_block_id"].replace("cb-", "v124-", 1)
        source = source_by_id[source_id]
        blocks.append(
            {
                "block_id": raw["consolidated_block_id"],
                "block_kind": "source_native_consolidated",
                "source_native_block_refs": [source_id],
                "table": raw["table"],
                "function_code": raw["function_code"],
                "address_start": raw["address_start"],
                "address_end": raw["address_end"],
                "vendor_heading_raw": source.get("vendor_heading_raw"),
                "vendor_group_label_raw": source.get("vendor_group_label_raw"),
                "role": {"normalized": source.get("normalized_role"), "status": source.get("role_status")},
                "applicability_path_refs": sorted(
                    {path_id(item) for item in path_list if item.get("resolved_block_ref") == raw["consolidated_block_id"]}
                ),
                "register_ids": [
                    ids[x]
                    for x in raw["register_ids"]
                    if any(item["source_register_id"] == x for item in by_block[raw["consolidated_block_id"]])
                ],
                "reserved_range_refs": [],
                "source_provenance": {
                    "document_id": "vendor_growatt_v124_2020",
                    "pages": [source["page_start"], source["page_end"]],
                    "source_claim_refs": source["source_claim_refs"],
                },
            }
        )
    block_ids = {x["block_id"] for x in blocks}
    for item in reserved:
        candidates = [b for b in blocks if b["table"] == item["table"] and b["address_start"] <= item["end"] and b["address_end"] >= item["start"]]
        if candidates:
            item["block_ref"] = candidates[0]["block_id"]
            candidates[0]["reserved_range_refs"].append(item["range_id"])

    families_by_id: defaultdict[str, dict[str, Any]] = defaultdict(lambda: {"family_id": "", "labels": set(), "declaration_refs": set(), "block_refs": set(), "path_refs": set()})
    for declaration in candidate["applicability"]:
        entry = families_by_id[declaration["family_id"]]
        entry["family_id"] = declaration["family_id"]
        entry["labels"].add(declaration["family_label"])
        entry["declaration_refs"].add(declaration["declaration_id"])
    for item in path_list:
        entry = families_by_id[item["family_id"]]
        entry["path_refs"].add(item["path_id"])
        if item.get("resolved_block_ref") in block_ids:
            entry["block_refs"].add(item["resolved_block_ref"])
    family_meta = {x["id"]: x for x in legacy.get("families", [])}
    families = []
    for family_id in sorted(families_by_id):
        entry = families_by_id[family_id]
        meta = family_meta.get(family_id, {})
        family_path_ids = entry["path_refs"]
        family_register_ids = sorted(
            register["register_id"]
            for values in by_block.values()
            for register in values
            if set(register["applicability_path_refs"]) & family_path_ids
        )
        families.append(
            {
                "family_id": family_id,
                "canonical_names": sorted(entry["labels"] or {meta.get("name", family_id)}),
                "declaration_refs": sorted(entry["declaration_refs"]),
                "block_refs": sorted(entry["block_refs"]),
                "applicability_path_refs": sorted(entry["path_refs"]),
                "register_ids": family_register_ids,
                "protocol_group": meta.get("protocol_group"),
                "models": meta.get("models", []),
                "legacy_notes": meta.get("notes"),
            }
        )

    active_by_address = defaultdict(list)
    for original, product in zip(candidate["registers"], [product_register(x, ids, path_list) for x in candidate["registers"]]):
        if isinstance(original.get("address"), int):
            active_by_address[(original["table"], original["address"])].append(product["register_id"])
    active_fields = []
    legacy_field_ids = set()
    for field in legacy["logical_fields"]:
        refs = [active_by_address.get((x["table"], x["address"]), []) for x in field["physical_registers"]]
        if all(refs):
            item = dict(field)
            item["physical_register_ids"] = [values[0] for values in refs]
            item["physical_registers"] = [{"register_id": values[0], "role": ref.get("role")} for values, ref in zip(refs, field["physical_registers"])]
            active_fields.append(item)
        else:
            legacy_field_ids.add(field["id"])
    active_canonical_ids = {
        match["physical_id"]
        for register in candidate["registers"]
        for match in register.get("current_canonical", [])
        if match.get("physical_id")
    }
    legacy_data = legacy_material(legacy, active_canonical_ids, {x["id"] for x in active_fields})
    enrich_canonical_relationships(products_by_source, candidate, legacy)
    legacy_data["historical_non_projected_logical_fields"] = [x for x in legacy["logical_fields"] if x["id"] in legacy_field_ids]
    protocols = legacy.get("protocols", {})
    metrics = {
        "source_native_blocks": len(source_blocks),
        "consolidated_blocks": len(blocks),
        "block_register_definitions": sum(len(x) for x in by_block.values()),
        "reserved_ranges": len(reserved),
        "reserved_words": sum(x["end"] - x["start"] + 1 for x in reserved),
        "applicability_declarations": len(candidate["applicability"]),
        "applicability_paths": len(path_list),
        "families": len(families),
        "logical_fields": len(active_fields),
        "enum_or_bitfield_fields": sum(
            any(
                token in str(register["datatype"].get("encoding", "")).lower()
                for token in ("enum", "bitfield", "packed")
            )
            for register in [x for values in by_block.values() for x in values]
        ),
        "unresolved_registers": candidate["metrics"].get("unresolved_count", 0),
        "conflicts": candidate["metrics"].get("conflict_count", 0),
        "legacy_registers_retained": len(legacy_data["historical_non_projected_registers"]),
        "legacy_logical_fields_retained": len(legacy_data["historical_non_projected_logical_fields"]),
    }
    return {
        "schema_version": "2.0.0",
        "artifact": "growatt_register_spec",
        "authority": "block_oriented_product_projection",
        "canonical_legacy_sha256": CANONICAL_SHA256,
        "source_documents": candidate["source_documents"],
        "protocols": protocols,
        "source_native_blocks": source_blocks,
        "applicability": {"declarations": candidate["applicability"], "paths": path_list},
        "blocks": blocks,
        "registers": [x for block in blocks for x in by_block[block["block_id"]]],
        "reserved_ranges": sorted(reserved, key=lambda x: (x["table"], x["start"])),
        "families": families,
        "logical_fields": sorted(active_fields, key=lambda x: x["id"]),
        "legacy_material": legacy_data,
        "metrics": metrics,
        "generation": {
            "generator": "tools/build_spec.py",
            "block_source": "sources/consolidated/register-blocks.json",
            "legacy_compatibility_source": "sources/legacy/compatibility-registers.json",
            "human_projection_same_model": True,
        },
    }


def markdown_cell(value: Any) -> str:
    if value is None or value == "":
        return "—"
    text = str(value).replace("|", "&#124;").replace("\n", "<br>").strip()
    return text or "—"


def md_table(rows: list[list[Any]], headers: list[str]) -> str:
    result = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    result.extend("| " + " | ".join(markdown_cell(item) for item in row) + " |" for row in rows)
    return "\n".join(result)


def register_address(register: dict[str, Any]) -> str:
    address = register.get("address")
    if address is None:
        return "—"
    prefix = "H" if register["table"] == "holding" else "I"
    end = register.get("address_end")
    if end is not None and end != address:
        return f"{prefix}{address}–{prefix}{end}"
    return f"{prefix}{address}"


def family_names_for_refs(model: dict[str, Any], refs: list[str]) -> str:
    path_by_id = {item["path_id"]: item for item in model["applicability"]["paths"]}
    family_by_id = {item["family_id"]: item for item in model["families"]}
    names = []
    for ref in refs:
        path = path_by_id.get(ref)
        if path is None:
            continue
        family = family_by_id.get(path["family_id"], {})
        names.extend(family.get("canonical_names", [path["family_id"]]))
    return "; ".join(dict.fromkeys(names)) or "Declared range only"


def applicability_summary(model: dict[str, Any], refs: list[str]) -> str:
    path_by_id = {item["path_id"]: item for item in model["applicability"]["paths"]}
    family_by_id = {item["family_id"]: item for item in model["families"]}
    details = []
    for family_id in dict.fromkeys(
        path_by_id[ref]["family_id"] for ref in refs if ref in path_by_id
    ):
        family = family_by_id.get(family_id, {})
        names = "/".join(family.get("canonical_names", [family_id]))
        models = family.get("models", [])
        details.append(f"{names} ({', '.join(models) if models else 'models not specified'})")
    return "; ".join(details) or "Declared range only"


def scale_summary(datatype: dict[str, Any]) -> str:
    parts = []
    for key in ("divisor", "scale", "multiplier"):
        value = datatype.get(key)
        if value is not None:
            parts.append(f"{key}={value}")
    return ", ".join(parts) or "—"


def enum_summary(datatype: dict[str, Any]) -> str:
    values = []
    for structure in datatype.get("structured", []):
        for item in structure.get("enums", []):
            label = item.get("vendor_label") or item.get("canonical_name")
            values.append(f"{item.get('value')} = {label}")
    return "; ".join(dict.fromkeys(values))


def register_rows(model: dict[str, Any], block: dict[str, Any]) -> list[list[Any]]:
    register_by_id = {item["register_id"]: item for item in model["registers"]}
    rows = []
    for register_id in block["register_ids"]:
        register = register_by_id[register_id]
        datatype = register["datatype"]
        encoding = datatype.get("encoding") or "—"
        if datatype.get("signed") is not None:
            encoding += ", " + ("signed" if datatype["signed"] else "unsigned")
        bounds = register.get("range_raw") or ""
        if register.get("default") is not None:
            bounds = "; ".join(part for part in (f"default {register['default']}", bounds) if part)
        enums = enum_summary(datatype)
        if enums:
            bounds = "; ".join(part for part in (bounds, enums) if part)
        rows.append(
            [
                register_address(register),
                register.get("canonical_name") or "; ".join(register.get("source_aliases", [])),
                register.get("description"),
                register.get("access"),
                encoding,
                scale_summary(datatype),
                datatype.get("unit"),
                bounds,
                family_names_for_refs(model, register.get("applicability_path_refs", [])),
                register.get("evidence", {}).get("validation_state"),
            ]
        )
    return rows


def structured_details(model: dict[str, Any], block: dict[str, Any]) -> list[str]:
    register_by_id = {item["register_id"]: item for item in model["registers"]}
    family_by_id = {item["family_id"]: item for item in model["families"]}
    enums: list[list[Any]] = []
    bits: list[list[Any]] = []
    packed: list[list[Any]] = []
    seen: set[str] = set()
    for register_id in block["register_ids"]:
        register = register_by_id[register_id]
        for structure in register["datatype"].get("structured", []):
            physical_id = structure.get("physical_id", "")
            family_id = physical_id.split(":", 1)[0]
            identity = "/".join(family_by_id.get(family_id, {}).get("canonical_names", [family_id])) or "Source record"
            for item in structure.get("enums", []):
                row = [register_address(register), identity, item.get("value"), item.get("vendor_label"), item.get("ambiguous")]
                marker = json.dumps(row, ensure_ascii=False, sort_keys=True)
                if marker not in seen:
                    enums.append(row)
                    seen.add(marker)
            for item in structure.get("bitfields", []):
                row = [register_address(register), identity, item.get("bits"), item.get("vendor_label") or item.get("name"), item.get("description"), item.get("status")]
                marker = json.dumps(row, ensure_ascii=False, sort_keys=True)
                if marker not in seen:
                    bits.append(row)
                    seen.add(marker)
            if structure.get("packed_fields") is not None:
                row = [register_address(register), identity, json.dumps(structure["packed_fields"], ensure_ascii=False, sort_keys=True)]
                marker = json.dumps(row, ensure_ascii=False, sort_keys=True)
                if marker not in seen:
                    packed.append(row)
                    seen.add(marker)
    result = []
    if enums:
        result.extend(["#### Enum values", "", md_table(enums, ["Address", "Source identity", "Value", "Vendor label", "Ambiguous"]), ""])
    if bits:
        result.extend(["#### Bitfields", "", md_table(bits, ["Address", "Source identity", "Bits", "Field", "Description", "Status"]), ""])
    if packed:
        result.extend(["#### Packed fields", "", md_table(packed, ["Address", "Source identity", "Fields"]), ""])
    return result


def source_summary(model: dict[str, Any], block: dict[str, Any]) -> str:
    native_id = block["source_native_block_refs"][0]
    native = next(item for item in model["source_native_blocks"] if item["source_block_id"] == native_id)
    pages = block["source_provenance"].get("pages", [])
    page_text = f"pp. {pages[0]}–{pages[-1]}" if pages else "page range not recorded"
    claim_count = len(block["source_provenance"].get("source_claim_refs", []))
    evidence_count = len(native.get("reviewed_evidence_claims", []))
    return (
        f"{block['source_provenance'].get('document_id')} {page_text}; "
        f"{claim_count} source rows and {evidence_count} reviewed evidence claims. "
        "See [vendor block data](../sources/vendor/growatt-v1.24-blocks.json) "
        "and [source claims](../sources/claims/vendor/vendor_growatt_v124_2020.json)."
    )


def logical_field_rows(model: dict[str, Any]) -> list[list[Any]]:
    register_by_id = {item["register_id"]: item for item in model["registers"]}
    family_by_id = {item["family_id"]: item for item in model["families"]}
    rows = []
    for field in model["logical_fields"]:
        components = []
        for component in field.get("physical_registers", []):
            register = register_by_id.get(component["register_id"])
            if register is not None:
                components.append(f"{register_address(register)} ({component.get('role') or 'word'})")
        parts = (field.get("id") or "").split(":", 2)
        family = family_by_id.get(parts[1], {}) if len(parts) > 1 else {}
        name = field.get("canonical_name") or field.get("canonical_description") or "Logical field"
        rows.append(
            [
                name,
                "/".join(family.get("canonical_names", [])),
                ", ".join(components),
                field.get("encoding"),
                field.get("word_order"),
                field.get("status"),
            ]
        )
    return rows


def render(model: dict[str, Any]) -> str:
    lines = [
        "# Growatt Register Specification",
        "",
        "The JSON specification is authoritative. This document is generated from the same in-memory model and presents the shared register blocks in vendor protocol order.",
        "",
        "## Contents",
        "",
        "- [Scope / applicability](#scope--applicability)",
        "- [Holding registers](#holding-registers)",
    ]
    input_blocks = [block for block in model["blocks"] if block["table"] == "input"]
    holding_blocks = [block for block in model["blocks"] if block["table"] == "holding"]
    for group, blocks in (("Holding registers", holding_blocks), ("Input registers", input_blocks)):
        if group == "Input registers":
            lines.append("- [Input registers](#input-registers)")
        for index, block in enumerate(blocks, start=1):
            anchor = f"block-{block['block_id']}"
            lines.append(f"  - [{block['vendor_heading_raw']}](#{anchor})")
    lines.extend(["- [Logical multi-word fields](#logical-multi-word-fields)", "", "## Scope / applicability", ""])
    lines.append(
        "The register maps preserve the source-native block layout. Each shared block is defined once; applicability paths connect families and declared ranges to those blocks. A declared family range does not by itself establish semantic rows for every address."
    )
    lines.append("")
    family_rows = []
    for family in model["families"]:
        family_rows.append(
            [
                " / ".join(family["canonical_names"]),
                ", ".join(family.get("models", [])) or "Models not specified",
                family.get("protocol_group") or "—",
                len(family["block_refs"]),
            ]
        )
    lines.extend([md_table(family_rows, ["Family", "Models", "Protocol group", "Shared blocks"]), ""])
    lines.append("Block applicability retains the vendor declarations and source/model qualifiers in the JSON `applicability` section.")
    lines.append("")

    for table, heading in (("holding", "Holding registers"), ("input", "Input registers")):
        lines.extend([f"## {heading}", ""])
        blocks = [block for block in model["blocks"] if block["table"] == table]
        for block in blocks:
            anchor = f"block-{block['block_id']}"
            lines.extend([f'<a id="{anchor}"></a>', f"### {block['vendor_heading_raw']}", ""])
            role = block["role"].get("normalized")
            role_status = block["role"].get("status")
            role_text = role if role else f"not normalized ({role_status})"
            prefix = "H" if table == "holding" else "I"
            lines.extend(
                [
                    f"- **Vendor heading:** {block['vendor_heading_raw']}",
                    f"- **Normalized role:** {role_text}",
                    f"- **Table / function:** {table.title()} / FC{block['function_code']:02d}",
                    f"- **Address range:** {prefix}{block['address_start']}–{prefix}{block['address_end']}",
                    f"- **Applicable families / models:** {applicability_summary(model, block['applicability_path_refs'])}",
                    f"- **Source / provenance:** {source_summary(model, block)}",
                    "",
                    md_table(
                        register_rows(model, block),
                        ["Addr", "Variable", "Description", "Access", "Type", "Scale", "Unit", "Range / Enum", "Applicability", "Status"],
                    ),
                    "",
                ]
            )
            lines.extend(structured_details(model, block))
        ranges = [item for item in model["reserved_ranges"] if item["table"] == table]
        if ranges:
            lines.extend(["### Reserved ranges", ""])
            lines.append(
                md_table(
                    [
                        [
                            f"{prefix}{item['start']}–{prefix}{item['end']}",
                            item["status"],
                            ", ".join(item.get("reservation_basis", [])),
                            item.get("semantic_meaning") or "Vendor-designated reserved range",
                            item.get("source_provenance", {}).get("source_page_or_section"),
                        ]
                        for item in ranges
                    ],
                    ["Range", "Status", "Basis", "Meaning", "Source"],
                )
            )
            lines.append("")

    lines.extend(["## Logical multi-word fields", ""])
    lines.append(
        "These rows preserve the accepted component order, word roles, and status. Unknown word order remains unknown; the entries do not imply an additional decoding rule."
    )
    lines.extend(
        [
            "",
            md_table(logical_field_rows(model), ["Variable", "Family", "Component registers", "Encoding", "Word order", "Status"]),
            "",
        ]
    )
    return "\n".join(lines)


def generate(root: Path = ROOT, output: Path = OUTPUT) -> dict[str, Any]:
    model = build_model(root)
    output.mkdir(parents=True, exist_ok=True)
    dump(output / "growatt-register-spec.json", model)
    (output / "growatt-register-spec.md").write_text(render(model), encoding="utf-8")
    return model


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=OUTPUT, help="Directory for the JSON and Markdown products")
    args = parser.parse_args()
    model = generate(output=args.output_dir)
    print(json.dumps(model["metrics"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
