"""Focused invariants for PIPELINE-8 applicability and evidence accounting."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.build_pipeline8_cohort import build
from tools.pipeline8_evidence import evidence_dimensions
from tools.validate_claims import validate

ROOT = Path(__file__).resolve().parents[1]


def claims() -> list[dict[str, object]]:
    return json.loads(
        (ROOT / "sources/claims/generic-claims.json").read_text(encoding="utf-8")
    )["claims"]


def applicability(table: str, address: int, family: str = "min_tl_xh") -> list[dict[str, object]]:
    return [
        item
        for item in claims()
        if item["assertion"]["kind"] == "document_range_applicability"
        and item["subject"]["family_scope"] == [family]
        and item["subject"].get("table") == table
        and item["subject"]["address"] <= address <= item["subject"]["address_end"]
    ]


def source_rows(table: str, address: int) -> list[dict[str, object]]:
    return [
        item
        for item in claims()
        if item["source_id"] == "vendor_growatt_v124_2020"
        and item["assertion"]["kind"] == "vendor_source_row"
        and item["subject"].get("table") == table
        and item["subject"].get("address") == address
    ]


def test_v124_all_family_declarations_are_projected() -> None:
    family_ids = {
        item["subject"]["family_scope"][0]
        for item in claims()
        if item["assertion"]["kind"] == "document_range_applicability"
    }
    assert family_ids == {
        "min_tl_xh",
        "tl3_max_mid_mac",
        "mod_tl3_xh",
        "storage_mix",
        "storage_spa",
        "storage_sph",
    }
    assert applicability("holding", 3070)
    assert applicability("input", 3300)
    assert applicability("input", 900, "tl3_max_mid_mac")


def test_v124_all_declared_ranges_are_preserved() -> None:
    expected = {
        "min_tl_xh": {
            ("holding", 0, 124),
            ("holding", 3000, 3124),
            ("holding", 3125, 3249),
            ("input", 3000, 3124),
            ("input", 3125, 3249),
            ("input", 3250, 3374),
        },
        "tl3_max_mid_mac": {
            ("holding", 0, 124),
            ("holding", 125, 249),
            ("input", 0, 124),
            ("input", 125, 249),
            ("input", 875, 999),
        },
        "mod_tl3_xh": {
            ("holding", 0, 124),
            ("holding", 3000, 3124),
            ("input", 3000, 3124),
            ("input", 3125, 3249),
        },
        "storage_mix": {
            ("holding", 0, 124),
            ("holding", 1000, 1124),
            ("input", 0, 124),
            ("input", 1000, 1124),
        },
        "storage_spa": {
            ("holding", 0, 124),
            ("holding", 1000, 1124),
            ("input", 1000, 1124),
            ("input", 1125, 1249),
            ("input", 2000, 2124),
        },
        "storage_sph": {
            ("holding", 0, 124),
            ("holding", 1000, 1124),
            ("input", 0, 124),
            ("input", 1000, 1124),
            ("input", 1125, 1249),
        },
    }
    actual = {
        family: {
            (
                item["subject"]["table"],
                item["subject"]["address"],
                item["subject"]["address_end"],
            )
            for item in claims()
            if item["assertion"]["kind"] == "document_range_applicability"
            and item["subject"]["family_scope"] == [family]
        }
        for family in expected
    }
    assert actual == expected


def test_rows_inherit_range_but_keep_local_qualifier_separate() -> None:
    assert len(applicability("holding", 3070)) == 1
    assert len(applicability("holding", 3095)) == 1
    h3071 = evidence_dimensions(claims(), "min_tl_xh", "holding", 3071)
    assert h3071["physical_applicability"]["status"] == "supported"
    assert h3071["model_specific_qualifier"]["status"] == "present"
    assert h3071["unresolved_qualifier"]["status"] == "present"
    assert any("SPH4-11K used" in item["assertion"]["value"] for item in claims() if item["assertion"]["kind"] == "row_local_qualifier" and item["subject"].get("address") == 3071)


def test_h3046_preserves_raw_reserved_and_normalized_role() -> None:
    rows = source_rows("holding", 3046)
    assert rows and rows[0]["assertion"]["value"]["raw_variable"] == "预留"
    assert any(
        item["assertion"]["kind"] == "normalized_protocol_role"
        and item["assertion"]["value"] == "Reserved"
        for item in claims()
        if item["subject"].get("table") == "holding" and item["subject"].get("address") == 3046
    )


def test_evidence_and_write_verification_are_separate() -> None:
    h3095 = evidence_dimensions(claims(), "min_tl_xh", "holding", 3095)
    assert h3095["semantic_row"]["status"] == "supported"
    assert h3095["write_documentation"]["status"] == "documented"
    assert h3095["live_write_verification"]["status"] == "absent"
    assert h3095["semantic_row"]["claim_ids"]
    assert h3095["write_documentation"]["claim_ids"]


def test_pipeline8_selects_bounded_cohort_and_is_deterministic() -> None:
    first = build(starting_sha="test-start")
    second = build(starting_sha="test-start")
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    assert first["selected_cohort"]["addresses"] == [3070, 3071, 3095]
    assert first["selected_cohort"]["physical_parity"] == {
        "selected": 3,
        "expected": 3,
        "percent": 100,
        "note": "H3046 is separately retained as a checked source-row example",
    }
    assert first["candidate_ranking"][0]["id"] == "min_tl_xh_holding_battery_bdc_3070_3071_3095"
    assert first["authority"]["repository_after"]["legacy_authoritative_property_cells"] < first["authority"]["repository_before"]["legacy_authoritative_property_cells"]
    assert hashlib.sha256((ROOT / "spec/growatt-register-spec.json").read_bytes()).hexdigest() == first["canonical"]["sha256"]


def test_generic_claims_validate() -> None:
    assert validate(ROOT / "sources/claims/generic-claims.json") == []
