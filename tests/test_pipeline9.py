"""Focused invariants for the repository-wide PIPELINE-9 cohort."""

from __future__ import annotations

from functools import lru_cache
import hashlib
import json
from pathlib import Path

import pytest
from tools.pipeline8_evidence import (
    SUPPORTED_QUALIFIED,
    SUPPORTED_UNCONDITIONAL,
    evaluate_applicability,
)
from tools.pipeline9_candidates import (
    REQUIRED_SOURCE_SCOPES,
    enumerate_candidates,
    path_key,
)

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SHA = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def artifact() -> dict:
    return json.loads(
        (ROOT / "docs/pipeline/data/GII-PIPELINE-9_REPOSITORY_WIDE_NEXT_COHORT.json").read_text()
    )


@lru_cache(maxsize=1)
def claims() -> list[dict]:
    return json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]


def test_enumeration_covers_all_v124_source_scopes_and_ranges() -> None:
    result = artifact()
    coverage = result["repository_wide_v124_coverage"]
    assert set(coverage) == set(REQUIRED_SOURCE_SCOPES)
    assert sum(item["declared_range_count"] for item in coverage.values()) == 33
    assert result["candidate_universe"]["non_min_candidate_count"] > 0


@pytest.mark.slow
def test_candidate_ranking_is_deterministic_and_repository_wide() -> None:
    first = enumerate_candidates()
    second = enumerate_candidates()
    assert first == second
    assert first["candidate_ranking"]
    assert any(set(item["source_scopes"]) - {"min_tl_xh"} for item in first["candidate_ranking"])


def test_source_scope_qualifiers_are_not_promoted_to_unconditional() -> None:
    claims_data = claims()
    qualified = evaluate_applicability(
        claims_data, "min_tl_xh", "holding", 3125, source_scope="min_tl_xh"
    )
    unconditional = evaluate_applicability(
        claims_data, "min_tl_xh", "holding", 3000, source_scope="min_tl_xh"
    )
    assert qualified["status"] == SUPPORTED_QUALIFIED
    assert not qualified["qualifier_context_known"]
    assert unconditional["status"] == SUPPORTED_UNCONDITIONAL


def test_max_1500v_scope_does_not_leak_to_generic_tl3_scope() -> None:
    claims_data = claims()
    specific = evaluate_applicability(
        claims_data, "tl3_max_mid_mac", "input", 900, source_scope="max_1500v_max_x_lv"
    )
    generic = evaluate_applicability(
        claims_data, "tl3_max_mid_mac", "input", 900, source_scope="tl3_max_mid_mac"
    )
    assert specific["status"] == SUPPORTED_UNCONDITIONAL
    assert generic["status"] == "NOT_SUPPORTED_BY_DECLARATION"


def test_shared_candidate_keeps_explicit_applicability_paths() -> None:
    selected = artifact()["selected_cohort"]
    assert selected["kind"] == "shared_vendor_row"
    assert set(selected["source_scopes"]) == set(REQUIRED_SOURCE_SCOPES)
    assert selected["canonical_physical_target_count"] == 6
    assert selected["applicability_path_count"] == 7
    assert {target["source_scope"] for target in selected["applicability_paths"]} == set(REQUIRED_SOURCE_SCOPES)
    tl3_paths = [
        target
        for target in selected["applicability_paths"]
        if target["canonical_family"] == "tl3_max_mid_mac"
    ]
    assert {target["source_scope"] for target in tl3_paths} == {
        "tl3_max_mid_mac",
        "max_1500v_max_x_lv",
    }
    assert {target["source_declaration"] for target in tl3_paths} == {
        "v124-instruction-tl3-max-mid-mac",
        "v124-instruction-max-1500v-max-x-lv",
    }
    assert selected["physical_parity"]["overall"]["percent"] == 100
    assert all(item["percent"] == 100 for item in selected["physical_parity"]["by_family"].values())
    assert selected["applicability_path_coverage"] == {
        "selected": 7,
        "accounted_for": 7,
        "percent": 100,
    }


def test_path_level_evidence_keys_do_not_collide() -> None:
    selected = artifact()["selected_cohort"]
    ranking = next(
        item for item in artifact()["candidate_ranking"] if item["id"] == selected["id"]
    )
    tl3_paths = [
        target
        for target in selected["applicability_paths"]
        if target["canonical_family"] == "tl3_max_mid_mac"
    ]
    keys = {path_key(target) for target in tl3_paths}
    assert len(keys) == 2
    assert keys <= set(ranking["evidence_dimensions"])
    assert keys <= set(ranking["properties_by_target"])


