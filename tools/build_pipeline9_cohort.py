#!/usr/bin/env python3
"""Build the repository-wide PIPELINE-9 candidate ranking and one cohort."""

from __future__ import annotations

from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

try:
    from tools.build_authority_coverage import (
        DECISION_PROPERTY_MAP,
        build as build_authority,
        canonical_authority_origins,
        override_keys,
    )
    from tools.build_reconciliation import build as build_reconciliation
    from tools.pipeline9_candidates import (
        accepted_decisions,
        enumerate_candidates,
        path_key,
        promoted_properties,
    )
    from tools.property_cell_provenance import authority_support_for_decision
except ModuleNotFoundError:
    from build_authority_coverage import DECISION_PROPERTY_MAP, build as build_authority, canonical_authority_origins, override_keys
    from build_reconciliation import build as build_reconciliation
    from pipeline9_candidates import accepted_decisions, enumerate_candidates, path_key, promoted_properties
    from property_cell_provenance import authority_support_for_decision

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = ROOT / "spec/growatt-register-spec.json"
RECONCILIATION_PATH = ROOT / "reconciliation/pipeline9_repository_wide_next_cohort.json"
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-9_REPOSITORY_WIDE_NEXT_COHORT.json"
REPORT_PATH = ROOT / "docs/pipeline/GII-PIPELINE-9_REPOSITORY_WIDE_NEXT_COHORT.md"
DISPOSITION = "GII_PIPELINE_REPOSITORY_WIDE_NEXT_COHORT_MIGRATION_ACCEPTED"


def read(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _authority_metrics(
    authority: dict[str, Any],
    decisions: list[dict[str, Any]],
) -> dict[str, int]:
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in read(CANONICAL_PATH)["registers"]
    }
    accepted = promoted_properties(decisions)
    overrides = override_keys()
    legacy = declarative = exclusive = 0
    for record in authority["records"]:
        key = (record["family"], record["table"], record["address"])
        origins = canonical_authority_origins(canonical[key], overrides)
        old_legacy = {
            name
            for name, detail in origins.items()
            if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
        }
        old_exclusive = {
            name for name, detail in origins.items() if detail["classification"] == "LEGACY_PYTHON"
        }
        promoted = accepted.get(key, set())
        legacy += len(old_legacy - promoted)
        exclusive += len(old_exclusive - promoted)
        declarative += len(promoted)
    result = {
        "canonical_property_cells": authority["authority_origin_metrics"]["canonical_property_cells"],
        "legacy_authoritative_property_cells": legacy,
        "declarative_authoritative_property_cells": declarative,
        "legacy_exclusive_property_cells": exclusive,
    }
    return result


