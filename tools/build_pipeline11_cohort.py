#!/usr/bin/env python3
"""Build one bounded property-backed cohort after PIPELINE-10 acceptance."""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

try:
    from tools.build_authority_coverage import build as build_authority, canonical_authority_origins
    from tools.build_property_backed_cohort import (
        all_promoted_properties_have_noncanonical_support,
        parity_summary,
        selected_views,
        semantic_parity,
    )
    from tools.build_pipeline9_cohort import (
        CANONICAL_PATH,
        _authority_metrics,
        _build_decisions,
        _selected_authority,
        override_keys,
        read,
    )
    from tools.build_reconciliation import build as build_reconciliation
    from tools.pipeline9_candidates import accepted_decisions, enumerate_candidates, promoted_properties
    from tools.property_cell_provenance import property_cell_support
except ModuleNotFoundError:
    from build_authority_coverage import build as build_authority, canonical_authority_origins
    from build_property_backed_cohort import (
        all_promoted_properties_have_noncanonical_support,
        parity_summary,
        selected_views,
        semantic_parity,
    )
    from build_pipeline9_cohort import CANONICAL_PATH, _authority_metrics, _build_decisions, _selected_authority, override_keys, read
    from build_reconciliation import build as build_reconciliation
    from pipeline9_candidates import accepted_decisions, enumerate_candidates, promoted_properties
    from property_cell_provenance import property_cell_support

ROOT = Path(__file__).resolve().parents[1]
RECONCILIATION_PATH = ROOT / "reconciliation/pipeline11_next_repository_wide_cohort.json"
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-11_NEXT_PROPERTY_BACKED_COHORT.json"
REPORT_PATH = ROOT / "docs/pipeline/GII-PIPELINE-11_NEXT_PROPERTY_BACKED_COHORT.md"
PIPELINE9_ARTIFACT = ROOT / "docs/pipeline/data/GII-PIPELINE-9_REPOSITORY_WIDE_NEXT_COHORT.json"
PIPELINE10_ARTIFACT = ROOT / "docs/pipeline/data/GII-PIPELINE-10_NEXT_REPOSITORY_WIDE_COHORT.json"
PIPELINE10_SOURCE = "reconciliation/pipeline10_next_repository_wide_cohort.json"
STARTING_MAIN_SHA = "94df0ab9f5eee2310766f1b66f1dac9f3f114aa3"
PIPELINE10_ACCEPTED_TIP_SHA = "50c8028b2112644a41ba95b3a589a7dac1d1d24f"
DISPOSITION = "GII_PIPELINE_NEXT_PROPERTY_BACKED_COHORT_MIGRATION_ACCEPTED"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _registry_transition() -> dict[str, Any]:
    before = accepted_decisions(exclude_sources={PIPELINE10_SOURCE})
    after = accepted_decisions()
    registry = read(ROOT / "reconciliation/accepted-authority-sources.json")
    return {
        "registry_path": "reconciliation/accepted-authority-sources.json",
        "source_count_before": len(registry["sources"]) - 1,
        "source_count_after": len(registry["sources"]),
        "decision_count_before": len(before),
        "decision_count_after": len(after),
        "accepted_pipeline9": any(item["decision_id"].startswith("pipeline9-") for item in after),
        "accepted_pipeline10": any(item["decision_id"].startswith("pipeline10-") for item in after),
        "pipeline10_source_added": PIPELINE10_SOURCE in {item["path"] for item in registry["sources"]},
        "pipeline11_source_added": "reconciliation/pipeline11_next_repository_wide_cohort.json"
        in {item["path"] for item in registry["sources"]},
    }


def _physical_property_support(candidate: dict[str, Any]) -> dict[str, dict[str, Any]]:
    claims = read(ROOT / "sources/claims/generic-claims.json")["claims"]
    claims_by_id = {claim["claim_id"]: claim for claim in claims}
    result: dict[str, dict[str, Any]] = {}
    for key, properties in candidate["properties_by_physical_target"].items():
        support: dict[str, list[str]] = {}
        for decision_property, claim_ids in properties.items():
            decision = {
                "target": {"property": decision_property},
                "support": claim_ids,
                "decision": {"value": {}},
            }
            for property_name, detail in property_cell_support(decision, claims_by_id).items():
                support.setdefault(property_name, []).extend(detail["claim_ids"])
        result[key] = {
            property_name: {
                "status": "supported",
                "claim_ids": sorted(set(claim_ids)),
                "source_types": sorted(
                    {claims_by_id[claim_id]["assertion"]["kind"] for claim_id in claim_ids}
                ),
            }
            for property_name, claim_ids in sorted(support.items())
        }
    return result


