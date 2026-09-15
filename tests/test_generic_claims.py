"""Golden invariants for the PIPELINE-3 unresolved claim projection."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

from tools.validate_claims import validate

ROOT = Path(__file__).resolve().parents[1]


@lru_cache(maxsize=1)
def claims() -> list[dict[str, Any]]:
    return json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]


def for_subject(namespace: str, table: str | None, address: int | None) -> list[dict[str, Any]]:
    return [
        item for item in claims()
        if item["subject"]["namespace"] == namespace
        and item["subject"].get("table") == table
        and item["subject"].get("address") == address
    ]


def test_generic_claims_validate() -> None:
    assert validate(ROOT / "sources/claims/generic-claims.json") == []


def test_holding_and_input_namespaces_are_distinct() -> None:
    holding = for_subject("MODBUS", "holding", 3047)
    input_register = for_subject("MODBUS", "input", 3047)
    assert holding
    assert input_register
    assert {item["subject"]["table"] for item in holding + input_register} == {"holding", "input"}


def test_h3040_and_nearby_h3047_have_independent_source_claims() -> None:
    selected = for_subject("MODBUS", "holding", 3040) + [
        item for item in claims()
        if item["subject"].get("logical_object") == "xh_schedule_slot_2"
    ]
    assert {item["source_id"] for item in selected} >= {"vendor_growatt_v124_2020", "min_live_validation", "min_shine_tou_write"}
    assert any(item["source_id"] == "openinverter_gateway" for item in for_subject("MODBUS", "holding", 3047))


def test_representative_status_and_cloud_claims_keep_evidence_strength() -> None:
    i3165 = for_subject("MODBUS", "input", 3165)
    i3111 = for_subject("MODBUS", "input", 3111)
    assert {item["source_id"] for item in i3165} >= {"vendor_growatt_v124_2020", "min_live_validation", "min_cloud_oracle"}
    assert any(item["evidence"]["confidence"] == "provisional" for item in i3111)


def test_fc20_has_a_separate_namespace() -> None:
    selected = for_subject("GROWATT_FC0x20", None, None)
    assert len(selected) == 1
    assert selected[0]["subject"]["logical_object"] == "fc20_response"
