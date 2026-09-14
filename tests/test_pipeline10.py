"""Regression tests for the post-PIPELINE-9 repository-wide cohort."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from tools.build_authority_coverage import DECISION_PROPERTY_MAP
from tools.build_pipeline10a_audit import build as build_property_cell_audit
from tools.property_cell_provenance import property_cell_support, supported_property_cells
from tools.pipeline9_candidates import accepted_decisions, enumerate_candidates, path_key

ROOT = Path(__file__).resolve().parents[1]
ARTIFACT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-10_NEXT_REPOSITORY_WIDE_COHORT.json"
CLAIMS_PATH = ROOT / "sources/claims/generic-claims.json"
RESOLVED_PATH = ROOT / "reconciliation/resolved-assertions.json"
CANONICAL_SHA = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def artifact() -> dict[str, Any]:
    return json.loads(ARTIFACT_PATH.read_text(encoding="utf-8"))


def test_pipeline9_authority_is_included_and_h123_is_not_reducible_again() -> None:
    data = artifact()
    pipeline9_ids = {
        item["decision_id"]
        for item in json.loads(
            (ROOT / "reconciliation/pipeline9_repository_wide_next_cohort.json").read_text()
        )["decisions"]
    }
    accepted_ids = {item["decision_id"] for item in accepted_decisions()}
    assert pipeline9_ids <= accepted_ids
    assert data["accepted_authority"]["pipeline9_included"] is True
    assert data["previous_h123"]["current_expected_reduction"] == 0
    assert data["previous_h123"]["current_candidate_rank"] is None


def test_fresh_enumeration_remains_repository_wide_and_deterministic() -> None:
    first = enumerate_candidates()
    second = enumerate_candidates()
    assert first == second
    assert set(first["coverage"]) == {
        "max_1500v_max_x_lv",
        "min_tl_xh",
        "mod_tl3_xh",
        "storage_mix",
        "storage_spa",
        "storage_sph",
        "tl3_max_mid_mac",
    }
    assert sum(item["declared_range_count"] for item in first["coverage"].values()) == 33


def test_selected_cohort_is_current_bounded_rank_one_with_separate_identities() -> None:
    selected = artifact()["selected_cohort"]
    assert selected["rank"] == 1
    assert selected["bounded"] is True
    assert selected["source_conflict"] is False
    assert selected["canonical_physical_target_count"] == 6
    assert selected["applicability_path_count"] == 7
    assert selected["physical_units"] == 6
    assert selected["physical_parity"]["overall"] == {"selected": 6, "accounted_for": 6, "percent": 100}
    assert selected["applicability_path_coverage"] == {
        "selected": 7,
        "accounted_for": 7,
        "percent": 100,
    }
    assert len({path_key(path) for path in selected["applicability_paths"]}) == 7
    assert len({
        (target["canonical_family"], target["table"], target["address"])
        for target in selected["physical_targets"]
    }) == 6


def test_selected_decision_provenance_matches_every_retained_applicability_path() -> None:
    data = artifact()
    claims = {
        claim["claim_id"]: claim for claim in json.loads(CLAIMS_PATH.read_text())["claims"]
    }
    decisions = json.loads(
        (ROOT / "reconciliation/pipeline10_next_repository_wide_cohort.json").read_text()
    )["decisions"]
    for decision in decisions:
        paths = {
            (
                path["canonical_family"],
                path["table"],
                path["address"],
                path["source_scope"],
                path["source_declaration"],
            )
            for path in decision["scope"]["applicability_paths"]
        }
        applicability_claims = [
            claims[claim_id]
            for claim_id in decision["support"]
            if claims[claim_id]["assertion"]["kind"] == "document_range_applicability"
        ]
        cited = {
            (
                claim["subject"]["family_scope"][0],
                claim["subject"]["table"],
                decision["target"]["address"],
                claim["subject"]["source_scope"],
                claim["subject"]["source_declaration"],
            )
            for claim in applicability_claims
        }
        assert cited <= paths
        assert (
            decision["target"]["canonical_family"],
            decision["target"]["table"],
            decision["target"]["address"],
            decision["scope"]["source_scope"],
            decision["scope"]["source_declaration"],
        ) in paths
    assert data["evidence"]["all_promoted_properties_have_noncanonical_support"] is True


def test_duplicate_paths_do_not_double_count_and_h3085_stays_deferred() -> None:
    data = artifact()
    selected = data["selected_cohort"]
    ranking = next(item for item in data["candidate_ranking"] if item["id"] == selected["id"])
    assert selected["applicability_path_count"] > selected["canonical_physical_target_count"]
    assert ranking["expected_reduction"] == sum(
        item["expected_reduction"] for item in ranking["authority_by_target"].values()
    )
    assert data["semantic_parity_summary"] == {"PARITY_MATCH": 6}
    assert data["correction_candidates"] == [
        {
            "physical_id": "min_tl_xh:holding:3085",
            "classification": "SUPPORTED_CANONICAL_CORRECTION_CANDIDATE",
            "disposition": "deferred; canonical remains frozen",
        }
    ]


def test_authority_moves_without_changing_canonical_or_pipeline9_resolution() -> None:
    data = artifact()
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    assert after["legacy_authoritative_property_cells"] < before["legacy_authoritative_property_cells"]
    assert after["declarative_authoritative_property_cells"] > before["declarative_authoritative_property_cells"]
    assert after["legacy_exclusive_property_cells"] == before["legacy_exclusive_property_cells"]
    assert data["canonical"]["sha256"] == CANONICAL_SHA
    assert data["canonical"]["canonical_modified"] is False
    resolved = json.loads(RESOLVED_PATH.read_text())
    resolved_ids = {item["decision_id"] for item in resolved["decisions"]}
    pipeline9_ids = {
        item["decision_id"]
        for item in json.loads(
            (ROOT / "reconciliation/pipeline9_repository_wide_next_cohort.json").read_text()
        )["decisions"]
    }
    assert pipeline9_ids <= resolved_ids


def test_semantic_mapping_does_not_expand_to_the_legacy_property_set() -> None:
    claims = {
        claim["claim_id"]: claim
        for claim in json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))["claims"]
    }
    row_claim = next(
        claim
        for claim in claims.values()
        if claim["assertion"]["kind"] == "vendor_source_row"
        and claim["subject"].get("table") == "holding"
        and claim["subject"].get("address") == 10
    )
    decision = {
        "target": {"property": "semantic_mapping"},
        "support": [row_claim["claim_id"]],
        "decision": {"value": {"signedness": "unsigned", "unit": None}},
    }
    supported = supported_property_cells(decision, claims)
    assert supported == {"human_description", "physical_quantity"}
    assert supported < DECISION_PROPERTY_MAP["semantic_mapping"]
    assert "signedness" not in property_cell_support(decision, claims)
    assert "unit" not in supported
    assert "normalization" not in supported


def test_canonical_only_values_cannot_become_property_support() -> None:
    claims = {
        claim["claim_id"]: claim
        for claim in json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))["claims"]
    }
    decision = {
        "target": {"property": "semantic_mapping"},
        "support": [],
        "decision": {
            "value": {
                "signedness": "signed",
                "unit": "W",
                "normalization": "source_semantics_preserved",
            }
        },
    }
    assert supported_property_cells(decision, claims) == set()


def test_every_accepted_promoted_cell_has_real_noncanonical_support() -> None:
    claims = {
        claim["claim_id"]: claim
        for claim in json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))["claims"]
    }
    audit = build_property_cell_audit()
    for item in audit["decisions"]:
        support = item["support_claim_ids_by_property"]
        assert set(item["correctly_evidence_supported_property_cells"]) == set(support)
        for property_name in item["correctly_evidence_supported_property_cells"]:
            claim_ids = support[property_name]
            assert claim_ids
            assert all(claim_id in claims for claim_id in claim_ids)
            assert all(
                not claim_id.startswith("spec/") and "compatibility" not in claim_id
                for claim_id in claim_ids
            )


def test_accepted_authority_registry_excludes_unaccepted_pipeline10() -> None:
    first = accepted_decisions()
    second = accepted_decisions()
    assert first == second
    assert all(not item["decision_id"].startswith("pipeline10-") for item in first)
    assert len(first) == 43


def test_property_cell_rebaseline_records_h123_h10_and_corrected_rank_one() -> None:
    data = artifact()
    accounting = data["property_cell_accounting"]
    assert accounting["mode"] == "explicit_property_cell_support"
    assert accounting["h123"]["historical_broad_expected_reduction"] == 30
    assert accounting["h123"]["corrected_expected_reduction"] == 24
    assert accounting["h10"]["historical_broad_expected_reduction"] == 30
    assert accounting["h10"]["corrected_expected_reduction"] == 12
    assert data["selected_cohort"]["id"] == data["candidate_ranking"][0]["id"]
    assert accounting["over_promoted_cells_removed"] == 88
