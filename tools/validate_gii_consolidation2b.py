#!/usr/bin/env python3
"""Validate the current review-resolved C2B artifacts."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path = ROOT) -> dict[str, Any]:
    candidate = load(root / "spec/growatt-register-spec-v2-candidate.json")
    correction = load(root / "docs/consolidation/data/GII-CONSOLIDATION-2B_ACCESS_AND_RESERVED_FINALIZATION.json")
    conflicts = load(root / "docs/consolidation/data/GII-CONSOLIDATION-2B_CONFLICTS.json")
    queue = load(root / "docs/consolidation/data/GII-CONSOLIDATION-2B_RESEARCH_QUEUE.json")
    errors: list[str] = []

    canonical_sha = hashlib.sha256((root / "spec/growatt-register-spec.json").read_bytes()).hexdigest()
    if canonical_sha != EXPECTED_CANONICAL_SHA256:
        errors.append("frozen canonical SHA changed")
    if len(candidate["registers"]) != 1486 or candidate["metrics"]["total_consolidated_registers"] != 1486:
        errors.append("candidate register count changed")
    if candidate["metrics"]["conflict_count"] != 0:
        errors.append("current candidate retains conflicts")
    if conflicts["retained_access_conflicts"] != 0:
        errors.append("current conflict artifact retains access conflicts")
    if queue["active_count"] != 0 or queue["active_items"]:
        errors.append("current research queue is not empty")

    by_address = {
        item["address"]: item
        for item in candidate["registers"]
        if item.get("table") == "holding" and isinstance(item.get("address"), int)
    }
    for address in (122, 123, 1002, 1003):
        item = by_address.get(address)
        if item is None:
            errors.append(f"H{address} is missing")
            continue
        if item["consolidated"]["access"] != "read_write":
            errors.append(f"H{address} is not current read_write")
        if item.get("conflict_refs"):
            errors.append(f"H{address} retains conflict references")
        if item.get("consolidated_access_capabilities") != {"readable": True, "writable": True}:
            errors.append(f"H{address} current capabilities are incorrect")
    if by_address[122]["reviewed_correction"]["reviewed_access_raw"] != "R/W":
        errors.append("H122 reviewed raw access is not R/W")
    if by_address[123]["reviewed_correction"]["reviewed_access_raw"] != "R/W":
        errors.append("H123 reviewed raw access is not R/W")
    if by_address[1003]["vendor"]["access_raw"] != "W":
        errors.append("H1003 historical vendor marker is not preserved as W")
    if by_address[1003]["vendor"]["access_capabilities"] != {"readable": None, "writable": True}:
        errors.append("H1003 W marker was normalized incorrectly")

    for address in (1004, 1005, 1006, 1007, 1008, 1009, 1010, 1011, 1012, 124):
        item = by_address.get(address)
        if item and item["consolidated_access_capabilities"] == {"readable": False, "writable": True}:
            errors.append(f"H{address} incorrectly implies write-only access")

    ranges = candidate["vendor_range_semantics"]["vendor_reserved_or_unassigned_ranges"]
    input_tail = next((item for item in ranges if item["table"] == "input" and item["start"] == 3281), None)
    if not input_tail or (input_tail["end"], input_tail["status"]) != (3374, "RESERVED"):
        errors.append("I3281-I3374 current reserved range is missing")
    if any(
        item.get("table") == "input"
        and isinstance(item.get("address"), int)
        and 3281 <= item["address"] <= 3374
        for item in candidate["registers"]
    ):
        errors.append("I3281-I3374 were instantiated as semantic candidate registers")
    if any(
        item["table"] == "input" and item["start"] <= 3280 <= item["end"]
        for item in ranges
        if item["status"] == "RESERVED"
    ):
        errors.append("I3250-I3280 was accidentally included in a reserved range")

    return {
        "valid": not errors,
        "errors": errors,
        "canonical_sha256": canonical_sha,
        "candidate_register_count": len(candidate["registers"]),
        "retained_access_conflicts_before": correction["resolved_access"]["before_retained_access_conflicts"],
        "retained_access_conflicts_after": conflicts["retained_access_conflicts"],
        "active_research_queue_count": queue["active_count"],
    }


def main() -> None:
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
