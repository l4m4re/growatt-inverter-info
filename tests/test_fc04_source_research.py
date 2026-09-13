from __future__ import annotations

import json

from tools.build_fc04_source_research import INVENTORY_PATH, build
from tools.validate_fc04_source_research import EXPECTED_ADDRESSES, validate


def test_source_research_covers_the_bounded_candidate_set() -> None:
    inventory, claims, reconciliation = build()
    assert validate() == []
    assert [item["address"] for item in inventory["candidate_findings"]] == EXPECTED_ADDRESSES
    assert inventory["candidate_count"] == 17
    assert len(claims["claims"]) == len(reconciliation["decisions"])


def test_source_research_preserves_property_level_unknowns() -> None:
    inventory, _, _ = build()
    by_address = {item["address"]: item for item in inventory["candidate_findings"]}
    assert by_address[3109]["properties"]["semantic_quantity"]["status"] == "UNRESOLVED"
    assert by_address[3109]["properties"]["packed_field_structure"]["status"] == "SUPPORTED"
    assert by_address[3233]["properties"]["semantic_quantity"]["status"] == "UNRESOLVED"
    assert by_address[3096]["properties"]["scale"]["value"] == "0.1 °C per raw count"


def test_source_research_artifact_rebuilds_deterministically() -> None:
    inventory, _, _ = build()
    assert json.loads(INVENTORY_PATH.read_text(encoding="utf-8")) == inventory