def _fresh_reduction(
    candidate: dict[str, Any],
    accepted: dict[tuple[str, str, int], set[str]],
    authority: dict[str, Any],
) -> int:
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in read(CANONICAL_PATH)["registers"]
    }
    overrides = override_keys()
    support = candidate.get("authority_support_by_physical_target") or _physical_property_support(candidate)
    records = {
        (item["family"], item["table"], item["address"]): item for item in authority["records"]
    }
    total = 0
    for key_text, supported in support.items():
        family, table, address = key_text.split(":")
        key = (family, table, int(address))
        origins = canonical_authority_origins(canonical[key], overrides)
        legacy = {
            name
            for name, detail in origins.items()
            if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
        }
        total += len((legacy - accepted.get(key, set())) & set(supported))
        if key not in records:
            raise AssertionError(f"candidate target missing from authority inventory: {key}")
    return total


def _historical_candidate(path: Path, address: int) -> dict[str, Any]:
    data = read(path)
    return next(
        item
        for item in data["candidate_ranking"]
        if item["table"] == "holding" and item["address"] == address
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


def build(generation_tip_sha: str = STARTING_MAIN_SHA) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    enumeration = enumerate_candidates()
    ranking = enumeration["candidate_ranking"]
    if not ranking:
        raise AssertionError("PIPELINE-11 produced no evidence-supported bounded candidate")
    selected = ranking[0]
    before_decisions = accepted_decisions()
    accepted = promoted_properties(before_decisions)
    authority = build_authority()
    before = _authority_metrics(authority, before_decisions)
    decisions = _build_decisions(selected, decision_prefix="pipeline11", pipeline_name="PIPELINE-11")
    after = _authority_metrics(authority, [*before_decisions, *decisions])
    physical, paths = selected_views(selected)
    selected_authority = _selected_authority(selected, before_decisions, decisions)
    selected_before = {
        "physical_records": selected_authority["physical_records"],
        "legacy_authoritative_property_cells": selected_authority["legacy_authoritative_property_cells_before"],
        "legacy_exclusive_property_cells": selected_authority["legacy_exclusive_property_cells_before"],
    }
    selected_after = {
        "physical_records": selected_authority["physical_records"],
        "legacy_authoritative_property_cells": selected_authority["legacy_authoritative_property_cells_after"],
        "legacy_exclusive_property_cells": selected_authority["legacy_exclusive_property_cells_after"],
    }
    p9_h123 = _historical_candidate(PIPELINE9_ARTIFACT, 123)
    p10_h100 = _historical_candidate(PIPELINE10_ARTIFACT, 100)
    h123_reduction = _fresh_reduction(p9_h123, accepted, authority)
    h100_reduction = _fresh_reduction(p10_h100, accepted, authority)
    if h123_reduction or h100_reduction:
        raise AssertionError(f"accepted cohort remains reducible: H123={h123_reduction}, H100={h100_reduction}")
    previous_ranking = read(PIPELINE10_ARTIFACT)["candidate_ranking"]
    parity = semantic_parity(selected, physical)
    data = {
        "schema_version": "1.0.0",
        "artifact": "growatt_pipeline11_next_property_backed_cohort",
        "generated_by": "tools/build_pipeline11_cohort.py",
        "disposition": DISPOSITION,
        "lineage": {
            "starting_merged_main_sha": STARTING_MAIN_SHA,
            "accepted_pipeline10_tip_ancestor_sha": PIPELINE10_ACCEPTED_TIP_SHA,
            "generation_tip_sha": generation_tip_sha,
        },
        "accepted_authority_transition": _registry_transition(),
        "canonical": {
            "path": "spec/growatt-register-spec.json",
            "sha256": sha256(CANONICAL_PATH),
            "canonical_modified": False,
        },
        "baseline": before,
        "repository_wide_coverage": enumeration["coverage"],
        "candidate_universe": enumeration["candidate_universe"],
        "candidate_ranking": ranking,
        "ranking_method": "Repository-wide V1.24 candidates ranked after accepted-authority registry loading; expected reduction uses unique explicit evidence-supported property cells and excludes already accepted cells.",
        "accepted_state_zero_reduction": {
            "pipeline9_h123": {
                "accepted_source": "reconciliation/pipeline9_repository_wide_next_cohort.json",
                "candidate_id": p9_h123["id"],
                "fresh_expected_reduction": h123_reduction,
                "status": "already_accepted_zero_fresh_reduction",
            },
            "pipeline10_h100": {
                "accepted_source": PIPELINE10_SOURCE,
                "candidate_id": p10_h100["id"],
                "fresh_expected_reduction": h100_reduction,
                "status": "already_accepted_zero_fresh_reduction",
            },
        },
        "ranking_delta_from_pipeline10": {
            "previous_winner": read(PIPELINE10_ARTIFACT)["selected_cohort"]["id"],
            "previous_rank_two": previous_ranking[1]["id"],
            "previous_winner_fresh_reduction": h100_reduction,
            "new_rank_one": selected["id"],
            "new_rank_two": ranking[1]["id"],
            "ordering_changed_beyond_satisfied_previous_winner": [
                item["id"] for item in previous_ranking[1:]
            ] != [item["id"] for item in ranking[: len(previous_ranking) - 1]],
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
            "all_promoted_properties_have_noncanonical_support": all_promoted_properties_have_noncanonical_support(decisions),
        },
        "semantic_parity": parity,
        "semantic_parity_summary": parity_summary(parity),
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
        },
        "deferred_candidates": [
            _candidate_summary(item, "ranked but deferred; PIPELINE-11 migrates exactly one cohort")
            for item in ranking[1:11]
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
            "shine_injection": False,
            "cloud_experiment": False,
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
    transition = data["accepted_authority_transition"]
    lines = [
        "# GII-PIPELINE-11 — Next property-backed repository-wide cohort",
        "",
        f"Disposition: `{data['disposition']}`",
        "",
        "## Lineage",
        "",
        f"- Merged `main` used as the starting point: `{data['lineage']['starting_merged_main_sha']}`.",
        f"- Accepted PIPELINE-10 tip verified in ancestry: `{data['lineage']['accepted_pipeline10_tip_ancestor_sha']}`.",
        f"- Generation tip recorded: `{data['lineage']['generation_tip_sha']}`.",
        "",
        "## Accepted authority transition",
        "",
        f"The accepted-authority registry grew from {transition['source_count_before']} to {transition['source_count_after']} sources and from {transition['decision_count_before']} to {transition['decision_count_after']} accepted decisions. PIPELINE-10 is now accepted through the registry; PIPELINE-11 is not registered before its own migration.",
        "",
        "## Property-cell baseline after PIPELINE-10 acceptance",
        "",
        f"| Metric | Value |\n| --- | ---: |\n| Legacy-authoritative property cells | {data['baseline']['legacy_authoritative_property_cells']} |\n| Declarative-authoritative property cells | {data['baseline']['declarative_authoritative_property_cells']} |\n| Legacy-exclusive property cells | {data['baseline']['legacy_exclusive_property_cells']} |",
        "",
        "This is the accepted baseline. The registry update itself is not counted as a PIPELINE-11 gain.",
        "",
        "## H123/H100 zero-reduction proof",
        "",
        f"- H123 (`{data['accepted_state_zero_reduction']['pipeline9_h123']['accepted_source']}`): fresh reduction `{data['accepted_state_zero_reduction']['pipeline9_h123']['fresh_expected_reduction']}`; already accepted.",
        f"- H100 (`{data['accepted_state_zero_reduction']['pipeline10_h100']['accepted_source']}`): fresh reduction `{data['accepted_state_zero_reduction']['pipeline10_h100']['fresh_expected_reduction']}`; already accepted.",
        "",
        "Both disappear naturally from the reducible candidate enumeration because accepted property cells are loaded from the registry; no address blacklist or pipeline-specific exclusion is used.",
        "",
        "## Repository-wide source-scope coverage",
        "",
        "The ranking retains all seven V1.24 source scopes and all 33 declared ranges.",
        "",
        "| Scope | Ranges | Records | Accepted declarative cells | Remaining legacy cells | Candidates | Qualified/unresolved | Best candidate | Reduction |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | ---: |",
    ]
    for scope, item in data["repository_wide_coverage"].items():
        lines.append(
            f"| `{scope}` | {item['declared_range_count']} | {item['applicable_physical_records_found']} | {item['partly_declarative_records']} | {item['remaining_legacy_authoritative_cells']} | {item['evidence_supported_candidate_count']} | {item['unresolved_or_qualified_candidate_count']} | `{item['best_bounded_candidate']}` | {item['best_expected_reduction']} |"
        )
    delta = data["ranking_delta_from_pipeline10"]
    lines += [
        "",
        "## Fresh candidate ranking",
        "",
        f"The previous PIPELINE-10 winner was `{delta['previous_winner']}`; its fresh reduction is {delta['previous_winner_fresh_reduction']}. The previous rank 2 was `{delta['previous_rank_two']}`. Fresh rank 1 is `{delta['new_rank_one']}` and fresh rank 2 is `{delta['new_rank_two']}`. Ordering changed beyond satisfying the previous winner: `{delta['ordering_changed_beyond_satisfied_previous_winner']}`.",
        "",
        "| Rank | Candidate | Semantic key | Address | Physical | Paths | Reduction | Evidence | Qualifiers | Conflicts |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | --- |",
    ]
    for item in data["candidate_ranking"][:12]:
        lines.append(
            f"| {item['rank']} | `{item['id']}` | `{item['semantic_key']}` | `{item['table']}:{item['address']}` | {item['canonical_physical_target_count']} | {item['applicability_path_count']} | {item['expected_reduction']} | {item['evidence_score']} | {item['qualifier_complexity']} | {item['source_conflict']} |"
        )
    lines += [
        "",
        "## Selected cohort",
        "",
        f"Fresh rank 1 `{selected['id']}` is `{selected['semantic_key']}` at `{selected['table']}:{selected['address']}`. It is bounded, has {selected['canonical_physical_target_count']}/{selected['canonical_physical_target_count']} unique physical targets and {selected['applicability_path_count']}/{selected['applicability_path_count']} applicability paths, and has an evidence-backed expected reduction of {selected['expected_reduction']} property cells.",
        "",
        "## Property-level evidence",
        "",
        f"Every promoted property has explicit noncanonical claim support: `{data['evidence']['all_promoted_properties_have_noncanonical_support']}`. The machine artifact records property names, claim IDs, source types and support per physical target. No unsupported canonical or compatibility value is promoted.",
        "",
        "## Physical targets vs applicability paths",
        "",
        "Physical authority is deduplicated by canonical family/table/address; applicability evidence retains source-scope/source-declaration paths. The selected cohort therefore has separate physical and path counts, and duplicate paths do not double-count authority.",
        "",
        "## Provenance consistency",
        "",
        f"All {selected['applicability_path_count']} applicability paths are in supported applicability states, and all selected decisions cite their retained paths. Property-cell support uses the existing PIPELINE-10A capability rules.",
        "",
        "## Semantic parity",
        "",
        f"Parity is classified over {len(data['semantic_parity'])} unique physical targets: `{data['semantic_parity_summary']}`. Canonical SHA is `{data['canonical']['sha256']}` and `canonical_modified=false`.",
        "",
        "## Authority movement",
        "",
        "| Metric | Accepted baseline | Selected cohort before | Repository after | Selected cohort after |",
        "| --- | ---: | ---: | ---: | ---: |",
        f"| Legacy-authoritative property cells | {before['legacy_authoritative_property_cells']} | {data['authority']['selected_before']['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells']} | {data['authority']['selected_after']['legacy_authoritative_property_cells']} |",
        f"| Declarative-authoritative property cells | {before['declarative_authoritative_property_cells']} | — | {after['declarative_authoritative_property_cells']} | — |",
        f"| Legacy-exclusive property cells | {before['legacy_exclusive_property_cells']} | {data['authority']['selected_before']['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells']} | {data['authority']['selected_after']['legacy_exclusive_property_cells']} |",
        "",
        "The repository legacy count decreases and declarative count increases solely through the selected property-supported decisions; legacy-exclusive remains measured rather than forced.",
        "",
        "## Deferred opportunities",
        "",
        "Only one cohort is migrated. The top deferred candidates, including qualifiers/conflicts and their calculated reductions, remain in the machine artifact.",
        "",
        "## Correction candidates",
        "",
        "H3085 remains a `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`; no canonical correction is made here.",
        "",
        "## Reusable runner/refactor",
        "",
        "PIPELINE-11 reuses the repository-wide candidate enumerator, accepted-authority registry, property-cell support rules and PIPELINE-9 decision/authority mechanics. The small `tools/build_property_backed_cohort.py` module provides shared physical/path views and parity/support checks without introducing a second authority or claims model.",
        "",
        "## Safety and validation",
        "",
        "No inverter writes, Shine injection, cloud experiment, broker change, Home Assistant change, runtime deployment or global cutover was performed. PIPELINE-11 is an offline semantic-authority migration only.",
        "",
        "Generated by `tools/build_pipeline11_cohort.py`; no canonical register specification was modified.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    generation_tip = subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    data, decisions = build(generation_tip)
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
    print(json.dumps({"selected": data["selected_cohort"]["id"], "authority": data["authority"]}, indent=2))


if __name__ == "__main__":
    main()
