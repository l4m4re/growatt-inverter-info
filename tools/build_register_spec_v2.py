#!/usr/bin/env python3
"""Build the block-oriented GII product specification and its projections.

The reviewed C2B candidate is input to this product build.  The V2 JSON and
all Markdown files are rendered from one in-memory model; the frozen legacy
specification is imported only as explicitly labelled compatibility material.
"""

from __future__ import annotations

from collections import defaultdict
import hashlib
import json
from pathlib import Path
import re
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "spec/growatt-register-spec-v2-candidate.json"
LEGACY = ROOT / "spec/growatt-register-spec.json"
OUTPUT = ROOT / "spec/v2"
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
    return {
        "role": "explicit_legacy_compatibility_material_not_active_v2_authority",
        "source_spec": {"path": "spec/growatt-register-spec.json", "sha256": sha256(LEGACY)},
        "historical_non_projected_registers": outside_registers,
        "historical_non_projected_logical_fields": outside_fields,
        "historical_context": {
            "families": legacy.get("families", []),
            "protocols": legacy.get("protocols", {}),
            "source_catalog": legacy.get("source_catalog", {}),
            "coverage": legacy.get("coverage", {}),
            "derived_views": legacy.get("derived_views", {}),
            "semantic_index": legacy.get("semantic_index", {}),
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
    candidate = load(root / CANDIDATE.relative_to(ROOT))
    legacy = load(root / LEGACY.relative_to(ROOT))
    if sha256(root / LEGACY.relative_to(ROOT)) != CANONICAL_SHA256:
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
        "artifact": "growatt_register_spec_v2",
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
        "generation": {"generator": "tools/build_register_spec_v2.py", "input_candidate": "spec/growatt-register-spec-v2-candidate.json", "human_projection_same_model": True},
    }


def md_table(rows: list[list[str]], headers: list[str]) -> str:
    result = ["| " + " | ".join(headers) + " |", "| " + " | ".join("---" for _ in headers) + " |"]
    result.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(result)


def render(model: dict[str, Any]) -> dict[str, str]:
    files: dict[str, str] = {}
    files["README.md"] = """# Growatt Register Specification V2\n\nThis is the generated block-oriented product specification. `register-spec-v2.json` is the sole V2 machine-readable authority; every Markdown page is rendered from that same in-memory model. Blocks are primary and family pages are projections.\n\nApplicability selects an existing block or declared range; it never creates a register definition. Legacy and non-V1.24 material is retained explicitly under `legacy_material`.\n\nGenerated indexes: `BLOCK_INDEX.md`, `PROTOCOLS.md`, `SEMANTIC_INDEX.md`, `blocks/`, and `families/`.\n"""
    files["BLOCK_INDEX.md"] = "# Block Index\n\n" + md_table(
        [[b["block_id"], b["table"], f"FC{b['function_code']:02d}", f"{b['address_start']}–{b['address_end']}", str(len(b["register_ids"])), str(len(b["applicability_path_refs"]))] for b in model["blocks"]],
        ["Block", "Table", "Function", "Range", "Register definitions", "Applicability paths"],
    ) + "\n\n## Reserved ranges\n\n" + md_table(
        [[x["range_id"], x["table"], str(x["start"]), str(x["end"]), x["status"], ", ".join(x.get("reservation_basis", []))] for x in model["reserved_ranges"]],
        ["Range", "Table", "Start", "End", "Status", "Basis"],
    ) + "\n\nReserved ranges are first-class and never materialized as semantic registers.\n"
    files["PROTOCOLS.md"] = "# Protocols and native read layout\n\n" + "\n".join(
        f"## `{key}`\n\n```json\n{json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True)}\n```\n" for key, value in model["protocols"].items()
    )
    files["SEMANTIC_INDEX.md"] = "# Semantic Index\n\n" + md_table(
        [[r["semantic_key"] or "", r["canonical_name"] or "", r["register_id"], r["table"], str(r["address"])] for r in model["registers"] if r.get("semantic_key")],
        ["Semantic key", "Canonical name", "Register", "Table", "Address"],
    ) + "\n"
    for block in model["blocks"]:
        rows = [next(r for r in model["registers"] if r["register_id"] == rid) for rid in block["register_ids"]]
        text = f"# `{block['block_id']}`\n\n**{block['table']} FC{block['function_code']:02d} {block['address_start']}–{block['address_end']}**\n\nVendor heading: `{block['vendor_heading_raw'] or ''}`\n\n" + md_table(
            [[r["register_id"], str(r["address"]), str(r["address_end"] or ""), r["semantic_key"] or "", r["canonical_name"] or "", r["access"] or "", r["evidence"]["validation_state"] or ""] for r in rows],
            ["Register", "Address", "End", "Semantic key", "Name", "Access", "Validation"],
        ) + "\n"
        reserved = [x for x in model["reserved_ranges"] if x.get("block_ref") == block["block_id"]]
        if reserved:
            text += "\n## Reserved ranges\n\n" + md_table([[x["range_id"], x["status"], ", ".join(x.get("reservation_basis", []))] for x in reserved], ["Range", "Status", "Basis"]) + "\n"
        files[f"blocks/{block['block_id']}.md"] = text
    for family in model["families"]:
        declarations = [x for x in model["applicability"]["declarations"] if x["family_id"] == family["family_id"]]
        declaration_text = "\n\n".join(f"`{x['declaration_id']}`: {x.get('raw_text', '')}" for x in declarations)
        family_registers = [next(r for r in model["registers"] if r["register_id"] == rid) for rid in family["register_ids"]]
        files[f"families/{slug(family['family_id'])}.md"] = "# " + " / ".join(family["canonical_names"]) + "\n\n" + declaration_text + "\n\n" + md_table(
            [[ref, "yes" if ref in family["block_refs"] else "declared/no semantic block"] for ref in family["applicability_path_refs"]], ["Applicability path", "Resolved block"]
        ) + "\n\nBlock projections: " + ", ".join(f"`{x}`" for x in family["block_refs"]) + ". Register rows below are references to shared block definitions; applicability does not duplicate them.\n\n" + md_table(
            [[r["register_id"], r["table"], str(r["address"]), r["semantic_key"] or "", r["canonical_name"] or "", r["access"] or ""] for r in family_registers],
            ["Register", "Table", "Address", "Semantic key", "Name", "Access"],
        ) + "\n"
    return files


def generate(root: Path = ROOT, output: Path = OUTPUT) -> dict[str, Any]:
    model = build_model(root)
    output.mkdir(parents=True, exist_ok=True)
    dump(output / "register-spec-v2.json", model)
    for relative, text in render(model).items():
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding="utf-8")
    return model


if __name__ == "__main__":
    model = generate()
    print(json.dumps(model["metrics"], indent=2, sort_keys=True))
