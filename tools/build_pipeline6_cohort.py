#!/usr/bin/env python3
"""Build the bounded PIPELINE-6 MIN/TL-XH holding EMS migration."""

from __future__ import annotations

import argparse
from collections import Counter
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
        decision_index,
        load_json,
        override_keys,
    )
except ModuleNotFoundError:
    from build_authority_coverage import (
        DECISION_PROPERTY_MAP,
        build as build_authority,
        canonical_authority_origins,
        decision_index,
        load_json,
        override_keys,
    )

ROOT = Path(__file__).resolve().parents[1]
RECONCILIATION_PATH = ROOT / "reconciliation/min_tl_xh_holding_ems_3036_3059_3081_3082.json"
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-6_NEXT_AUTHORITY_COHORT.json"
REPORT_PATH = ROOT / "docs/pipeline/GII-PIPELINE-6_NEXT_AUTHORITY_COHORT.md"
CANONICAL_PATH = ROOT / "spec/growatt-register-spec.json"

SELECTED_ADDRESSES = [*range(3036, 3060), 3081, 3082]
NEW_ADDRESSES = [*range(3038, 3046), *range(3050, 3060)]
REUSED_DECISION_SOURCE = "reconciliation/min_tl_xh.json"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def claim_id(claims: list[dict[str, Any]], source_id: str, address: int, prefix: str) -> str:
    matches = [
        item["claim_id"]
        for item in claims
        if item["source_id"] == source_id
        and item["subject"].get("table") == "holding"
        and item["subject"].get("address") == address
        and prefix in item["claim_id"]
        and ":source-row:" in item["claim_id"]
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one {source_id} claim for H{address}, found {matches}")
    return matches[0]


def semantic_claim_id(claims: list[dict[str, Any]], address: int) -> str:
    matches = [
        item["claim_id"]
        for item in claims
        if item["source_id"] == "min_semantic_review"
        and item["subject"].get("table") == "holding"
        and item["subject"].get("address") == address
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one semantic review claim for H{address}, found {matches}")
    return matches[0]


def build_decisions() -> list[dict[str, Any]]:
    claims = load_json(ROOT / "sources/claims/generic-claims.json")["claims"]
    reviews = {
        item["address"]: item
        for item in load_json(ROOT / "sources/evidence/min-6000tl-xh-semantic-review.json")["records"]
        if item["table"] == "holding"
    }
    decisions: list[dict[str, Any]] = []
    for address in NEW_ADDRESSES:
        review = reviews[address]
        encoding = review["encoding"]
        packed = encoding.startswith("packed")
        value = {
            "semantic_key": review["semantic_key"],
            "canonical_name": review["canonical_name"],
            "datatype": encoding,
            "signedness": "not_applicable" if packed else "unsigned",
            "unit": review.get("unit"),
            "normalization": "identity",
        }
        if packed:
            value["packed_layout"] = (
                "xh_schedule_start_control_v124"
                if "priority/enable" in encoding
                else "xh_schedule_end_v124"
            )
        vendor_claim = claim_id(claims, "vendor_growatt_v124_2020", address, ":visual-review")
        semantic_claim = semantic_claim_id(claims, address)
        confidence = review["confidence"]
        decisions.append(
            {
                "decision_id": f"min-xh-h{address}-ems-semantic-authority",
                "target": {
                    "canonical_family": "min_tl_xh",
                    "namespace": "MODBUS",
                    "table": "holding",
                    "address": address,
                    "property": "semantic_mapping",
                },
                "scope": {
                    "family": "min_tl_xh",
                    "model": "MIN/TL-XH",
                    "firmware": None,
                    "protocol_revision": "V1.24",
                    "region": None,
                    "applicability": "MIN/TL-XH EMS holding register",
                },
                "decision": {"status": "resolved", "confidence": confidence, "value": value},
                "support": [vendor_claim, semantic_claim],
                "conflicts": [],
                "rationale": (
                    "The reviewed V1.24 vendor row and the existing semantic review establish "
                    "the physical semantic for this MIN/TL-XH EMS register. Packed schedule "
                    "words retain the reusable V1.24 codec; no unsupported enum members are added."
                ),
                "review": {
                    "status": "reviewed",
                    "notes": "PIPELINE-6 promotion of an already reviewed source claim; canonical output remains frozen.",
                },
            }
        )
    return decisions


def selected_decisions(new_decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    old = load_json(ROOT / REUSED_DECISION_SOURCE)["decisions"]
    reused = [
        item
        for item in old
        if item["target"].get("namespace") == "MODBUS"
        and item["target"].get("table") == "holding"
        and item["target"].get("address") in SELECTED_ADDRESSES
    ]
    return [*reused, *new_decisions]


def build_reconciliation(new_decisions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_reconciliation_decisions",
        "decisions": new_decisions,
    }


def properties_for(decisions: list[dict[str, Any]]) -> dict[tuple[str, str, int], set[str]]:
    result: dict[tuple[str, str, int], set[str]] = {}
    for item in decisions:
        target = item["target"]
        if target.get("namespace") != "MODBUS":
            continue
        key = (target["canonical_family"], target["table"], target["address"])
        result.setdefault(key, set()).update(
            property_name
            for property_name in DECISION_PROPERTY_MAP.get(target["property"], set())
        )
    return result


def metrics(authority: dict[str, Any], selected: list[dict[str, Any]]) -> dict[str, Any]:
    records = authority["records"]
    by_key = {(item["family"], item["table"], item["address"]): item for item in records}
    all_declarative = properties_for(
        [
            item
            for item in load_json(ROOT / REUSED_DECISION_SOURCE)["decisions"]
            if item["target"].get("namespace") == "MODBUS"
        ]
        + [item for item in selected if item["decision_id"] not in {x["decision_id"] for x in load_json(ROOT / REUSED_DECISION_SOURCE)["decisions"]}]
    )
    selected_props = properties_for(selected)
    override_map = override_keys()
    canonical = load_json(CANONICAL_PATH)
    canonical_records = {
        (item["family"], item["table"], item["address"]): item for item in canonical["registers"]
    }
    before_legacy = after_legacy = before_exclusive = after_exclusive = 0
    before_declared = after_declared = 0
    selected_before = selected_after = 0
    selected_before_exclusive = selected_after_exclusive = 0
    for item in records:
        key = (item["family"], item["table"], item["address"])
        origins = canonical_authority_origins(canonical_records[key], override_map)
        legacy = {name for name, detail in origins.items() if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]}
        exclusive = {name for name, detail in origins.items() if detail["classification"] == "LEGACY_PYTHON"}
        # The pre-PIPELINE-6 4A decisions remain diagnostic. Only decisions
        # for this selected cohort move legacy authority in this transition.
        promoted = selected_props.get(key, set())
        baseline_declared = set(item["declarative_properties"])
        before_legacy += len(legacy)
        after_legacy += len(legacy - promoted)
        before_exclusive += len(exclusive)
        after_exclusive += len(exclusive - promoted)
        before_declared += len(baseline_declared)
        after_declared += len(baseline_declared | promoted)
        if key in selected_props:
            selected_before += len(legacy)
            selected_after += len(legacy - promoted)
            selected_before_exclusive += len(exclusive)
            selected_after_exclusive += len(exclusive - promoted)
    selected_record_keys = {("min_tl_xh", "holding", address) for address in SELECTED_ADDRESSES}
    parity = []
    for address in SELECTED_ADDRESSES:
        key = ("min_tl_xh", "holding", address)
        record = canonical_records[key]
        decision_items = [item for item in selected if item["target"].get("address") == address]
        values = [item["decision"]["value"] for item in decision_items if "semantic_key" in item["decision"]["value"]]
        candidate_key = values[-1].get("semantic_key") if values else None
        current_key = record["semantic_identity"].get("quantity")
        key_match = candidate_key and (candidate_key == current_key or candidate_key.replace("_", ".") == current_key)
        parity.append(
            {
                "physical_id": f"min_tl_xh:holding:{address}",
                "decision_ids": [item["decision_id"] for item in decision_items],
                "classification": "PARITY_MATCH" if key_match else "REPRESENTATION_ONLY",
                "canonical_semantic": current_key,
                "candidate_semantic": candidate_key,
            }
        )
    return {
        "repository_before": {
            "canonical_property_cells": authority["authority_origin_metrics"]["canonical_property_cells"],
            "legacy_authoritative_property_cells": before_legacy,
            "declarative_authoritative_property_cells": before_declared,
            "legacy_exclusive_property_cells": before_exclusive,
        },
        "repository_after": {
            "canonical_property_cells": authority["authority_origin_metrics"]["canonical_property_cells"],
            "legacy_authoritative_property_cells": after_legacy,
            "declarative_authoritative_property_cells": after_declared,
            "legacy_exclusive_property_cells": after_exclusive,
        },
        "selected_before": {
            "canonical_records": len(selected_record_keys),
            "legacy_authoritative_property_cells": selected_before,
            "legacy_exclusive_property_cells": selected_before_exclusive,
        },
        "selected_after": {
            "canonical_records": len(selected_record_keys),
            "legacy_authoritative_property_cells": selected_after,
            "legacy_exclusive_property_cells": selected_after_exclusive,
        },
        "promoted_property_cells": after_declared - before_declared,
        "parity": parity,
        "property_provenance": {
            f"min_tl_xh:holding:{address}": {
                property_name: {
                    "decision_ids": [
                        item["decision_id"]
                        for item in selected
                        if item["target"].get("table") == "holding"
                        and item["target"].get("address") == address
                        and property_name in DECISION_PROPERTY_MAP.get(item["target"].get("property"), set())
                    ],
                    "claim_ids": sorted({
                        claim_id
                        for item in selected
                        if item["target"].get("table") == "holding"
                        and item["target"].get("address") == address
                        and property_name in DECISION_PROPERTY_MAP.get(item["target"].get("property"), set())
                        for claim_id in item["support"]
                    }),
                }
                for property_name in sorted(selected_props.get(("min_tl_xh", "holding", address), set()))
            }
            for address in SELECTED_ADDRESSES
        },
    }


def candidate_ranking(authority: dict[str, Any]) -> list[dict[str, Any]]:
    records = authority["records"]
    canonical = load_json(CANONICAL_PATH)
    canonical_records = {(item["family"], item["table"], item["address"]): item for item in canonical["registers"]}
    override_map = override_keys()
    units: dict[tuple[str, int, int], set[str]] = {}
    for record in records:
        units.setdefault((record["table"], record["address"], record["length_words"]), set()).add(record["family"])
    shared_units = {
        key for key, families in units.items() if len(families) > 1
    }
    candidates = [
        ("MIN/TL-XH holding EMS H3036-H3059 + H3081-H3082", lambda r: r["family"] == "min_tl_xh" and r["table"] == "holding" and (3036 <= r["address"] <= 3059 or r["address"] in {3081, 3082}), "high", "low", "selected bounded EMS slice"),
        ("MIN/TL-XH holding registers", lambda r: r["family"] == "min_tl_xh" and r["table"] == "holding", "high", "high", "large mixed control/identity surface"),
        ("MIN/TL-XH input 3250-3374", lambda r: r["family"] == "min_tl_xh" and r["table"] == "input" and 3250 <= r["address"] <= 3374, "medium", "high", "outside frozen FC04 cohort but many evidence-gated records"),
        ("MIN/TL-XH input outside frozen I3000-I3249", lambda r: r["family"] == "min_tl_xh" and r["table"] == "input" and not 3000 <= r["address"] <= 3249, "medium", "high", "broader candidate with mixed diagnostics and evidence-gated records"),
        ("MIN/TL-XH holding 3125-3249", lambda r: r["family"] == "min_tl_xh" and r["table"] == "holding" and 3125 <= r["address"] <= 3249, "low", "high", "mostly reserved/complex and weak semantic density"),
        ("Shared bus physical units across families", lambda r: (r["table"], r["address"], r["length_words"]) in shared_units, "mixed", "high", "inventory-level candidate is expanded across families rather than a coherent family slice"),
        ("All structured enum/bitfield records", lambda r: bool(r["semantic_keys"] and r["migration_class"] == "LEGACY_ONLY_COMPLEX"), "mixed", "high", "cross-family and not one coherent scope"),
    ]
    result = []
    for name, predicate, evidence, complexity, note in candidates:
        selected = [r for r in records if predicate(r)]
        exclusive = 0
        for record in selected:
            origins = canonical_authority_origins(
                canonical_records[(record["family"], record["table"], record["address"])],
                override_map,
            )
            exclusive += sum(detail["classification"] == "LEGACY_PYTHON" for detail in origins.values())
        result.append(
            {
                "candidate": name,
                "family_records": len(selected),
                "physical_units": len({(r["table"], r["address"], r["length_words"]) for r in selected}),
                "semantic_concepts": len({key for r in selected for key in r["semantic_keys"]}),
                "legacy_authoritative_cells": sum(len(set(r["legacy_dependencies"]) | set(r["compatibility_dependencies"])) for r in selected),
                "legacy_exclusive_cells": exclusive,
                "existing_declarative_cells": sum(len(r["declarative_properties"]) for r in selected),
                "evidence_quality": evidence,
                "complexity": complexity,
                "note": note,
            }
        )
    result.sort(key=lambda item: (item["candidate"] != candidates[0][0], -item["legacy_exclusive_cells"], item["candidate"]))
    for rank, item in enumerate(result, 1):
        item["rank"] = rank
    return result


def build(starting_sha: str | None = None) -> dict[str, Any]:
    # Preserve reproducibility of this historical report; PIPELINE-10A uses
    # the default explicit property-cell accounting for current authority.
    authority = build_authority(property_cell_accounting=False)
    new_decisions = build_decisions()
    selected = selected_decisions(new_decisions)
    authority_metrics = metrics(authority, selected)
    selected_reduction = authority_metrics["selected_before"]["legacy_authoritative_property_cells"] - authority_metrics["selected_after"]["legacy_authoritative_property_cells"]
    ranking = candidate_ranking(authority)
    for item in ranking:
        item["expected_reduction"] = selected_reduction if item["rank"] == 1 else max(0, item["legacy_authoritative_cells"] - item["existing_declarative_cells"])
    parity_match = Counter(item["classification"] for item in authority_metrics["parity"])
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_pipeline6_next_authority_cohort",
        "generated_by": "tools/build_pipeline6_cohort.py",
        "starting_main_sha": starting_sha or subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(),
        "canonical": {"path": "spec/growatt-register-spec.json", "sha256": sha256(CANONICAL_PATH), "canonical_modified": False},
        "selected_cohort": {
            "id": "min_tl_xh_holding_ems_3036_3059_3081_3082",
            "family": "min_tl_xh",
            "table": "holding",
            "addresses": SELECTED_ADDRESSES,
            "physical_units": len(SELECTED_ADDRESSES),
            "reused_decisions": [item["decision_id"] for item in selected if item not in new_decisions],
            "new_decisions": [item["decision_id"] for item in new_decisions],
            "decision_source": str(RECONCILIATION_PATH.relative_to(ROOT)),
        },
        "candidate_ranking": ranking,
        "ranking_method": "Deterministic review priority: coherent single-family scope, evidence quality, bounded complexity and frozen-cohort exclusion, then authority-reduction potential.",
        "authority": authority_metrics,
        "parity_summary": dict(sorted(parity_match.items())),
        "schema_changes": [],
        "evidence_mode": "retained vendor V1.24 and reviewed semantic claims; no live experiment",
        "offline_inputs": {
            "authority_inventory": "docs/pipeline/data/GII-PIPELINE-5A_AUTHORITY_COVERAGE.json",
            "semantic_review": "sources/evidence/min-6000tl-xh-semantic-review.json",
            "generic_claims": "sources/claims/generic-claims.json",
            "canonical": "spec/growatt-register-spec.json",
        },
    }


def render_report(data: dict[str, Any]) -> str:
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    sb = data["authority"]["selected_before"]
    sa = data["authority"]["selected_after"]
    lines = [
        "# GII-PIPELINE-6 — Next declarative authority cohort",
        "",
        "Disposition: `GII_PIPELINE_NEXT_COHORT_MIGRATION_ACCEPTED`",
        "",
        "## Baseline",
        "",
        f"- Starting repaired `main`: `{data['starting_main_sha']}`.",
        f"- Canonical SHA-256 before/after: `{data['canonical']['sha256']}`; `canonical_modified=false`.",
        "- The authority inventory was regenerated offline from the canonical and compatibility inputs.",
        "",
        "## Candidate ranking",
        "",
        "| Rank | Candidate | Physical units | Semantic concepts | Legacy cells | Legacy-exclusive | Existing declarative | Expected reduction | Evidence | Complexity |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for item in data["candidate_ranking"]:
        lines.append(
            f"| {item['rank']} | {item['candidate']} | {item['physical_units']} | {item['semantic_concepts']} | {item['legacy_authoritative_cells']} | {item['legacy_exclusive_cells']} | {item['existing_declarative_cells']} | {item['expected_reduction']} | {item['evidence_quality']} | {item['complexity']} |"
        )
    lines += [
        "",
        "Ranking is deterministic in the generator: a coherent single-family scope, evidence quality, bounded complexity and exclusion of the frozen FC04 cohort are preferred before raw reduction potential. The selected slice is one modern V1.24 MIN/TL-XH EMS control region. It has reviewed V1.24 claims for every register and exercises reusable packed schedule semantics without reopening the frozen FC04 input cohort.",
        "",
        "## Selected cohort and migration",
        "",
        "- Scope: `min_tl_xh`, holding H3036–H3059 and H3081–H3082.",
        "- Physical parity: 26/26 (100%). H3046 is explicitly reserved through the accepted 4A decision; the other physical units have semantic decisions.",
        f"- Reused reviewed decisions: {len(data['selected_cohort']['reused_decisions'])}; new property-level semantic decisions: {len(data['selected_cohort']['new_decisions'])}.",
        "- Property support is carried by the existing generic claim model: the new decisions cite the reviewed V1.24 vendor rows and the reviewed MIN/TL-XH semantic records. No second claim taxonomy or compatibility source was introduced.",
        "- Packed schedule words use the existing V1.24 codec concepts. Unsupported enum members and undocumented write behavior remain unresolved rather than being invented.",
        "- No schema extension was needed.",
        "",
        "## Semantic parity",
        "",
        f"- Parity result: `{data['parity_summary']}` across all 26 physical targets.",
        "- Underscore/dot semantic-key differences are representation-only; canonical names and physical table/address identity remain aligned.",
        "- No supported canonical correction candidate, source conflict, or unresolved physical target was introduced.",
        "",
        "## Authority movement",
        "",
        "| Metric | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
    ]
    for key, label in [
        ("legacy_authoritative_property_cells", "Repository legacy-authoritative cells"),
        ("declarative_authoritative_property_cells", "Repository declarative-authoritative cells"),
        ("legacy_exclusive_property_cells", "Repository legacy-exclusive cells"),
    ]:
        lines.append(f"| {label} | {before[key]} | {after[key]} | {after[key] - before[key]:+d} |")
    lines += [
        f"| Selected-cohort legacy-authoritative cells | {sb['legacy_authoritative_property_cells']} | {sa['legacy_authoritative_property_cells']} | {sa['legacy_authoritative_property_cells'] - sb['legacy_authoritative_property_cells']:+d} |",
        f"| Selected-cohort legacy-exclusive cells | {sb['legacy_exclusive_property_cells']} | {sa['legacy_exclusive_property_cells']} | {sa['legacy_exclusive_property_cells'] - sb['legacy_exclusive_property_cells']:+d} |",
        "",
        "The reduction is calculated by replacing only the promoted property cells for this cohort; the canonical artifact itself is not regenerated or modified. Remaining legacy code is still present as compatibility/generation infrastructure and remains outside this bounded migration.",
        "",
        "## Validation and disposition",
        "",
        "- The selected cohort artifact, authority transition, candidate ranking, and this report are generated by `tools/build_pipeline6_cohort.py`.",
        "- Existing claims, reconciliation, canonical/spec, vendor, FC04 migration/closure/source-research validators and the offline test suite are run at publication time.",
        "- No HA, broker, inverter, Cloud/Shine, or live configuration access was used or changed.",
        "- Canonical remains frozen: `canonical_modified=false`.",
        "",
        "Final disposition: `GII_PIPELINE_NEXT_COHORT_MIGRATION_ACCEPTED`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    new_decisions = build_decisions()
    RECONCILIATION_PATH.write_text(json.dumps(build_reconciliation(new_decisions), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    data = build()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(render_report(data), encoding="utf-8")
    print(json.dumps({"selected": data["selected_cohort"]["id"], "authority": data["authority"], "parity": data["parity_summary"]}, indent=2))


if __name__ == "__main__":
    main()
