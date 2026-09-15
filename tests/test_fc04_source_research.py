from __future__ import annotations

import json

import pytest
from tools.build_fc04_source_research import INVENTORY_PATH, build
from tools.validate_fc04_source_research import EXPECTED_ADDRESSES, validate


@pytest.fixture(scope="module")
def source_research_data() -> tuple[dict, dict, dict]:
    return build()


@pytest.mark.slow
def test_source_research_covers_the_bounded_candidate_set(
    source_research_data: tuple[dict, dict, dict],
) -> None:
    inventory, claims, reconciliation = source_research_data
    assert validate() == []
    assert [item["address"] for item in inventory["candidate_findings"]] == EXPECTED_ADDRESSES
    assert inventory["candidate_count"] == 17
    assert len(claims["claims"]) == len(reconciliation["decisions"])


@pytest.mark.slow
def test_source_research_preserves_property_level_unknowns(
    source_research_data: tuple[dict, dict, dict],
) -> None:
    inventory, _, _ = source_research_data
    by_address = {item["address"]: item for item in inventory["candidate_findings"]}
    assert by_address[3109]["properties"]["semantic_quantity"]["status"] == "UNRESOLVED"
    assert by_address[3109]["properties"]["packed_field_structure"]["status"] == "SUPPORTED"
    assert by_address[3233]["properties"]["semantic_quantity"]["status"] == "UNRESOLVED"
    assert by_address[3096]["properties"]["scale"]["value"] == "0.1 °C per raw count"


@pytest.mark.slow
def test_source_research_artifact_rebuilds_deterministically(
    source_research_data: tuple[dict, dict, dict],
) -> None:
    inventory, _, _ = source_research_data
    assert json.loads(INVENTORY_PATH.read_text(encoding="utf-8")) == inventory
