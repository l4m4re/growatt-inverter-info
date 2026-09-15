#!/usr/bin/env python3
"""Validate the bounded GII-CONSOLIDATION-2A correction artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
EXPECTED_C2_SHA = "1c9c0d34e819d6839958cd9b7a2ae4e2d2cff4a8"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path = ROOT) -> dict[str, Any]:
    data = root / "docs/consolidation/data"
    correction = load(data / "GII-CONSOLIDATION-2A_RESERVED_AND_BMS_CORRECTIONS.json")
    classification = load(data / "GII-CONSOLIDATION-2A_MIN_TL_XH_GAP_CLASSIFICATION.json")
    projection = load(data / "GII-CONSOLIDATION-2A_MIN_TL_XH_PROJECTION.json")
    conflicts = load(data / "GII-CONSOLIDATION-2A_CONFLICTS.json")
    queue = load(data / "GII-CONSOLIDATION-2A_RESEARCH_QUEUE.json")
    candidate = load(root / "spec/growatt-register-spec-v2-candidate.json")
    canonical_path = root / "spec/growatt-register-spec.json"
    errors: list[str] = []

    canonical_sha = hashlib.sha256(canonical_path.read_bytes()).hexdigest()
    if canonical_sha != EXPECTED_CANONICAL_SHA256:
        errors.append("frozen canonical SHA changed")
    if correction["starting_main_sha"] != EXPECTED_C2_SHA or correction["parent_c2_sha"] != EXPECTED_C2_SHA:
        errors.append("C2A parent lineage is incorrect")
    if correction["canonical_sha256"] != EXPECTED_CANONICAL_SHA256:
        errors.append("correction canonical hash is incorrect")
    if classification["initial_gap_count"] != 377 or len(classification["items"]) != 377:
        errors.append("C2A classification does not preserve all 377 C2 gaps")
    if sum(classification["category_counts"].values()) != 377:
        errors.append("C2A classification counts do not sum to 377")

    gap_items = classification["items"]
    input_gap = [item for item in gap_items if item["table"] == "input" and 3281 <= item["address"] <= 3374]
    holding_overlap = [item for item in gap_items if item["table"] == "holding" and 3116 <= item["address"] <= 3123]
    if len(input_gap) != 94 or {item["gap_category"] for item in input_gap} != {"RESERVED_VENDOR_RANGE"}:
        errors.append("I3281-I3374 are not classified as the explicit reserved range")
    if len(holding_overlap) != 8 or {item["gap_category"] for item in holding_overlap} != {"CANONICAL_CONFLICTS_WITH_VENDOR_RESERVED_RANGE"}:
        errors.append("H3116-H3123 are not retained as reserved-range conflicts")

    ranges = candidate["vendor_range_semantics"]["vendor_reserved_or_unassigned_ranges"]
    if not any(
        item["table"] == "holding" and item["start"] == 3115 and item["end"] == 3124 and item["status"] == "RESERVED"
        for item in ranges
    ):
        errors.append("H3115-H3124 reserved range is missing")
    input_range = next((item for item in ranges if item["table"] == "input"), {})
    if (
        (input_range.get("start"), input_range.get("end")) != (3281, 3374)
        or input_range.get("status") not in {"RESERVED_VENDOR_RANGE", "RESERVED"}
    ):
        errors.append("input reserved range is missing")

    candidate_gap_regs = [
        item for item in candidate["registers"]
        if item.get("table") == "input" and isinstance(item.get("address"), int) and 3281 <= item["address"] <= 3374
    ]
    if candidate_gap_regs:
        errors.append("candidate instantiated input gap registers")
    h3085 = next((item for item in candidate["registers"] if item.get("table") == "holding" and item.get("address") == 3085), {})
    h3086 = next((item for item in candidate["registers"] if item.get("table") == "holding" and item.get("address") == 3086), {})
    if h3085.get("consolidated", {}).get("semantic_key") != "bdc_bms_slave_address":
        errors.append("H3085 BDC/BMS semantic key is missing")
    if h3085.get("consolidated", {}).get("default") != 1 or h3085.get("consolidated", {}).get("range_raw") != "1..254":
        errors.append("H3085 default/range is incorrect")
    if h3085.get("consolidated", {}).get("subsystem") != "bdc_bms" or h3085.get("consolidated", {}).get("interface") != "sys_com_rs485_battery":
        errors.append("H3085 interface scope is missing")
    if h3086.get("consolidated", {}).get("semantic_key") != "bdc_bms_rs485_baud_rate":
        errors.append("H3086 BDC/BMS semantic key is missing")
    if h3086.get("consolidated", {}).get("enum_values") != {"0": "9600 bps", "1": "38400 bps"}:
        errors.append("H3086 enum values are incorrect")
    if h3086.get("consolidated", {}).get("subsystem") != "bdc_bms" or h3086.get("consolidated", {}).get("interface") != "sys_com_rs485_battery":
        errors.append("H3086 interface scope is missing")

    if projection["existence_model"]["applicability_is_existence"] or projection["existence_model"]["polling_is_existence"]:
        errors.append("applicability/polling incorrectly promotes existence")
    if len(conflicts["conflicts"]) != 23:
        errors.append("C2 conflict inventory was not preserved")
    if sum(item["disposition"] == "RETAINED_ACCESS_CONFLICT_REVIEW" for item in conflicts["conflicts"]) != 4:
        errors.append("the four access conflicts were not retained")
    if any(item["disposition"] == "RETAINED_SEMANTIC_CONFLICT_REVIEW" for item in conflicts["conflicts"]):
        errors.append("resolved H3085 semantic conflicts remain active")
    queue_ids = {item["queue_id"] for item in queue["items"]}
    if queue_ids & {"h3085-semantic", "canonical-only-holding-3116-3123", "canonical-only-input-3281-3374"}:
        errors.append("resolved C2 queue item remains active")
    if candidate["metrics"]["total_consolidated_registers"] != 1486:
        errors.append("candidate register count changed")
    return {
        "valid": not errors,
        "errors": errors,
        "canonical_sha256": canonical_sha,
        "candidate_register_count": candidate["metrics"]["total_consolidated_registers"],
        "classification_items": len(gap_items),
        "queue_items": len(queue["items"]),
        "retained_access_conflicts": sum(item["disposition"] == "RETAINED_ACCESS_CONFLICT_REVIEW" for item in conflicts["conflicts"]),
    }


def main() -> None:
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
