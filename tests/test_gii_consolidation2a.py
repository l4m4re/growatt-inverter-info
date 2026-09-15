from __future__ import annotations

from pathlib import Path

from tools.validate_gii_consolidation2a import validate


ROOT = Path(__file__).parents[1]


def test_c2a_reserved_and_bms_corrections_are_valid() -> None:
    result = validate(ROOT)
    assert result["valid"], result["errors"]


def test_c2a_keeps_canonical_frozen_and_candidate_cardinality_stable() -> None:
    result = validate(ROOT)
    assert result["canonical_sha256"] == "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
    assert result["candidate_register_count"] == 1486


def test_c2a_keeps_four_access_conflicts_as_the_only_active_queue() -> None:
    result = validate(ROOT)
    assert result["retained_access_conflicts"] == 4
    assert result["queue_items"] == 1