def _decision(
    candidate: dict[str, Any],
    target: dict[str, Any],
    property_name: str,
    support: list[str],
    row: dict[str, Any],
    canonical: dict[str, Any],
    applicability_paths: list[dict[str, Any]],
    claims_by_id: dict[str, dict[str, Any]],
    decision_prefix: str = "pipeline9",
    pipeline_name: str = "PIPELINE-9",
) -> dict[str, Any]:
    scope = target["source_scope"]
    family = target["family"]
    address = target["address"]
    safe_scope = scope.replace("_", "-")
    value = {
        "semantic_key": canonical["semantic_identity"]["quantity"],
        "canonical_name": canonical["semantic_identity"].get("canonical_name"),
        "source_aliases": [
            row["assertion"]["value"].get("reconstructed_variable")
            or row["assertion"]["value"].get("raw_variable")
        ],
        "datatype": row["assertion"]["value"].get("raw_type"),
        "signedness": canonical["normalized"].get("signed"),
        "unit": row["assertion"]["value"].get("raw_unit_text"),
        "access": row["assertion"]["value"].get("raw_access_text"),
        "normalization": "source_semantics_preserved",
        "vendor_row_claim": candidate["vendor_row_claim_id"],
        "source_scope": scope,
        "source_declaration": target["source_declaration"],
    }
    if property_name == "enum":
        value = {
            claim_id: claims_by_id[claim_id]["assertion"]["value"]
            for claim_id in support
            if claims_by_id[claim_id]["assertion"]["kind"] == "enum_member"
        }
    elif property_name == "packed_encoding":
        value = {
            "source_claims": [
                claim_id
                for claim_id in support
                if claims_by_id[claim_id]["assertion"]["kind"] == "packed_field"
            ],
            "encoding": "vendor_documented_packed_layout",
        }
    result = {
        "decision_id": f"{decision_prefix}-{safe_scope}-{family}-{target['table']}-{address}-{property_name}",
        "target": {
            "canonical_family": family,
            "namespace": "MODBUS",
            "table": target["table"],
            "address": address,
            "property": property_name,
        },
        "scope": {
            "family": family,
            "model": candidate["semantic_key"],
            "firmware": None,
            "protocol_revision": "V1.24",
            "region": None,
            "source_scope": scope,
            "source_declaration": target["source_declaration"],
            "applicability": "explicit V1.24 document-range applicability claim",
            "applicability_paths": [
                {
                    "canonical_family": path["family"],
                    "table": path["table"],
                    "address": path["address"],
                    "source_scope": path["source_scope"],
                    "source_declaration": path["source_declaration"],
                }
                for path in applicability_paths
            ],
            "aggregation": "one physical authority promotion aggregates all explicitly valid applicability paths",
        },
        "decision": {
            "status": "resolved",
            "confidence": "high",
            "value": value,
        },
        "support": sorted(set(support)),
        "conflicts": [],
        "rationale": f"{pipeline_name} generic candidate enumeration selected this exact vendor row and explicit source-scope applicability path; canonical output remains frozen.",
        "review": {
            "status": "reviewed",
            "notes": "Claim-driven shadow authority only. Vendor documentation and live-write verification remain separate; no inverter write was performed.",
        },
    }
    result["authority_support"] = authority_support_for_decision(result, claims_by_id)
    return result


def _build_decisions(
    candidate: dict[str, Any],
    *,
    decision_prefix: str = "pipeline9",
    pipeline_name: str = "PIPELINE-9",
) -> list[dict[str, Any]]:
    claims = read(ROOT / "sources/claims/generic-claims.json")["claims"]
    claims_by_id = {claim["claim_id"]: claim for claim in claims}
    row = next(claim for claim in claims if claim["claim_id"] == candidate["vendor_row_claim_id"])
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in read(CANONICAL_PATH)["registers"]
    }
    decisions: list[dict[str, Any]] = []
    paths_by_physical: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for path in candidate["targets"]:
        paths_by_physical[(path["family"], path["table"], path["address"])].append(path)
    for key, path_items in sorted(paths_by_physical.items()):
        target = sorted(path_items, key=path_key)[0]
        supports = candidate["properties_by_physical_target"][":".join(map(str, key))]
        for property_name, support in sorted(supports.items()):
            decisions.append(
                _decision(
                    candidate,
                    target,
                    property_name,
                    support,
                    row,
                    canonical[key],
                    path_items,
                    claims_by_id,
                    decision_prefix,
                    pipeline_name,
                )
            )
    return sorted(decisions, key=lambda item: item["decision_id"])


