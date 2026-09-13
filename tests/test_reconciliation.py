"""Focused invariants for the PIPELINE-4 reconciliation shadow."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

from tools.build_reconciliation import build
from tools.validate_reconciliation import validate

ROOT = Path(__file__).resolve().parents[1]
START_SHA = "1b929fa4b46fb7f7bb8b7bd0beeebc7eb3074fe3"


def decisions() -> dict[str, dict[str, Any]]:
    return {
        item["decision_id"]: item
        for item in json.loads((ROOT / "reconciliation/resolved-assertions.json").read_text())["decisions"]
    }


def test_reconciliation_validates_and_scope_repair_is_visible() -> None:
    assert validate() == []
    conflicts = json.loads((ROOT / "sources/claims/conflicts.json").read_text())
    assert conflicts["scope_aware_total"] == 201
    assert conflicts["hard_conflict_count"] == 46
    assert conflicts["potential_scope_conflict_count"] == 155
    assert conflicts["pipeline3_baseline"]["count"] == 201
    assert not any(item["scope_id"] == "legacy_pv" for item in conflicts["conflicts"])


def test_physical_table_identity_is_not_crossed() -> None:
    items = decisions()
    assert items["min-xh-h3047-battery-first-charge-rate"]["target"]["table"] == "holding"
    assert items["min-xh-h3047-battery-first-charge-rate"]["target"]["address"] == 3047
    assert not any(
        item["target"].get("table") == "input" and item["target"].get("address") == 3047
        for item in items.values()
    )


def test_xh_slots_use_reusable_packed_codecs() -> None:
    items = decisions()
    slot_2 = items["min-xh-slot-2"]["decision"]["value"]
    assert slot_2 == {
        "slot": 2,
        "start_control": "H3040",
        "end": "H3041",
        "encoding_template": "xh_schedule_start_control_v124/xh_schedule_end_v124",
    }
    start = items["min-xh-template-start-control-v124"]["decision"]["value"]
    assert [(field["name"], field["bits"]) for field in start["fields"]] == [
        ("minute", [0, 7]),
        ("hour", [8, 12]),
        ("priority", [13, 14]),
        ("enable", [15, 15]),
    ]
    assert start["fields"][2]["values"]["3"] == "reserved_or_unknown"
    assert items["min-xh-h3046-reserved"]["decision"]["status"] == "reserved"
    assert items["min-xh-h3046-reserved"]["decision"]["value"] == {"reserved": True}
    assert items["min-xh-h3047-battery-first-charge-rate"]["target"]["address"] == 3047
    assert items["min-xh-h3048-battery-first-stop-soc"]["target"]["address"] == 3048
    assert items["min-xh-h3049-ac-charge-enable"]["target"]["address"] == 3049
    assert items["min-xh-slot-3"]["decision"]["value"]["inherits_from"] == "Time1"
    assert items["min-xh-slot-4"]["decision"]["value"]["inherits_from"] == "Time1"
    assert items["min-xh-slot-5-through-9"]["decision"]["value"]["inherits_from"] == "Time1"


def test_i3000_raw_normal_decodes_into_status_byte() -> None:
    item = decisions()["min-input-i3000-status-mode"]["decision"]["value"]
    raw = 0x0001
    mode = raw >> 8
    status = raw & 0xFF
    assert (mode, status) == (0, 1)
    assert item["fields"][0]["enum"][str(mode)] == "waiting_module"
    assert item["fields"][1]["enum"][str(status)] == "normal"
    assert set(item["fields"][0]["enum"].values()).isdisjoint(item["fields"][1]["enum"].values())


def test_status_codebooks_and_current_relationships_remain_explicit() -> None:
    items = decisions()
    derating = items["min-input-i3165-derating-codebook"]["decision"]["value"]
    assert {"22", "23", "24"} <= set(derating["values"])
    assert derating["reserved"] == [[7, 15], [25, 29]]
    packed = items["min-input-i3166-packed-status"]["decision"]["value"]
    assert packed["fields"][0]["bits"] == [8, 15]
    assert packed["fields"][1]["bits"] == [0, 7]
    request_bits = items["min-input-i3211-request-flags"]["decision"]["value"]["bits"]
    assert [item["bit"] for item in request_bits] == [0, 1, 2, 8, 9]
    assert items["min-input-i3111-cloud-word4-relationship"]["decision"]["status"] == "provisionally_resolved"
    assert items["min-input-i3111-present-fft"]["decision"]["value"]["semantic_key"] != "sys_fault_word4"
    assert items["min-input-i3170-bdc-current-magnitude"]["decision"]["value"]["signedness"] == "non_negative"
    assert items["min-input-i3217-bms-current"]["decision"]["value"]["signedness"] == "signed"


def test_percentage_normalizations_have_explicit_review_support() -> None:
    items = decisions()
    support = {key: set(items[key]["support"]) for key in (
        "min-xh-h3036-grid-first-discharge-rate",
        "min-xh-h3037-grid-first-stop-soc",
        "min-xh-h3082-load-first-stop-soc",
    )}
    assert "min_semantic_review:holding:3036:0" in support["min-xh-h3036-grid-first-discharge-rate"]
    assert "min_semantic_review:holding:3037:1" in support["min-xh-h3037-grid-first-stop-soc"]
    assert "min_semantic_review:holding:3082:26" in support["min-xh-h3082-load-first-stop-soc"]
    assert items["min-xh-h3036-grid-first-discharge-rate"]["decision"]["value"]["special_value_semantics"]["255"] == "unresolved"
    assert items["min-xh-h3082-load-first-stop-soc"]["decision"]["value"]["source_unit"] == "ratio"


def test_fc20_is_separate_and_unresolved() -> None:
    item = decisions()["min-fc20-proprietary-profile"]
    assert item["target"]["namespace"] == "GROWATT_FC0x20"
    assert item["decision"]["status"] == "unresolved"
    assert item["decision"]["value"]["function_code_decimal"] == 32
    assert item["decision"]["value"]["semantics"] == "unresolved"


def test_query_exposes_logical_pair_for_h3040() -> None:
    result = subprocess.run(
        ["python3", "tools/query_reconciliation.py", "--family", "min_tl_xh", "--table", "holding", "--address", "3040"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    assert '"id": "min-xh-slot-2"' in result.stdout
    assert '"id": "min-xh-h3040-h3041-access"' in result.stdout


def test_reconciliation_does_not_use_canonical_as_evidence() -> None:
    claims = json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]
    claim_by_id = {item["claim_id"]: item for item in claims}
    for item in decisions().values():
        for claim_id in [*item["support"], *(rejection["claim_id"] for rejection in item["conflicts"] )]:
            artifact = claim_by_id[claim_id]["provenance"]["source_artifact"]
            assert not artifact.startswith("spec/")
            assert "knowledge/compatibility/" not in artifact


def test_canonical_spec_is_byte_identical_to_pipeline3() -> None:
    expected = subprocess.run(
        ["git", "show", f"{START_SHA}:spec/growatt-register-spec.json"],
        cwd=ROOT,
        check=True,
        capture_output=True,
    ).stdout
    actual = (ROOT / "spec/growatt-register-spec.json").read_bytes()
    assert hashlib.sha256(actual).digest() == hashlib.sha256(expected).digest()


def test_shadow_regeneration_is_deterministic() -> None:
    first = json.dumps(build(), ensure_ascii=False, sort_keys=True)
    second = json.dumps(build(), ensure_ascii=False, sort_keys=True)
    checked_in = json.loads((ROOT / "reconciliation/resolved-assertions.json").read_text())
    assert first == second
    assert json.loads(first) == checked_in
