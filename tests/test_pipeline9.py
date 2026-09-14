"""Focused invariants for the repository-wide PIPELINE-9 cohort."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.pipeline8_evidence import SUPPORTED_QUALIFIED, SUPPORTED_UNCONDITIONAL, evaluate_applicability
from tools.pipeline9_candidates import REQUIRED_SOURCE_SCOPES, enumerate_candidates

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SHA = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def artifact() -> dict:
    return json.loads(
        (ROOT / "docs/pipeline/data/GII-PIPELINE-9_REPOSITORY_WIDE_NEXT_COHORT.json").read_text()
    )


def test_enumeration_covers_all_v124_source_scopes_and_ranges() -> None:
    result = enumerate_candidates()
    assert set(result["source_scopes"]) == set(REQUIRED_SOURCE_SCOPES)
    assert sum(item["declared_range_count"] for item in result["coverage"].values()) == 33
    assert result["candidate_universe"]["non_min_candidate_count"] > 0


def test_candidate_ranking_is_deterministic_and_repository_wide() -> None:
    first = enumerate_candidates()
    second = enumerate_candidates()
    assert first == second
    assert first["candidate_ranking"]
    assert any(set(item["source_scopes"]) - {"min_tl_xh"} for item in first["candidate_ranking"])


def test_source_scope_qualifiers_are_not_promoted_to_unconditional() -> None:
    claims = json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]
    qualified = evaluate_applicability(
        claims, "min_tl_xh", "holding", 3125, source_scope="min_tl_xh"
    )
    unconditional = evaluate_applicability(
        claims, "min_tl_xh", "holding", 3000, source_scope="min_tl_xh"
    )
    assert qualified["status"] == SUPPORTED_QUALIFIED
    assert not qualified["qualifier_context_known"]
    assert unconditional["status"] == SUPPORTED_UNCONDITIONAL


def test_max_1500v_scope_does_not_leak_to_generic_tl3_scope() -> None:
    claims = json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]
    specific = evaluate_applicability(
        claims, "tl3_max_mid_mac", "input", 900, source_scope="max_1500v_max_x_lv"
    )
    generic = evaluate_applicability(
        claims, "tl3_max_mid_mac", "input", 900, source_scope="tl3_max_mid_mac"
    )
    assert specific["status"] == SUPPORTED_UNCONDITIONAL
    assert generic["status"] == "NOT_SUPPORTED_BY_DECLARATION"


def test_shared_candidate_keeps_explicit_applicability_paths() -> None:
    selected = artifact()["selected_cohort"]
    assert selected["kind"] == "shared_vendor_row"
    assert set(selected["source_scopes"]) == set(REQUIRED_SOURCE_SCOPES)
    assert {target["source_scope"] for target in selected["targets"]} == set(REQUIRED_SOURCE_SCOPES)
    assert selected["physical_parity"]["overall"]["percent"] == 100
    assert all(item["percent"] == 100 for item in selected["physical_parity"]["by_family"].values())


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
