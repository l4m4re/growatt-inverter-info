from __future__ import annotations

import json
from pathlib import Path

from tools.validate_gii_consolidation2b import validate


ROOT = Path(__file__).parents[1]


def candidate() -> dict:
    return json.loads((ROOT / "spec/growatt-register-spec-v2-candidate.json").read_text())


def test_c2b_current_artifacts_are_valid() -> None:
    result = validate(ROOT)
    assert result["valid"], result["errors"]


def test_reviewed_access_is_current_read_write_and_w_is_not_write_only() -> None:
    registers = {
        item["address"]: item
        for item in candidate()["registers"]
        if item.get("table") == "holding"
    }
    assert registers[122]["reviewed_correction"]["reviewed_access_raw"] == "R/W"
    assert registers[123]["reviewed_correction"]["reviewed_access_raw"] == "R/W"
    assert registers[1002]["vendor"]["access_raw"] == "R/W"
    assert registers[1003]["vendor"]["access_raw"] == "W"
    for address in (122, 123, 1002, 1003):
        assert registers[address]["consolidated"]["access"] == "read_write"
        assert registers[address]["consolidated_access_capabilities"] == {
            "readable": True,
            "writable": True,
        }
    assert registers[1003]["vendor"]["access_capabilities"] == {
        "readable": None,
        "writable": True,
    }
    assert registers[124]["consolidated_access_capabilities"] == {
        "readable": None,
        "writable": True,
    }


def test_current_reserved_tail_is_exactly_i3281_i3374() -> None:
    data = candidate()
    ranges = data["vendor_range_semantics"]["vendor_reserved_or_unassigned_ranges"]
    assert next(item for item in ranges if item["table"] == "input" and item["start"] == 3281)["status"] == "RESERVED"
    assert not any(
        item.get("table") == "input"
        and isinstance(item.get("address"), int)
        and 3281 <= item["address"] <= 3374
        for item in data["registers"]
    )
    assert not any(
        item["table"] == "input" and item["start"] <= 3280 <= item["end"] and item["status"] == "RESERVED"
        for item in ranges
    )


def test_current_conflicts_and_queue_are_closed() -> None:
    result = validate(ROOT)
    assert result["retained_access_conflicts_before"] == 4
    assert result["retained_access_conflicts_after"] == 0
    assert result["active_research_queue_count"] == 0
