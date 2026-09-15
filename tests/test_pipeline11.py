"""Focused invariants for the PIPELINE-11 accepted-authority lifecycle."""

from __future__ import annotations

from functools import lru_cache
import json
from pathlib import Path
from typing import Any

import pytest
from tools.build_pipeline11_cohort import (
    PIPELINE10_ACCEPTED_TIP_SHA,
    STARTING_MAIN_SHA,
    build,
)
from tools.pipeline9_candidates import (
    REQUIRED_SOURCE_SCOPES,
    accepted_decisions,
    promoted_properties,
)
from tools.property_cell_provenance import property_cell_support

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-11_NEXT_PROPERTY_BACKED_COHORT.json"
RECONCILIATION_PATH = ROOT / "reconciliation/pipeline11_next_repository_wide_cohort.json"
CLAIMS_PATH = ROOT / "sources/claims/generic-claims.json"
CANONICAL_SHA = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def artifact() -> dict[str, Any]:
    return json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))


@lru_cache(maxsize=1)
def claims() -> dict[str, dict[str, Any]]:
    return {
        item["claim_id"]: item
        for item in json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))["claims"]
    }


def test_acceptance_registry_includes_pipeline10_but_not_current_pipeline11() -> None:
    data = artifact()
    registry = json.loads((ROOT / "reconciliation/accepted-authority-sources.json").read_text())
    paths = {item["path"] for item in registry["sources"]}
    assert "reconciliation/pipeline10_next_repository_wide_cohort.json" in paths
    assert "reconciliation/pipeline11_next_repository_wide_cohort.json" not in paths
    accepted = accepted_decisions()
    assert any(item["decision_id"].startswith("pipeline9-") for item in accepted)
    assert any(item["decision_id"].startswith("pipeline10-") for item in accepted)
    assert not any(item["decision_id"].startswith("pipeline11-") for item in accepted)
    assert data["accepted_authority_transition"]["pipeline11_source_added"] is False
    assert data["accepted_authority_transition"]["decision_count_before"] == 43
    assert data["accepted_authority_transition"]["decision_count_after"] == 49


def test_h123_and_h100_are_zero_only_because_registry_authority_is_loaded() -> None:
    data = artifact()
    assert data["accepted_state_zero_reduction"]["pipeline9_h123"]["fresh_expected_reduction"] == 0
    assert data["accepted_state_zero_reduction"]["pipeline10_h100"]["fresh_expected_reduction"] == 0
    assert data["accepted_state_zero_reduction"]["pipeline9_h123"]["status"] == "already_accepted_zero_fresh_reduction"
    assert data["accepted_state_zero_reduction"]["pipeline10_h100"]["status"] == "already_accepted_zero_fresh_reduction"
    assert not any(
        item["table"] == "holding" and item["address"] in {100, 123}
        for item in data["candidate_ranking"]
    )


def test_pipeline11_fresh_rank_one_is_property_backed_and_path_deduplicated() -> None:
    data = artifact()
    selected = data["selected_cohort"]
    assert selected["id"] == data["candidate_ranking"][0]["id"]
    assert selected["id"] == "v124-row-holding-107-row-015-0108"
    assert selected["semantic_key"] == "control.q_v_response_delay"
    assert selected["canonical_physical_target_count"] == 6
    assert selected["applicability_path_count"] == 7
    assert selected["physical_parity"]["overall"] == {"selected": 6, "accounted_for": 6, "percent": 100}
    assert selected["applicability_path_coverage"] == {"selected": 7, "accounted_for": 7, "percent": 100}
    ranking = data["candidate_ranking"][0]
    assert len(ranking["authority_by_target"]) == selected["canonical_physical_target_count"]
    assert ranking["expected_reduction"] == selected["expected_reduction"]


def test_selected_properties_have_capable_noncanonical_claims_and_compatible_values() -> None:
    data = artifact()
    claims_by_id = claims()
    decisions = json.loads(RECONCILIATION_PATH.read_text())["decisions"]
    for decision in decisions:
        without_authority = {key: value for key, value in decision.items() if key != "authority_support"}
        derived = property_cell_support(without_authority, claims_by_id)
        for property_name, detail in decision["authority_support"].items():
            if detail["status"] != "supported":
                continue
            assert detail["claim_ids"]
            assert set(detail["claim_ids"]) <= set(derived[property_name]["claim_ids"])
            assert all(not claim_id.startswith("spec/") and "compatibility" not in claim_id for claim_id in detail["claim_ids"])
        row_claim = next(claims_by_id[claim_id] for claim_id in decision["support"] if claims_by_id[claim_id]["assertion"]["kind"] == "vendor_source_row")
        row_value = row_claim["assertion"]["value"]
        value = decision["decision"]["value"]
        assert value["unit"] == row_value["raw_unit_text"]
        assert value["access"] == row_value["raw_access_text"]
        assert value["semantic_key"] == data["selected_cohort"]["semantic_key"]


def test_all_scopes_and_ranges_remain_in_fresh_enumeration() -> None:
    data = artifact()
    assert set(data["repository_wide_coverage"]) == set(REQUIRED_SOURCE_SCOPES)
    assert sum(item["declared_range_count"] for item in data["repository_wide_coverage"].values()) == 33
    assert data["candidate_universe"]["candidate_count"] == 1194


def test_authority_moves_from_accepted_baseline_only_for_selected_cohort() -> None:
    data = artifact()
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    selected_before = data["authority"]["selected_before"]
    selected_after = data["authority"]["selected_after"]
    assert before == {"canonical_property_cells": 49867, "legacy_authoritative_property_cells": 49500, "declarative_authoritative_property_cells": 135, "legacy_exclusive_property_cells": 41}
    assert after["legacy_authoritative_property_cells"] < before["legacy_authoritative_property_cells"]
    assert after["declarative_authoritative_property_cells"] > before["declarative_authoritative_property_cells"]
    assert after["legacy_exclusive_property_cells"] == before["legacy_exclusive_property_cells"]
    assert selected_after["legacy_authoritative_property_cells"] < selected_before["legacy_authoritative_property_cells"]
    assert selected_before["legacy_authoritative_property_cells"] == 78
    assert selected_after["legacy_authoritative_property_cells"] == 54


@pytest.mark.slow
def test_lineage_canonical_freeze_and_determinism() -> None:
    data = artifact()
    assert data["lineage"]["starting_merged_main_sha"] == STARTING_MAIN_SHA
    assert data["lineage"]["accepted_pipeline10_tip_ancestor_sha"] == PIPELINE10_ACCEPTED_TIP_SHA
    assert data["canonical"] == {"path": "spec/growatt-register-spec.json", "sha256": CANONICAL_SHA, "canonical_modified": False}
    first_build, _ = build("test-generation-tip")
    second_build, _ = build("test-generation-tip")
    assert first_build == second_build