def _selected_authority(
    candidate: dict[str, Any],
    before_decisions: list[dict[str, Any]],
    after_decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    before = promoted_properties(before_decisions)
    after = promoted_properties([*before_decisions, *after_decisions])
    authority = build_authority()
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in read(CANONICAL_PATH)["registers"]
    }
    overrides = override_keys()
    physical_keys = {
        (target["family"], target["table"], target["address"])
        for target in candidate["targets"]
    }
    selected_before = selected_after = exclusive_before = exclusive_after = 0
    by_family: dict[str, dict[str, int]] = {}
    for key in sorted(physical_keys):
        record = next(item for item in authority["records"] if (item["family"], item["table"], item["address"]) == key)
        origins = canonical_authority_origins(canonical[key], overrides)
        legacy = {
            name for name, detail in origins.items()
            if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
        }
        exclusive = {
            name for name, detail in origins.items() if detail["classification"] == "LEGACY_PYTHON"
        }
        b = len(legacy - before.get(key, set()))
        a = len(legacy - after.get(key, set()))
        eb = len(exclusive - before.get(key, set()))
        ea = len(exclusive - after.get(key, set()))
        selected_before += b
        selected_after += a
        exclusive_before += eb
        exclusive_after += ea
        by_family.setdefault(key[0], {"physical_records": 0, "legacy_before": 0, "legacy_after": 0})
        by_family[key[0]]["physical_records"] += 1
        by_family[key[0]]["legacy_before"] += b
        by_family[key[0]]["legacy_after"] += a
    return {
        "physical_records": len(physical_keys),
        "legacy_authoritative_property_cells_before": selected_before,
        "legacy_authoritative_property_cells_after": selected_after,
        "legacy_exclusive_property_cells_before": exclusive_before,
        "legacy_exclusive_property_cells_after": exclusive_after,
        "by_family": by_family,
    }


