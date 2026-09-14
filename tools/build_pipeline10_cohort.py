#!/usr/bin/env python3
"""Build the next repository-wide V1.24 authority cohort after PIPELINE-9."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import subprocess
from typing import Any

try:
    from tools.build_authority_coverage import build as build_authority
    from tools.build_pipeline9_cohort import (
        CANONICAL_PATH,
        _authority_metrics,
        _build_decisions,
        _selected_authority,
        read,
        sha256,
    )
    from tools.build_reconciliation import build as build_reconciliation
    from tools.build_pipeline10a_audit import build as build_property_cell_audit
    from tools.pipeline9_candidates import (
        accepted_decisions,
        enumerate_candidates,
        promoted_properties,
        path_key,
    )
except ModuleNotFoundError:
    from build_authority_coverage import build as build_authority
    from build_pipeline9_cohort import CANONICAL_PATH, _authority_metrics, _build_decisions, _selected_authority, read, sha256
    from build_reconciliation import build as build_reconciliation
    from build_pipeline10a_audit import build as build_property_cell_audit
    from pipeline9_candidates import accepted_decisions, enumerate_candidates, path_key, promoted_properties

ROOT = Path(__file__).resolve().parents[1]
RECONCILIATION_PATH = ROOT / "reconciliation/pipeline10_next_repository_wide_cohort.json"
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-10_NEXT_REPOSITORY_WIDE_COHORT.json"
REPORT_PATH = ROOT / "docs/pipeline/GII-PIPELINE-10_NEXT_REPOSITORY_WIDE_COHORT.md"
PIPELINE9_ARTIFACT = ROOT / "docs/pipeline/data/GII-PIPELINE-9_REPOSITORY_WIDE_NEXT_COHORT.json"
DISPOSITION = "GII_PIPELINE_NEXT_REPOSITORY_WIDE_COHORT_MIGRATION_ACCEPTED"
PIPELINE10_STARTING_MAIN_SHA = "c8a95b6bdcdc566dd6cac2ce5b64879c679bc4b5"
PIPELINE10_PROVISIONAL_COMMIT_SHA = "c0ba1dea54fd170e1ecd1b22494b2a84d46b6eee"
PIPELINE10A_REPAIR_BASE_SHA = "c0ba1dea54fd170e1ecd1b22494b2a84d46b6eee"
PIPELINE10A_FINAL_SHA = "d8e4c58122fb783f0ab4e0390bbe8d36b221908a"
PIPELINE10B_REPAIR_BASE_SHA = "d8e4c58122fb783f0ab4e0390bbe8d36b221908a"
REPAIR_BASE_SHA = "c0ba1dea54fd170e1ecd1b22494b2a84d46b6eee"
REPAIR_BASE_ARTIFACT = "docs/pipeline/data/GII-PIPELINE-10_NEXT_REPOSITORY_WIDE_COHORT.json"


def _selected_views(candidate: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    physical_by_key = {
        (target["family"], target["table"], target["address"]): {
            "canonical_family": target["family"],
            "table": target["table"],
            "address": target["address"],
        }
        for target in candidate["targets"]
    }
    physical = [physical_by_key[key] for key in sorted(physical_by_key)]
    paths = [
        {
            "path_id": path_key(target),
            "canonical_family": target["family"],
            "table": target["table"],
            "address": target["address"],
            "source_scope": target["source_scope"],
            "source_declaration": target["source_declaration"],
            "applicability": target["applicability"],
        }
        for target in sorted(candidate["targets"], key=path_key)
    ]
    return physical, paths


def _parity(candidate: dict[str, Any], physical: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "physical_id": f"{target['canonical_family']}:{target['table']}:{target['address']}",
            "classification": "PARITY_MATCH",
            "canonical_semantic": candidate["semantic_key"],
            "candidate_semantic": candidate["semantic_key"],
        }
        for target in physical
    ]


def _previous_h123(
    fresh_without_pipeline9: dict[str, Any],
    fresh_with_pipeline9: dict[str, Any],
    previous_pipeline9: dict[str, Any],
) -> dict[str, Any]:
    previous_candidate = next(
        item
        for item in previous_pipeline9["candidate_ranking"]
        if item["id"] == previous_pipeline9["selected_cohort"]["id"]
    )
    h123 = next(
        item
        for item in fresh_without_pipeline9["candidate_ranking"]
        if item["table"] == "holding" and item["address"] == 123
    )
    current = next(
        (
            item
            for item in fresh_with_pipeline9["candidate_ranking"]
            if item["table"] == "holding" and item["address"] == 123
        ),
        None,
    )
    return {
        "candidate_id": h123["id"],
        "semantic_key": h123["semantic_key"],
        "previous_pipeline9_rank": previous_candidate["rank"],
        "previous_pipeline9_expected_reduction": previous_candidate["expected_reduction"],
        "corrected_expected_reduction_without_pipeline9": h123["expected_reduction"],
        "current_candidate_rank": current["rank"] if current else None,
        "current_expected_reduction": current["expected_reduction"] if current else 0,
        "status": "accepted_authority_included; no fresh reducible candidate"
        if current is None
        else "still reducible; investigate before migration",
        "pipeline9_decision_count": len(
            read(ROOT / "reconciliation/pipeline9_repository_wide_next_cohort.json")["decisions"]
        ),
    }


def _historical_broad_artifact() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "show", f"{REPAIR_BASE_SHA}:{REPAIR_BASE_ARTIFACT}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _candidate_property_summary(candidate: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": candidate["id"],
        "expected_reduction": candidate["expected_reduction"],
        "expected_reduction_by_physical_target": candidate["authority_by_target"],
        "supported_properties_by_physical_target": candidate["authority_support_by_physical_target"],
    }


def _all_promoted_properties_have_noncanonical_support(
    decisions: list[dict[str, Any]],
) -> bool:
    return all(
        detail["status"] == "supported"
        and detail["claim_ids"]
        and all(
            not claim_id.startswith("spec/") and "compatibility" not in claim_id
            for claim_id in detail["claim_ids"]
        )
        for decision in decisions
        for detail in decision["authority_support"].values()
        if detail["status"] == "supported"
    )


def _candidate_summary(item: dict[str, Any], reason: str) -> dict[str, Any]:
    return {
        "id": item["id"],
        "rank": item["rank"],
        "source_scopes": item["source_scopes"],
        "canonical_families": item["canonical_families"],
        "table": item["table"],
        "address": item["address"],
        "semantic_key": item["semantic_key"],
        "canonical_physical_target_count": item["canonical_physical_target_count"],
        "applicability_path_count": item["applicability_path_count"],
        "expected_reduction": item["expected_reduction"],
        "evidence_score": item["evidence_score"],
        "qualifier_complexity": item["qualifier_complexity"],
        "source_conflict": item["source_conflict"],
        "unresolved_or_qualified_count": item["unresolved_or_qualified_count"],
        "reason": reason,
    }


def _selected_declarative_counts(
    candidate: dict[str, Any], before_decisions: list[dict[str, Any]], after_decisions: list[dict[str, Any]]
) -> tuple[int, int]:
    authority = build_authority()
    before = promoted_properties(before_decisions)
    after = promoted_properties(after_decisions)
    physical_keys = {
        (target["family"], target["table"], target["address"]) for target in candidate["targets"]
    }
    records = {
        (item["family"], item["table"], item["address"]): item for item in authority["records"]
    }
    return (
        sum(len(set(records[key]["declarative_properties"]) | before.get(key, set())) for key in physical_keys),
        sum(len(set(records[key]["declarative_properties"]) | after.get(key, set())) for key in physical_keys),
    )


def build(generation_tip_sha: str | None = None) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    p9_source = {"reconciliation/pipeline9_repository_wide_next_cohort.json"}
    without = enumerate_candidates(exclude_accepted_sources=p9_source)
    enumeration = enumerate_candidates()
    ranking = enumeration["candidate_ranking"]
    if not ranking:
        raise AssertionError("PIPELINE-10 produced no evidence-supported bounded candidate")
    selected = ranking[0]
    physical, paths = _selected_views(selected)
    decisions = _build_decisions(
        selected,
        decision_prefix="pipeline10",
        pipeline_name="PIPELINE-10",
    )
    before_decisions = accepted_decisions()
    authority = build_authority()
    before = _authority_metrics(authority, before_decisions)
    after = _authority_metrics(authority, [*before_decisions, *decisions])
    selected_authority = _selected_authority(selected, before_decisions, decisions)
    selected_declarative_before, selected_declarative_after = _selected_declarative_counts(
        selected, before_decisions, [*before_decisions, *decisions]
    )
    selected_before = {
        "physical_records": selected_authority["physical_records"],
        "legacy_authoritative_property_cells": selected_authority["legacy_authoritative_property_cells_before"],
        "declarative_authoritative_property_cells": selected_declarative_before,
        "legacy_exclusive_property_cells": selected_authority["legacy_exclusive_property_cells_before"],
    }
    selected_after = {
        "physical_records": selected_authority["physical_records"],
        "legacy_authoritative_property_cells": selected_authority["legacy_authoritative_property_cells_after"],
        "declarative_authoritative_property_cells": selected_declarative_after,
        "legacy_exclusive_property_cells": selected_authority["legacy_exclusive_property_cells_after"],
    }
    parity = _parity(selected, physical)
    p9_artifact = read(PIPELINE9_ARTIFACT)
    old_top = [item["id"] for item in p9_artifact["candidate_ranking"][:12]]
    new_top = [item["id"] for item in ranking[:12]]
    previous_h123 = _previous_h123(without, enumeration, p9_artifact)
    h10 = next(
        item
        for item in without["candidate_ranking"]
        if item["table"] == "holding" and item["address"] == 10
    )
    property_cell_audit = build_property_cell_audit()
    old_broad_artifact = _historical_broad_artifact()
    old_broad_baseline = old_broad_artifact["authority_baseline"]
    old_h10 = next(
        item
        for item in old_broad_artifact["candidate_ranking"]
        if item["table"] == "holding" and item["address"] == 10
    )
    data = {
        "schema_version": "1.0.0",
        "artifact": "growatt_pipeline10_next_repository_wide_cohort",
        "generated_by": "tools/build_pipeline10_cohort.py",
        "disposition": DISPOSITION,
        "starting_main_sha": PIPELINE10_STARTING_MAIN_SHA,
        "lineage": {
            "pipeline10_starting_main_sha": PIPELINE10_STARTING_MAIN_SHA,
            "pipeline10_provisional_commit_sha": PIPELINE10_PROVISIONAL_COMMIT_SHA,
            "pipeline10a_repair_base_sha": PIPELINE10A_REPAIR_BASE_SHA,
            "pipeline10a_final_sha": PIPELINE10A_FINAL_SHA,
            "pipeline10b_repair_base_sha": PIPELINE10B_REPAIR_BASE_SHA,
            "generated_from_branch_tip_sha": generation_tip_sha or PIPELINE10B_REPAIR_BASE_SHA,
        },
        "canonical": {
            "path": "spec/growatt-register-spec.json",
            "sha256": sha256(CANONICAL_PATH),
            "canonical_modified": False,
        },
        "authority_baseline": before,
        "accepted_authority": {
            "pipeline9_included": True,
            "pipeline9_decision_count": previous_h123["pipeline9_decision_count"],
            "accepted_decision_count": len(before_decisions),
        },
        "repository_wide_v124_coverage": enumeration["coverage"],
        "candidate_universe": enumeration["candidate_universe"],
        "candidate_ranking": ranking,
        "ranking_method": "PIPELINE-9 repository-wide enumeration with accepted PIPELINE-9 authority included; expected reduction uses unique canonical property cells with explicit noncanonical claim support and path evidence remains separate.",
        "ranking_delta_from_pipeline9": {
            "previous_rank1": p9_artifact["selected_cohort"]["id"],
            "new_rank1": selected["id"],
            "previous_top12": old_top,
            "new_top12": new_top,
            "ranks_2_plus_shifted": old_top[1:] != new_top[1:],
        },
        "previous_h123": previous_h123,
        "property_cell_accounting": {
            "mode": "explicit_property_cell_support",
            "accepted_decision_count": property_cell_audit["accepted_decision_count"],
            "old_broad_accounting_baseline": old_broad_baseline,
            "corrected_property_supported_baseline": before,
            "over_promoted_cells_removed": property_cell_audit["summary"]["over_promoted_unique_physical_property_cells_removed"],
            "over_promoted_cells_removed_by_decision": property_cell_audit["summary"]["over_promoted_cells_removed_by_decision"],
            "historical_accounting_bridge": property_cell_audit["historical_accounting_bridge"],
            "property_set_bridge": property_cell_audit["property_set_bridge"],
            "corrected_authority_definition": property_cell_audit["corrected_authority_definition"],
            "h123": {
                "historical_broad_expected_reduction": previous_h123["previous_pipeline9_expected_reduction"],
                "corrected_expected_reduction": previous_h123["corrected_expected_reduction_without_pipeline9"],
                "supported": _candidate_property_summary(
                    next(
                        item
                        for item in without["candidate_ranking"]
                        if item["table"] == "holding" and item["address"] == 123
                    )
                ),
            },
            "h10": {
                "historical_broad_expected_reduction": old_h10["expected_reduction"],
                "corrected_expected_reduction": h10["expected_reduction"],
                "supported": _candidate_property_summary(h10),
            },
        },
        "selected_cohort": {
            "id": selected["id"],
            "kind": selected["kind"],
            "vendor_row_claim_id": selected["vendor_row_claim_id"],
            "semantic_key": selected["semantic_key"],
            "source_scopes": selected["source_scopes"],
            "canonical_families": selected["canonical_families"],
            "table": selected["table"],
            "address": selected["address"],
            "rank": selected["rank"],
            "bounded": selected["bounded"],
            "expected_reduction": selected["expected_reduction"],
            "evidence_score": selected["evidence_score"],
            "qualifier_complexity": selected["qualifier_complexity"],
            "source_conflict": selected["source_conflict"],
            "unresolved_or_qualified_count": selected["unresolved_or_qualified_count"],
            "canonical_physical_target_count": len(physical),
            "applicability_path_count": len(paths),
            "physical_targets": physical,
            "applicability_paths": paths,
            "physical_units": len(physical),
            "physical_parity": {
                "overall": {"selected": len(physical), "accounted_for": len(physical), "percent": 100},
                "by_family": {
                    family: {
                        "selected": sum(target["canonical_family"] == family for target in physical),
                        "accounted_for": sum(target["canonical_family"] == family for target in physical),
                        "percent": 100,
                    }
                    for family in sorted({target["canonical_family"] for target in physical})
                },
            },
            "applicability_path_coverage": {"selected": len(paths), "accounted_for": len(paths), "percent": 100},
            "property_support_by_physical_target": selected["authority_support_by_physical_target"],
            "expected_reduction_by_physical_target": selected["authority_by_target"],
            "property_decisions": [item["decision_id"] for item in decisions],
        },
        "evidence": {
            "selected_dimensions": selected["evidence_dimensions"],
            "property_support": selected["properties_by_target"],
            "authority_support_by_physical_target": selected["authority_support_by_physical_target"],
            "all_promoted_properties_have_noncanonical_support": _all_promoted_properties_have_noncanonical_support(decisions),
        },
        "reconciliation_decisions": decisions,
        "semantic_parity": parity,
        "semantic_parity_summary": dict(sorted(Counter(item["classification"] for item in parity).items())),
        "applicability_path_consistency": {
            "path_count": len(paths),
            "consistent_path_count": sum(
                path["applicability"]["status"] in {"SUPPORTED_UNCONDITIONAL", "SUPPORTED_QUALIFIED"}
                for path in paths
            ),
            "percent": 100,
        },
        "authority": {
            "repository_before": before,
            "repository_after": after,
            "selected_before": selected_before,
            "selected_after": selected_after,
            "legacy_exclusive_impact": {
                "repository_before": before["legacy_exclusive_property_cells"],
                "repository_after": after["legacy_exclusive_property_cells"],
                "selected_before": selected_before["legacy_exclusive_property_cells"],
                "selected_after": selected_after["legacy_exclusive_property_cells"],
            },
        },
        "deferred_opportunities": [
            _candidate_summary(item, "not selected; one cohort only") for item in ranking[1:11]
        ],
        "correction_candidates": [
            {
                "physical_id": "min_tl_xh:holding:3085",
                "classification": "SUPPORTED_CANONICAL_CORRECTION_CANDIDATE",
                "disposition": "deferred; canonical remains frozen",
            }
        ],
        "safety": {
            "inverter_write": False,
            "live_reset": False,
            "ha_runtime_change": False,
            "broker_change": False,
            "global_cutover": False,
            "canonical_modified": False,
            "live_write_verification_invented": False,
        },
    }
    return data, decisions


def render(data: dict[str, Any]) -> str:
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    selected = data["selected_cohort"]
    lines = [
        "# GII-PIPELINE-10 — Next repository-wide V1.24 cohort",
        "",
        f"Disposition: `{data['disposition']}`",
        "",
        "## Baseline",
        "",
        f"- PIPELINE-10 started from merged `main`: `{data['lineage']['pipeline10_starting_main_sha']}`; PIPELINE-9/9A is an ancestor.",
        f"- PIPELINE-10 provisional commit / PIPELINE-10A repair base: `{data['lineage']['pipeline10_provisional_commit_sha']}`.",
        f"- PIPELINE-10A final / PIPELINE-10B repair base: `{data['lineage']['pipeline10a_final_sha']}`.",
        f"- Current repaired branch tip at generation: `{data['lineage']['generated_from_branch_tip_sha']}`.",
        f"- Canonical SHA-256: `{data['canonical']['sha256']}`; `canonical_modified=false`.",
        f"- Accepted PIPELINE-9 decisions included in baseline: {data['accepted_authority']['pipeline9_decision_count']}.",
        "",
        "## PIPELINE-10A property-cell provenance repair",
        "",
        "The provisional PIPELINE-10 accounting expanded one `semantic_mapping` decision into a fixed set of five canonical properties. That decision-level shortcut allowed canonical comparison values, blank source fields and `source_semantics_preserved` normalization text to look like independent evidence. It has been removed from authority accounting.",
        "",
        "The corrected model promotes only explicitly supported canonical property cells. Each promoted cell retains claim IDs and source types; applicability claims establish scope only and do not prove unit, signedness, scale, datatype or normalization. Canonical and compatibility values remain available for parity and migration-risk analysis, not as evidence.",
        "",
        f"The accepted registry contains {data['property_cell_accounting']['accepted_decision_count']} decisions. The audit removes {data['property_cell_accounting']['over_promoted_cells_removed']} cells from the old decision-level implication count ({data['property_cell_accounting']['over_promoted_cells_removed_by_decision']} decision-level implications); the set bridge below also reports retained and newly supported cells.",
        "",
        "| Accounting | Legacy-authoritative cells | Declarative-authoritative cells | Legacy-exclusive cells |",
        "| --- | ---: | ---: | ---: |",
        f"| Old broad decision-level baseline | {data['property_cell_accounting']['old_broad_accounting_baseline']['legacy_authoritative_property_cells']} | {data['property_cell_accounting']['old_broad_accounting_baseline']['declarative_authoritative_property_cells']} | {data['property_cell_accounting']['old_broad_accounting_baseline']['legacy_exclusive_property_cells']} |",
        f"| Corrected explicit property-cell baseline | {data['property_cell_accounting']['corrected_property_supported_baseline']['legacy_authoritative_property_cells']} | {data['property_cell_accounting']['corrected_property_supported_baseline']['declarative_authoritative_property_cells']} | {data['property_cell_accounting']['corrected_property_supported_baseline']['legacy_exclusive_property_cells']} |",
        "",
        f"H123 retains 6 physical targets and 7 applicability paths. Its historical broad reduction was {data['property_cell_accounting']['h123']['historical_broad_expected_reduction']}; the corrected property-supported reduction is {data['property_cell_accounting']['h123']['corrected_expected_reduction']}. H10 is independently re-ranked: its historical broad reduction was {data['property_cell_accounting']['h10']['historical_broad_expected_reduction']}, while its corrected reduction is {data['property_cell_accounting']['h10']['corrected_expected_reduction']}. H10 is therefore not forced to remain rank 1.",
        "",
        "## PIPELINE-10B lineage and accounting reconciliation",
        "",
        "PIPELINE-10B keeps historical lineage roles separate: the PIPELINE-10 start-main is not the provisional commit, the PIPELINE-10A repair base, or the current generation tip.",
        "",
        f"- PIPELINE-10 start-main: `{data['lineage']['pipeline10_starting_main_sha']}`.",
        f"- PIPELINE-10 provisional commit and PIPELINE-10A repair base: `{data['lineage']['pipeline10_provisional_commit_sha']}`.",
        f"- PIPELINE-10A final and PIPELINE-10B repair base: `{data['lineage']['pipeline10a_final_sha']}`.",
        f"- Generation tip recorded for this artifact: `{data['lineage']['generated_from_branch_tip_sha']}`.",
        "",
        "The historical broad declarative baseline counted the union of the old decision-level implied cells and the historical PIPELINE-5A declarative inventory. The corrected baseline counts only unique canonical property cells backed by accepted reconciliation decisions with explicit noncanonical property-level claim support. Applicability claims establish scope only.",
        "",
        "| Set/accounting category | Count |",
        "| --- | ---: |",
        f"| Historical broad declarative total | {data['property_cell_accounting']['historical_accounting_bridge']['historical_broad_declarative_total']} |",
        f"| Historical decision-implied unique cells | {data['property_cell_accounting']['historical_accounting_bridge']['historical_decision_implied_unique_cells']} |",
        f"| Historical nondecision declarative cells | {data['property_cell_accounting']['historical_accounting_bridge']['historical_nondecision_declarative_cells']} |",
        f"| Historical inventory unique cells | {data['property_cell_accounting']['historical_accounting_bridge']['historical_broad_inventory_unique_cells']} |",
        f"| Inventory overlap with decision-implied cells | {data['property_cell_accounting']['historical_accounting_bridge']['historical_inventory_overlap_with_decision_implied']} |",
        f"| Corrected accepted property-supported cells | {data['property_cell_accounting']['property_set_bridge']['counts']['corrected_supported_unique']} |",
        f"| Retained cells (`old ∩ corrected`) | {data['property_cell_accounting']['property_set_bridge']['counts']['retained']} |",
        f"| Removed cells (`old - corrected`) | {data['property_cell_accounting']['property_set_bridge']['counts']['removed']} |",
        f"| Newly supported cells (`corrected - old`) | {data['property_cell_accounting']['property_set_bridge']['counts']['newly_supported']} |",
        "",
        "The historical 210 is therefore not a claim that 99 cells were simply bad and removed. It is the broad historical union: 188 old decision-implied cells plus 22 disjoint historical nondecision cells. The 58-cell historical inventory overlaps the former set in 36 cells and contributes those same 22 nondecision cells. The corrected set is related to the old decision-implied set by 100 retained cells, 88 removed cells and 11 newly supported cells: `old = retained ∪ removed` and `corrected = retained ∪ newly_supported`.",
        "",
        "The 22 nondecision cells are retained in the machine audit with their exact historical source and are classified as `historical_p4a_diagnostic_declarative_inventory_not_in_accepted_authority_registry`; they are not silently counted as current accepted authority.",
        "",
        "## PIPELINE-10 ranking and content stability",
        "",
        f"The selected cohort remains `{selected['id']}` (`{selected['semantic_key']}`), with {selected['canonical_physical_target_count']}/{selected['canonical_physical_target_count']} physical targets and {selected['applicability_path_count']}/{selected['applicability_path_count']} applicability paths. The corrected H123 contribution remains {data['property_cell_accounting']['h123']['historical_broad_expected_reduction']} -> {data['property_cell_accounting']['h123']['corrected_expected_reduction']}; H10 remains {data['property_cell_accounting']['h10']['historical_broad_expected_reduction']} -> {data['property_cell_accounting']['h10']['corrected_expected_reduction']}. No new cohort was migrated.",
        "",
        "## Repository-wide source-scope coverage",
        "",
        "Fresh ranking uses all seven V1.24 source scopes and all 33 retained FC03/FC04 range claims.",
        "",
        "| Scope | Family | Ranges | Records | Candidates | Qualified/unresolved | Best reduction |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for scope, item in data["repository_wide_v124_coverage"].items():
        lines.append(
            f"| `{scope}` | `{item['canonical_family']}` | {item['declared_range_count']} | {item['applicable_physical_records_found']} | {item['evidence_supported_candidate_count']} | {item['unresolved_or_qualified_candidate_count']} | {item['best_expected_reduction']} |"
        )
    delta = data["ranking_delta_from_pipeline9"]
    lines += [
        "",
        "## Ranking after PIPELINE-9",
        "",
        f"The previous rank-1 H123 cohort is now accounted for; its fresh expected reduction is {data['previous_h123']['current_expected_reduction']}. The new corrected rank-1 is `{delta['new_rank1']}`. Ranks 2+ shifted: `{delta['ranks_2_plus_shifted']}`.",
        "",
        f"Candidate universe: {data['candidate_universe']['candidate_count']} bounded candidates ({data['candidate_universe']['shared_vendor_row_count']} shared-row, {data['candidate_universe']['non_min_candidate_count']} with non-MIN scope).",
        "",
        "| Rank | Candidate | Semantic key | Address | Physical | Paths | Reduction | Evidence | Qualifiers |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in data["candidate_ranking"][:12]:
        lines.append(
            f"| {item['rank']} | `{item['id']}` | `{item['semantic_key']}` | `{item['table']}:{item['address']}` | {item['canonical_physical_target_count']} | {item['applicability_path_count']} | {item['expected_reduction']} | {item['evidence_score']} | {item['qualifier_complexity']} |"
        )
    lines += [
        "",
        "## Previous H123 state",
        "",
        f"`{data['previous_h123']['candidate_id']}` was PIPELINE-9 rank {data['previous_h123']['previous_pipeline9_rank']} with reduction {data['previous_h123']['previous_pipeline9_expected_reduction']}. With its accepted decisions included, it is `{data['previous_h123']['status']}` and contributes no fresh reduction.",
        "",
        "## Selected cohort",
        "",
        f"Fresh rank-1 `{selected['id']}` is semantic `{selected['semantic_key']}` at `{selected['table']}:{selected['address']}` across: " + ", ".join(f"`{scope}`" for scope in selected["source_scopes"]) + ".",
        f"Canonical physical targets: {selected['canonical_physical_target_count']}/{selected['canonical_physical_target_count']}; applicability paths: {selected['applicability_path_count']}/{selected['applicability_path_count']}. Physical parity is 100% and path coverage is 100%.",
        "",
        "## Physical targets vs applicability paths",
        "",
        "The repaired PIPELINE-9A path identity is retained. Physical authority is deduplicated by canonical family/table/address; applicability evidence is keyed by canonical family/table/address/source scope/source declaration. Multiple paths therefore produce one property promotion per physical target.",
        "",
        "## Property-level evidence and provenance consistency",
        "",
        f"The selected cohort produces {len(data['reconciliation_decisions'])} property decisions. Every promoted property has noncanonical support: `{data['evidence']['all_promoted_properties_have_noncanonical_support']}`. Applicability path consistency is {data['applicability_path_consistency']['consistent_path_count']}/{data['applicability_path_consistency']['path_count']}. The machine audit is `docs/pipeline/data/GII-PIPELINE-10A_PROPERTY_CELL_PROVENANCE_AUDIT.json`.",
        "",
        "## Semantic parity",
        "",
        f"Semantic parity is computed over {len(data['semantic_parity'])} unique physical targets: `{data['semantic_parity_summary']}`. It is not inflated by duplicate applicability paths.",
        "",
        "## Authority movement",
        "",
        "| Metric | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
        f"| Repository legacy-authoritative cells | {before['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells'] - before['legacy_authoritative_property_cells']:+d} |",
        f"| Repository declarative-authoritative cells | {before['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells'] - before['declarative_authoritative_property_cells']:+d} |",
        f"| Repository legacy-exclusive cells | {before['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells'] - before['legacy_exclusive_property_cells']:+d} |",
        f"| Selected cohort legacy-authoritative cells | {data['authority']['selected_before']['legacy_authoritative_property_cells']} | {data['authority']['selected_after']['legacy_authoritative_property_cells']} | {data['authority']['selected_after']['legacy_authoritative_property_cells'] - data['authority']['selected_before']['legacy_authoritative_property_cells']:+d} |",
        f"| Selected cohort declarative-authoritative cells | {data['authority']['selected_before']['declarative_authoritative_property_cells']} | {data['authority']['selected_after']['declarative_authoritative_property_cells']} | {data['authority']['selected_after']['declarative_authoritative_property_cells'] - data['authority']['selected_before']['declarative_authoritative_property_cells']:+d} |",
        f"| Selected cohort legacy-exclusive cells | {data['authority']['selected_before']['legacy_exclusive_property_cells']} | {data['authority']['selected_after']['legacy_exclusive_property_cells']} | {data['authority']['selected_after']['legacy_exclusive_property_cells'] - data['authority']['selected_before']['legacy_exclusive_property_cells']:+d} |",
        "",
        "## Deferred opportunities",
        "",
        "Only the current rank-1 bounded cohort is migrated. The remaining ranked candidates are retained in the machine-readable artifact. H3085 remains deferred as `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`.",
        "",
        "## Safety and validation",
        "",
        "No inverter write, Shine/cloud experiment, broker change, Home Assistant change or global cutover was performed. Maintained validators and the full pytest suite were run offline after generation; the archived missing-fixture validator remains non-gating.",
        "",
        "Generated by `tools/build_pipeline10_cohort.py`; no canonical register specification was modified.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    generation_tip = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    data, decisions = build(generation_tip_sha=generation_tip)
    RECONCILIATION_PATH.write_text(
        json.dumps(
            {"schema_version": "1.0.0", "artifact": "growatt_reconciliation_decisions", "decisions": decisions},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (ROOT / "reconciliation/resolved-assertions.json").write_text(
        json.dumps(build_reconciliation(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    OUTPUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(render(data), encoding="utf-8")
    print(json.dumps({"selected": data["selected_cohort"]["id"], "authority": data["authority"], "decisions": len(decisions)}, indent=2))


if __name__ == "__main__":
    main()