def test_selected_decisions_have_scope_consistent_applicability_support() -> None:
    data = artifact()
    claims = {
        claim["claim_id"]: claim
        for claim in json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]
    }
    decisions = json.loads(
        (ROOT / "reconciliation/pipeline9_repository_wide_next_cohort.json").read_text()
    )["decisions"]
    for decision in decisions:
        scope_paths = {
            (
                path["canonical_family"],
                path["table"],
                path["address"],
                path["source_scope"],
                path["source_declaration"],
            )
            for path in decision["scope"]["applicability_paths"]
        }
        cited_paths = {
            (
                claims[claim_id]["subject"]["family_scope"][0],
                claims[claim_id]["subject"]["table"],
                decision["target"]["address"],
                claims[claim_id]["subject"]["source_scope"],
                claims[claim_id]["subject"]["source_declaration"],
            )
            for claim_id in decision["support"]
            if claims[claim_id]["assertion"]["kind"] == "document_range_applicability"
        }
        assert cited_paths
        assert cited_paths <= scope_paths
        for claim_id in decision["support"]:
            claim = claims[claim_id]
            if claim["assertion"]["kind"] == "document_range_applicability":
                assert claim["subject"]["address"] <= decision["target"]["address"] <= claim["subject"]["address_end"]
        assert (
            decision["target"]["canonical_family"],
            decision["target"]["table"],
            decision["target"]["address"],
            decision["scope"]["source_scope"],
            decision["scope"]["source_declaration"],
        ) in scope_paths


def test_duplicate_paths_do_not_double_count_authority_reduction() -> None:
    selected = artifact()["selected_cohort"]
    ranking = next(item for item in artifact()["candidate_ranking"] if item["id"] == selected["id"])
    assert len(ranking["authority_by_target"]) == selected["canonical_physical_target_count"]
    assert selected["applicability_path_count"] > selected["canonical_physical_target_count"]
    assert ranking["expected_reduction"] == sum(
        item["expected_reduction"] for item in ranking["authority_by_target"].values()
    )
    assert ranking["expected_reduction"] == 30
    assert len(artifact()["semantic_parity"]) == 6


def test_promoted_properties_have_noncanonical_support_and_authority_moves() -> None:
    data = artifact()
    assert data["evidence"]["all_promoted_properties_have_noncanonical_support"]
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    selected_before = data["authority"]["selected_before"]
    selected_after = data["authority"]["selected_after"]
    assert after["legacy_authoritative_property_cells"] < before["legacy_authoritative_property_cells"]
    assert selected_after["legacy_authoritative_property_cells"] < selected_before["legacy_authoritative_property_cells"]


def test_canonical_sha_is_unchanged_and_pipeline8_decisions_remain_present() -> None:
    digest = hashlib.sha256((ROOT / "spec/growatt-register-spec.json").read_bytes()).hexdigest()
    assert digest == CANONICAL_SHA
    data = artifact()
    assert data["canonical"]["canonical_modified"] is False
    decisions = json.loads((ROOT / "reconciliation/resolved-assertions.json").read_text())["decisions"]
    decision_ids = {item["decision_id"] for item in decisions}
    previous = json.loads((ROOT / "reconciliation/min_tl_xh_holding_bdc_3070_3071_3095.json").read_text())["decisions"]
    assert {item["decision_id"] for item in previous} <= decision_ids
    assert data["correction_candidates"][0]["classification"] == "SUPPORTED_CANONICAL_CORRECTION_CANDIDATE"


def test_every_selected_decision_has_explicit_scope_and_source_support() -> None:
    data = artifact()
    claim_ids = {
        claim["claim_id"]
        for claim in json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]
    }
    selected_ids = set(data["selected_cohort"]["property_decisions"])
    decisions = {
        item["decision_id"]: item
        for item in json.loads((ROOT / "reconciliation/pipeline9_repository_wide_next_cohort.json").read_text())["decisions"]
    }
    assert selected_ids == set(decisions)
    for item in decisions.values():
        assert item["scope"]["source_scope"] in REQUIRED_SOURCE_SCOPES
        assert set(item["support"]) <= claim_ids
        assert item["support"]
