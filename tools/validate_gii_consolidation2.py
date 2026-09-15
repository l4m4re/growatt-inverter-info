#!/usr/bin/env python3
"""Validate GII-CONSOLIDATION-2 classification invariants."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
EXPECTED_BASELINE_GAPS = 377


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate(root: Path = ROOT) -> dict[str, Any]:
    data = root / "docs/consolidation/data"
    classification = load(data / "GII-CONSOLIDATION-2_MIN_TL_XH_GAP_CLASSIFICATION.json")
    projection = load(data / "GII-CONSOLIDATION-2_MIN_TL_XH_PROJECTION.json")
    conflicts = load(data / "GII-CONSOLIDATION-2_CONFLICTS.json")
    unresolved = load(data / "GII-CONSOLIDATION-2_UNRESOLVED.json")
    queue = load(data / "GII-CONSOLIDATION-2_RESEARCH_QUEUE.json")
    candidate = load(root / "spec/growatt-register-spec-v2-candidate.json")
    canonical = load(root / "spec/growatt-register-spec.json")
    errors: list[str] = []
    items = classification["items"]
    categories = [item["gap_category"] for item in items]
    if len(items) != EXPECTED_BASELINE_GAPS:
        errors.append(f"expected {EXPECTED_BASELINE_GAPS} original gaps, got {len(items)}")
    if len({item["gap_id"] for item in items}) != len(items):
        errors.append("canonical gap IDs are not unique")
    if any(not category for category in categories):
        errors.append("a canonical gap has no category")
    if sum(classification["category_counts"].values()) != EXPECTED_BASELINE_GAPS:
        errors.append("gap category counts do not sum to the original gap count")
    if classification["final_unexplained_count"] != 0 or unresolved["unexplained_count"] != 0:
        errors.append("an unexplained gap remains")
    if conflicts["total"] != 23 or len(conflicts["conflicts"]) != 23:
        errors.append("the 23 original conflicts are not all represented")
    if sum(conflicts["summary"].values()) != 23:
        errors.append("conflict dispositions do not sum to 23")
    if len([item for item in conflicts["conflicts"] if item["original_conflict"]["property"] == "semantic_identity"]) != 2:
        errors.append("H3085 semantic conflicts are incomplete")
    if projection["canonical_sha256"] != EXPECTED_CANONICAL_SHA256:
        errors.append("projection canonical hash changed")
    if classification["canonical_sha256"] != EXPECTED_CANONICAL_SHA256:
        errors.append("classification canonical hash changed")
    if candidate["canonical_comparison"]["sha256"] != EXPECTED_CANONICAL_SHA256:
        errors.append("candidate canonical comparison hash changed")
    if len(canonical["registers"]) != 4048:
        errors.append("canonical register count changed")
    if projection["physical_coverage"]["initial"]["missing"] != EXPECTED_BASELINE_GAPS:
        errors.append("baseline projection no longer reports 377 missing keys")
    if projection["physical_coverage"]["after"]["missing"] != projection["physical_coverage"]["canonical_min_tlxh_physical_keys"] - projection["physical_coverage"]["after"]["covered"]:
        errors.append("after coverage is not disjoint")
    queue_ids = {item.get("queue_id") for item in queue["items"]}
    if len(queue_ids) != len(queue["items"]):
        errors.append("research queue IDs are not unique")
    return {"valid": not errors, "errors": errors, "initial_gaps": len(items), "final_unexplained": unresolved["unexplained_count"], "conflicts": conflicts["total"], "queue_items": len(queue["items"])}


def main() -> None:
    result = validate()
    print(json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
