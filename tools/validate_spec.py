#!/usr/bin/env python3
"""Validate the current consolidated Growatt register specification."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
SPEC = ROOT / "spec/growatt-register-spec.json"
SCHEMA = ROOT / "spec/growatt-register-spec.schema.json"
LEGACY_SOURCE = ROOT / "sources/legacy/compatibility-registers.json"
CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate(spec: dict[str, Any], schema_path: Path = SCHEMA, legacy_source_path: Path = LEGACY_SOURCE) -> list[str]:
    errors = [error.message for error in Draft202012Validator(load(schema_path)).iter_errors(spec)]
    blocks = spec.get("blocks", [])
    block_by_id = {x.get("block_id"): x for x in blocks}
    if len(block_by_id) != len(blocks):
        errors.append("block_id values are not unique")
    source_by_id = {x.get("source_block_id"): x for x in spec.get("source_native_blocks", [])}
    if len(source_by_id) != len(spec.get("source_native_blocks", [])):
        errors.append("source native block IDs are not unique")
    path_by_id = {x.get("path_id"): x for x in spec.get("applicability", {}).get("paths", [])}
    if len(path_by_id) != len(spec.get("applicability", {}).get("paths", [])):
        errors.append("applicability path IDs are not unique")
    registers = spec.get("registers", [])
    register_by_id = {x.get("register_id"): x for x in registers}
    if len(register_by_id) != len(registers):
        errors.append("register IDs are not unique")
    for block in blocks:
        if block.get("function_code") != {"holding": 3, "input": 4}.get(block.get("table")):
            errors.append(f"{block.get('block_id')}: table/function pairing is invalid")
        if block.get("address_start", 0) > block.get("address_end", -1):
            errors.append(f"{block.get('block_id')}: block address range is reversed")
        for source_ref in block.get("source_native_block_refs", []):
            if source_ref not in source_by_id:
                errors.append(f"{block.get('block_id')}: unknown source native block {source_ref}")
        for path_ref in block.get("applicability_path_refs", []):
            if path_ref not in path_by_id:
                errors.append(f"{block.get('block_id')}: unknown applicability path {path_ref}")
        for register_id in block.get("register_ids", []):
            if register_id not in register_by_id:
                errors.append(f"{block.get('block_id')}: unknown register {register_id}")
            elif register_by_id[register_id].get("table") != block.get("table"):
                errors.append(f"{register_id}: register table differs from containing block")
        block_register_ids = block.get("register_ids", [])
        if len(block_register_ids) != len(set(block_register_ids)):
            errors.append(f"{block.get('block_id')}: register reference is duplicated")
        block_registers = [register_by_id[rid] for rid in block_register_ids if rid in register_by_id]
        identities = [
            (item.get("table"), item.get("address"), item.get("address_end"))
            for item in block_registers
            if item.get("address") is not None
        ]
        if len(identities) != len(set(identities)):
            errors.append(f"{block.get('block_id')}: register identity is duplicated within the block")
    for register in registers:
        if register.get("function_code") != {"holding": 3, "input": 4}.get(register.get("table")):
            errors.append(f"{register.get('register_id')}: table/function pairing is invalid")
        address = register.get("address")
        end = register.get("address_end")
        if address is not None and end is not None and end < address:
            errors.append(f"{register.get('register_id')}: register address range is reversed")
        for path_ref in register.get("applicability_path_refs", []):
            if path_ref not in path_by_id:
                errors.append(f"{register.get('register_id')}: unknown applicability path {path_ref}")
    for item in spec.get("reserved_ranges", []):
        if item["start"] > item["end"]:
            errors.append(f"{item['range_id']}: reserved range is reversed")
        for register in registers:
            if register.get("table") != item["table"] or register.get("address") is None:
                continue
            register_end = register.get("address_end") or register["address"]
            if register["address"] <= item["end"] and register_end >= item["start"]:
                errors.append(f"{item['range_id']}: reserved range overlaps {register['register_id']}")
    for field in spec.get("logical_fields", []):
        for item in field.get("physical_registers", []):
            if item.get("register_id") not in register_by_id:
                errors.append(f"{field.get('id')}: logical component has unknown register")
    if spec.get("canonical_legacy_sha256") != CANONICAL_SHA256:
        errors.append("canonical legacy SHA-256 is not the frozen value")
    legacy_metadata = spec.get("legacy_material", {}).get("source_spec", {})
    if legacy_metadata.get("sha256") != CANONICAL_SHA256:
        errors.append("legacy material does not preserve the frozen canonical SHA-256")
    if legacy_metadata.get("path") != "sources/legacy/compatibility-registers.json":
        errors.append("legacy material does not reference the retained compatibility source")
    if not legacy_source_path.exists() or sha256(legacy_source_path) != CANONICAL_SHA256:
        errors.append("retained compatibility source does not match the frozen canonical SHA-256")
    if any("family" in register for register in registers):
        errors.append("active register definitions contain family-expanded copies")
    for family in spec.get("families", []):
        for register_id in family.get("register_ids", []):
            if register_id not in register_by_id:
                errors.append(f"{family.get('family_id')}: family projection has unknown register")
        for block_id in family.get("block_refs", []):
            if block_id not in block_by_id:
                errors.append(f"{family.get('family_id')}: family projection has unknown block")
    if any(register.get("register_id") not in {rid for block in blocks for rid in block.get("register_ids", [])} for register in registers):
        errors.append("a register is not owned by a block")
    if not any(x["table"] == "holding" and x["start"] == 3115 and x["end"] == 3124 and x["status"] == "RESERVED" for x in spec.get("reserved_ranges", [])):
        errors.append("H3115-H3124 reserved range is missing")
    if not any(x["table"] == "input" and x["start"] == 3281 and x["end"] == 3374 and x["status"] == "RESERVED" for x in spec.get("reserved_ranges", [])):
        errors.append("I3281-I3374 reserved range is missing")
    if any(x["table"] == "input" and x["start"] <= 3280 <= x["end"] for x in spec.get("reserved_ranges", [])):
        errors.append("I3280 is incorrectly classified as reserved")
    if spec.get("metrics", {}).get("conflicts") != 0:
        errors.append("current product contains access conflicts")
    return sorted(set(errors))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", type=Path, default=SPEC)
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    parser.add_argument("--legacy-source", type=Path, default=LEGACY_SOURCE)
    args = parser.parse_args()
    errors = validate(load(args.path), args.schema, args.legacy_source)
    if errors:
        print(json.dumps({"valid": False, "errors": errors}, indent=2))
        raise SystemExit(1)
    markdown_path = args.path.with_name("growatt-register-spec.md")
    markdown_status = {"present": markdown_path.exists()}
    if not markdown_path.exists():
        print(json.dumps({"valid": False, "errors": [f"Markdown projection is missing: {markdown_path}"]}, indent=2))
        raise SystemExit(1)
    markdown = markdown_path.read_text(encoding="utf-8")
    missing = [
        f"{'H' if item['table'] == 'holding' else 'I'}{item['address']}"
        for item in load(args.path)["registers"]
        if item.get("address") is not None
        and f"{'H' if item['table'] == 'holding' else 'I'}{item['address']}" not in markdown
    ]
    if missing:
        print(json.dumps({"valid": False, "errors": [f"Markdown projection omits addresses: {', '.join(missing[:10])}"]}, indent=2))
        raise SystemExit(1)
    markdown_status["register_addresses_present"] = True
    print(json.dumps({"valid": True, "metrics": load(args.path)["metrics"], "markdown": markdown_status}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