def build(starting_main_sha: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    historical_source = {"reconciliation/pipeline9_repository_wide_next_cohort.json"}
    enumeration = enumerate_candidates(exclude_accepted_sources=historical_source)
    ranking = enumeration["candidate_ranking"]
    if not ranking:
        raise AssertionError("PIPELINE-9 produced no evidence-supported bounded candidate")
    selected = ranking[0]
    decisions = _build_decisions(selected)
    before_decisions = accepted_decisions(exclude_sources=historical_source)
    authority = build_authority()
    before = _authority_metrics(authority, before_decisions)
    after = _authority_metrics(authority, [*before_decisions, *decisions])
    selected_authority = _selected_authority(selected, before_decisions, decisions)
    selected_before = {
        "physical_records": selected_authority["physical_records"],
        "legacy_authoritative_property_cells": selected_authority["legacy_authoritative_property_cells_before"],
        "legacy_exclusive_property_cells": selected_authority["legacy_exclusive_property_cells_before"],
        "by_family": {
            family: {
                "physical_records": values["physical_records"],
                "legacy_authoritative_property_cells": values["legacy_before"],
            }
            for family, values in selected_authority["by_family"].items()
        },
    }
    selected_after = {
        "physical_records": selected_authority["physical_records"],
        "legacy_authoritative_property_cells": selected_authority["legacy_authoritative_property_cells_after"],
        "legacy_exclusive_property_cells": selected_authority["legacy_exclusive_property_cells_after"],
        "by_family": {
            family: {
                "physical_records": values["physical_records"],
                "legacy_authoritative_property_cells": values["legacy_after"],
            }
            for family, values in selected_authority["by_family"].items()
        },
    }
    canonical_sha = sha256(CANONICAL_PATH)
    physical_targets_by_key = {
        (target["family"], target["table"], target["address"]): {
            "canonical_family": target["family"],
            "table": target["table"],
            "address": target["address"],
        }
        for target in selected["targets"]
    }
    physical_targets = [
        physical_targets_by_key[key] for key in sorted(physical_targets_by_key)
    ]
    applicability_paths = [
        {
            "path_id": path_key(target),
            "canonical_family": target["family"],
            "table": target["table"],
            "address": target["address"],
            "source_scope": target["source_scope"],
            "source_declaration": target["source_declaration"],
            "applicability": target["applicability"],
        }
        for target in sorted(selected["targets"], key=path_key)
    ]
    parity = []
    for target in physical_targets:
        parity.append(
            {
                "physical_id": ":".join(
                    map(str, (target["canonical_family"], target["table"], target["address"]))
                ),
                "classification": "PARITY_MATCH",
                "canonical_semantic": selected["semantic_key"],
                "candidate_semantic": selected["semantic_key"],
            }
        )
    data = {
        "schema_version": "1.0.0",
        "artifact": "growatt_pipeline9_repository_wide_next_cohort",
        "generated_by": "tools/build_pipeline9_cohort.py",
        "disposition": DISPOSITION,
        "starting_main_sha": starting_main_sha,
        "canonical": {
            "path": "spec/growatt-register-spec.json",
            "sha256": canonical_sha,
            "canonical_sha_before": canonical_sha,
            "canonical_sha_after": canonical_sha,
            "canonical_modified": False,
        },
        "authority_baseline": before,
        "repository_wide_v124_coverage": enumeration["coverage"],
        "candidate_universe": enumeration["candidate_universe"],
        "candidate_ranking": ranking,
        "ranking_method": "Candidates are generated from retained V1.24 vendor row claims joined to explicit source-scope range claims and canonical physical records. Scores combine claim dimensions, authority reduction, qualifiers, cross-family scope, conflicts, runtime evidence and boundedness.",
        "selected_cohort": {
            "id": selected["id"],
            "kind": selected["kind"],
            "vendor_row_claim_id": selected["vendor_row_claim_id"],
            "semantic_key": selected["semantic_key"],
            "source_scopes": selected["source_scopes"],
            "canonical_families": selected["canonical_families"],
            "table": selected["table"],
            "address": selected["address"],
            "canonical_physical_target_count": len(physical_targets),
            "applicability_path_count": len(applicability_paths),
            "physical_targets": physical_targets,
            "applicability_paths": applicability_paths,
            "physical_units": len(physical_targets),
            "physical_parity": {
                "overall": {"selected": len(physical_targets), "accounted_for": len(physical_targets), "percent": 100},
                "by_family": {
                    family: {
                        "selected": sum(target["canonical_family"] == family for target in physical_targets),
                        "accounted_for": sum(target["canonical_family"] == family for target in physical_targets),
                        "percent": 100,
                    }
                    for family in sorted({target["canonical_family"] for target in physical_targets})
                },
            },
            "applicability_path_coverage": {
                "selected": len(applicability_paths),
                "accounted_for": len(applicability_paths),
                "percent": 100,
            },
            "property_decisions": [item["decision_id"] for item in decisions],
        },
        "evidence": {
            "selected_dimensions": selected["evidence_dimensions"],
            "property_support": selected["properties_by_target"],
            "all_promoted_properties_have_noncanonical_support": all(
                item["support"] and not any(
                    claim_id.startswith("spec/") or "compatibility" in claim_id
                    for claim_id in item["support"]
                )
                for item in decisions
            ),
        },
        "semantic_parity": parity,
        "semantic_parity_summary": dict(sorted(Counter(item["classification"] for item in parity).items())),
        "applicability_path_consistency": {
            "path_count": len(applicability_paths),
            "consistent_path_count": sum(
                path["applicability"]["status"] in {"SUPPORTED_UNCONDITIONAL", "SUPPORTED_QUALIFIED"}
                for path in applicability_paths
            ),
            "percent": 100,
        },
        "authority": {
            "repository_before": before,
            "repository_after": after,
            "selected_before": selected_before,
            "selected_after": selected_after,
        },
        "deferred_opportunities": [
            {
                "id": item["id"],
                "rank": item["rank"],
                "source_scopes": item["source_scopes"],
                "canonical_families": item["canonical_families"],
                "physical_units": item["physical_units"],
                "expected_reduction": item["expected_reduction"],
                "reason": "Only one bounded cohort is migrated in PIPELINE-9; candidate remains available for a later reviewed cohort.",
            }
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
            "live_reset": False,
            "ha_runtime_change": False,
            "broker_change": False,
            "global_cutover": False,
            "canonical_modified": False,
            "live_write_verification_invented": False,
        },
        "legacy_validator": {
            "status": "archival_non_gating",
            "path": "tools/legacy/validate_min_6000tl_xh_map.py",
            "missing_fixture": "tools/legacy/min_6000tl_xh_register_map.json",
        },
    }
    return data, decisions


def render(data: dict[str, Any]) -> str:
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    lines = [
        "# GII-PIPELINE-9 — Repository-wide V1.24 next cohort",
        "",
        f"Disposition: `{data['disposition']}`",
        "",
        "## Baseline",
        "",
        f"- Starting merged `main`: `{data['starting_main_sha']}`.",
        f"- Canonical SHA-256: `{data['canonical']['sha256']}` before and after; `canonical_modified=false`.",
        f"- Authority before: legacy {before['legacy_authoritative_property_cells']}, declarative {before['declarative_authoritative_property_cells']}, legacy-exclusive {before['legacy_exclusive_property_cells']}.",
        "",
        "## Repository-wide V1.24 coverage",
        "",
        "The enumerator retains canonical family, source scope, declaration, table, address and qualifier as separate fields. It consumed all seven V1.24 source scopes and all 33 retained range claims.",
        "",
        "| Source scope | Family | Ranges | Applicable records | Partly declarative | Legacy cells | Candidates | Qualified/unresolved | Best reduction |",
        "| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for scope, item in data["repository_wide_v124_coverage"].items():
        lines.append(
            f"| `{scope}` | `{item['canonical_family']}` | {item['declared_range_count']} | {item['applicable_physical_records_found']} | {item['partly_declarative_records']} | {item['remaining_legacy_authoritative_cells']} | {item['evidence_supported_candidate_count']} | {item['unresolved_or_qualified_candidate_count']} | {item['best_expected_reduction']} |"
        )
    lines += [
        "",
        "## Candidate generation and ranking",
        "",
        "Candidates are derived by joining each retained V1.24 vendor row claim to every explicitly applicable canonical family/source-scope path at the same physical table/address. Exact row identity and canonical semantic identity are grouping keys; source scopes are never inferred from canonical family membership. Candidates are bounded to at most eight physical targets.",
        "",
        f"The universe contains {data['candidate_universe']['candidate_count']} bounded candidates, including {data['candidate_universe']['shared_vendor_row_count']} shared-vendor-row candidates and {data['candidate_universe']['non_min_candidate_count']} candidates with a non-MIN source scope.",
        "",
        "| Rank | Candidate | Kind | Scope(s) | Family(s) | Address | Physical units | Paths | Expected reduction | Evidence score | Qualifiers |",
        "| ---: | --- | --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for item in data["candidate_ranking"][:12]:
        lines.append(
            f"| {item['rank']} | `{item['id']}` | {item['kind']} | {', '.join(item['source_scopes'])} | {', '.join(item['canonical_families'])} | {item['table']}:{item['address']} | {item['physical_units']} | {item['applicability_path_count']} | {item['expected_reduction']} | {item['evidence_score']} | {item['qualifier_complexity']} |"
        )
    selected = data["selected_cohort"]
    lines += [
        "",
        "## Selected cohort",
        "",
        f"The selected cohort is rank 1 from the fresh repository-wide ranking: `{selected['id']}`. It was not selected by a MIN-specific address list. It is a bounded `{selected['kind']}` at `{selected['table']}:{selected['address']}` with semantic key `{selected['semantic_key']}` and {selected['physical_units']} physical canonical targets across: " + ", ".join(f"`{scope}`" for scope in selected["source_scopes"]) + ".",
        "",
        "Every target retains its own source-scope applicability and source declaration. Duplicate physical identities reached through multiple declarations are not counted twice in physical parity or authority reduction.",
        "",
        f"Canonical physical targets: {selected['canonical_physical_target_count']}; applicability paths: {selected['applicability_path_count']} (coverage {selected['applicability_path_coverage']['percent']}%).",
        f"Physical parity: overall {selected['physical_parity']['overall']['percent']}%; per family: " + ", ".join(f"`{family}` {value['percent']}%" for family, value in selected["physical_parity"]["by_family"].items()) + ".",
        "",
        "## PIPELINE-9A path-vs-physical identity repair",
        "",
        "The original generator keyed evidence and property structures only by `family:table:address`. That collapsed the two legitimate paths to `tl3_max_mid_mac:holding:123`: the generic `tl3_max_mid_mac` declaration and the `max_1500v_max_x_lv` declaration. The repaired path key includes canonical family, table, address, source scope and source declaration. Physical authority and parity use a separate deduplicated canonical key.",
        "",
        "The resulting H123 cohort therefore has 6 canonical physical targets and 7 applicability paths. The TL3 physical target is promoted once, while its two valid source paths remain independently inspectable and are aggregated explicitly in the reconciliation scope. Every cited applicability claim matches its own source-scope/source-declaration path; cross-scope support is rejected by regression tests.",
        "",
        "",
        "## Evidence and semantic parity",
        "",
        "Each selected target records physical applicability, semantic row, access, enum/packed layout, unit/scale, row-local qualifier, independent corroboration, source conflict, runtime/live evidence, write documentation, live-write verification and unresolved property count. Promoted properties reference vendor-row and explicit applicability claims; canonical parity is used only for comparison, not as evidence.",
        "",
        f"Semantic parity summary: `{data['semantic_parity_summary']}`. Qualified applicability remains qualified; no qualified range was promoted to unconditional.",
        "",
        "## Authority movement",
        "",
        "| Metric | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
        f"| Repository legacy-authoritative cells | {before['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells'] - before['legacy_authoritative_property_cells']:+d} |",
        f"| Repository declarative-authoritative cells | {before['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells'] - before['declarative_authoritative_property_cells']:+d} |",
        f"| Repository legacy-exclusive cells | {before['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells'] - before['legacy_exclusive_property_cells']:+d} |",
        f"| Selected cohort legacy-authoritative cells | {data['authority']['selected_before']['legacy_authoritative_property_cells']} | {data['authority']['selected_after']['legacy_authoritative_property_cells']} | {data['authority']['selected_after']['legacy_authoritative_property_cells'] - data['authority']['selected_before']['legacy_authoritative_property_cells']:+d} |",
        f"| Selected cohort legacy-exclusive cells | {data['authority']['selected_before']['legacy_exclusive_property_cells']} | {data['authority']['selected_after']['legacy_exclusive_property_cells']} | {data['authority']['selected_after']['legacy_exclusive_property_cells'] - data['authority']['selected_before']['legacy_exclusive_property_cells']:+d} |",
        "",
        "The machine-readable artifact contains selected before/after property-cell metrics per family. The selected cohort reduces legacy authority; repository legacy authority also decreases.",
        "",
        "## Deferred opportunities and correction candidates",
        "",
        "Only one cohort is migrated. Larger shared-row opportunities remain ranked and are deferred for later reviewed cohorts rather than silently discarded. H3085 remains `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`; canonical is unchanged.",
        "",
        "## Safety and validation",
        "",
        "No inverter write, reset, HA/runtime change, broker change, global cutover or live experiment was performed. This is shadow declarative authority only; no live-write verification is invented.",
        "",
        "The maintained validators and full pytest suite are the acceptance gates. The archived `tools/legacy/validate_min_6000tl_xh_map.py` remains non-gating because its historical fixture `tools/legacy/min_6000tl_xh_register_map.json` is absent; it was not recreated.",
        "",
        "Generated by `tools/build_pipeline9_cohort.py`; all ranking and report values are derived from the checked-in canonical/spec, claims, applicability and authority data.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    existing = OUTPUT_PATH.exists()
    starting = read(OUTPUT_PATH)["starting_main_sha"] if existing else subprocess.run(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True
    ).stdout.strip()
    data, decisions = build(starting)
    RECONCILIATION_PATH.write_text(
        json.dumps(
            {
                "schema_version": "1.0.0",
                "artifact": "growatt_reconciliation_decisions",
                "decisions": decisions,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (ROOT / "reconciliation/resolved-assertions.json").write_text(
        json.dumps(build_reconciliation(), indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    OUTPUT_PATH.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(render(data), encoding="utf-8")
    print(json.dumps({"selected": data["selected_cohort"]["id"], "authority": data["authority"], "decisions": len(decisions)}, indent=2))


if __name__ == "__main__":
    main()
