from __future__ import annotations

import json
from pathlib import Path

from tools.validate_gii_consolidation2 import validate


ROOT = Path(__file__).parents[1]


def read(name: str) -> dict:
    return json.loads((ROOT / "docs/consolidation/data" / name).read_text())


def test_completeness_classification_is_disjoint_and_complete() -> None:
    data = read("GII-CONSOLIDATION-2_MIN_TL_XH_GAP_CLASSIFICATION.json")
    assert len(data["items"]) == 377
    assert len({item["gap_id"] for item in data["items"]}) == 377
    assert sum(data["category_counts"].values()) == 377
    assert data["final_unexplained_count"] == 0


def test_physical_and_logical_layers_are_reported_separately() -> None:
    projection = read("GII-CONSOLIDATION-2_MIN_TL_XH_PROJECTION.json")
    coverage = projection["physical_coverage"]
    assert coverage["canonical_min_tlxh_physical_keys"] == 895
    assert coverage["canonical_min_tlxh_logical_register_keys"] == 0
    assert coverage["canonical_min_tlxh_logical_fields"] == 132
    assert coverage["initial"]["missing"] == 377
    assert coverage["after"]["candidate_physical_keys"] == 648
    assert coverage["after"]["missing"] == 247


def test_conflict_review_preserves_all_original_conflicts() -> None:
    conflicts = read("GII-CONSOLIDATION-2_CONFLICTS.json")
    assert conflicts["total"] == 23
    assert sum(conflicts["summary"].values()) == 23
    assert sum(item["original_conflict"]["property"] == "semantic_identity" for item in conflicts["conflicts"]) == 2
    assert sum(item["disposition"] == "RETAINED_ACCESS_CONFLICT_REVIEW" for item in conflicts["conflicts"]) == 4


def test_consolidation2_validator_is_green() -> None:
    result = validate(ROOT)
    assert result["valid"], result["errors"]
