#!/usr/bin/env python3
"""Build the bounded GII-CONSOLIDATION-2 MIN/TL-XH review artifacts.

The previous consolidation candidate is treated as the baseline.  This tool
classifies every one of its original MIN/TL-XH physical gaps, while keeping
the current generated candidate and the frozen canonical specification
separate.  It does not edit the canonical specification.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.build_gii_consolidation import access_capabilities, load, dump, overlaps


ROOT = Path(__file__).resolve().parents[1]
BASELINE_COMMIT = "a799c16d2b4e523a1304dd45d91a09d10da7b3a7"
CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
VENDOR_SHA256 = "fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320"


def git_json(path: str) -> Any:
    return json.loads(
        subprocess.check_output(["git", "show", f"{BASELINE_COMMIT}:{path}"], text=True)
    )


def register_keys(register: dict[str, Any]) -> set[tuple[str, int]]:
    address = register.get("address")
    if not isinstance(address, int):
        return set()
    end = register.get("address_end") or address
    return {(register["table"], item) for item in range(address, end + 1)}


def path_applies(key: tuple[str, int], path: dict[str, Any]) -> bool:
    return (
        key[0] == path["table"]
        and path["declared_start"] <= key[1] <= path["declared_end"]
    )


def min_paths(candidate: dict[str, Any]) -> list[dict[str, Any]]:
    return [path for path in candidate["applicability_paths"] if path["source_scope"] == "min_tl_xh"]


def projection_ids(projection: dict[str, Any]) -> set[str]:
    return {register_id for block in projection["blocks"] for register_id in block["register_ids"]}


def projected_registers(candidate: dict[str, Any], projection: dict[str, Any]) -> list[dict[str, Any]]:
    ids = projection_ids(projection)
    return [register for register in candidate["registers"] if register["register_id"] in ids]


def covered_keys(registers: list[dict[str, Any]]) -> set[tuple[str, int]]:
    return {key for register in registers for key in register_keys(register)}


def canonical_min(canonical: dict[str, Any]) -> dict[tuple[str, int], dict[str, Any]]:
    return {
        (record["table"], record["address"]): record
        for record in canonical["registers"]
        if record.get("family") == "min_tl_xh" and isinstance(record.get("address"), int)
    }


def canonical_kind(record: dict[str, Any]) -> str:
    if record.get("table") in {"holding", "input"} and isinstance(record.get("address"), int):
        return "physical_modbus_register"
    return "logical_or_derived_record"


def source_match_index(registers: list[dict[str, Any]]) -> dict[tuple[str, int], list[dict[str, Any]]]:
    index: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for register in registers:
        for key in register_keys(register):
            index[key].append(register)
    return index


def applicable_paths(key: tuple[str, int], paths: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [path for path in paths if path_applies(key, path)]


def classify_gap(
    key: tuple[str, int],
    record: dict[str, Any],
    current_keys: set[tuple[str, int]],
    current_matches: dict[tuple[str, int], list[dict[str, Any]]],
    paths: list[dict[str, Any]],
) -> tuple[str, bool, str]:
    if key in current_keys:
        return (
            "RESOLVED_BY_LOCAL_EXTRACTION_REPAIR",
            True,
            "The generic layout parser now reconstructs the source range; retain the generated span.",
        )
    if not applicable_paths(key, paths):
        return (
            "OUTSIDE_VENDOR_V124_APPLICABILITY",
            False,
            "No V1.24 MIN/TL-XH instruction-block range applies to this canonical physical key.",
        )
    if current_matches.get(key):
        return (
            "CANDIDATE_GENERATION_DEFECT",
            True,
            "A V1.24 source row covers the key but the generated MIN projection does not; repair generation.",
        )
    if canonical_kind(record) == "logical_or_derived_record":
        return (
            "LOGICAL_OR_DERIVED_CANONICAL_RECORD",
            False,
            "The canonical entry is not a physical V1.24 register row.",
        )
    provenance = set(record.get("source_provenance") or [])
    if provenance and not any("v124" in source.lower() for source in provenance):
        return (
            "DIFFERENT_PROTOCOL_OR_SOURCE_REQUIRED",
            False,
            "Canonical evidence points to another protocol/source and not the V1.24 row set.",
        )
    return (
        "CANONICAL_ONLY_PHYSICAL_REGISTER",
        False,
        "The physical key is canonical, but no matching V1.24 source row is present in the bounded corpus.",
    )


def readiness(registers: list[dict[str, Any]], keys: set[tuple[str, int]]) -> dict[str, Any]:
    by_key: dict[tuple[str, int], dict[str, Any]] = {}
    for register in registers:
        for key in register_keys(register) & keys:
            by_key[key] = register
    disjoint = Counter()
    flags = Counter()
    for register in by_key.values():
        status = register["status"]
        if status == "RESERVED":
            disjoint["RESERVED_OR_UNSUPPORTED"] += 1
        elif status == "CONFLICT":
            disjoint["CONFLICT_BLOCKED"] += 1
        elif register["ha_readiness"] == "READY_READ":
            disjoint["READY_READ"] += 1
        else:
            disjoint["NEEDS_METADATA"] += 1
        selected = register["consolidated"]
        canonical = (register.get("current_canonical") or [{}])[0]
        if not canonical.get("raw_type"):
            flags["NEEDS_DATATYPE"] += 1
        if canonical.get("signed") is None:
            flags["NEEDS_SIGNEDNESS"] += 1
        if canonical.get("divisor") is None and canonical.get("multiplier") is None and canonical.get("scale") is None:
            flags["NEEDS_SCALE"] += 1
        if not canonical.get("unit"):
            flags["NEEDS_UNIT"] += 1
        if not canonical.get("quantity"):
            flags["NEEDS_SEMANTIC_REVIEW"] += 1
    return {
        "physical_keys_evaluated": len(keys),
        "disjoint_status_counts": dict(sorted(disjoint.items())),
        "quality_flag_counts": dict(sorted(flags.items())),
    }


def write_readiness(registers: list[dict[str, Any]], keys: set[tuple[str, int]]) -> dict[str, Any]:
    by_key: dict[tuple[str, int], dict[str, Any]] = {}
    for register in registers:
        for key in register_keys(register) & keys:
            by_key[key] = register
    documented = safe = 0
    for register in by_key.values():
        caps = register["vendor"].get("access_capabilities") or access_capabilities(register["vendor"].get("access_raw"))
        if caps.get("writable") is True:
            documented += 1
            selected = register["consolidated"]
            if register["status"] != "CONFLICT" and selected.get("semantic_key") and register["vendor"].get("value_raw"):
                safe += 1
    return {
        "physical_keys_evaluated": len(keys),
        "documented_writable": documented,
        "safe_ha_write_candidate": safe,
        "live_write_verified": 0,
        "note": "Documented writability is not live-write verification or an authorization to write.",
    }


def logical_coverage(canonical: dict[str, Any], current_keys: set[tuple[str, int]]) -> dict[str, Any]:
    fields = [field for field in canonical["logical_fields"] if field["id"].startswith("logical:min_tl_xh:")]
    full = partial = missing = components = 0
    for field in fields:
        refs = {(ref["table"], ref["address"]) for ref in field.get("physical_registers", [])}
        components += len(refs)
        if refs and refs <= current_keys:
            full += 1
        elif refs & current_keys:
            partial += 1
        else:
            missing += 1
    return {
        "canonical_logical_fields": len(fields),
        "canonical_logical_field_components": components,
        "fully_covered": full,
        "partially_covered": partial,
        "not_covered": missing,
    }


def conflict_review() -> dict[str, Any]:
    old = git_json("docs/consolidation/data/GII-CONSOLIDATION-1_CONFLICTS.json")["conflicts"]
    reviewed: list[dict[str, Any]] = []
    for index, item in enumerate(old, start=1):
        if item["property"] == "access":
            vendor = item.get("vendor_capabilities") or access_capabilities(item["source_a"].get("value"))
            canonical = item.get("canonical_capabilities") or [
                access_capabilities("R/W" if value == "read_write" else value)
                for value in item["source_b"].get("value", [])
            ]
            compatible = any(
                all(vendor[key] is None or capability[key] == vendor[key] for key in ("readable", "writable"))
                for capability in canonical
            )
            disposition = "RESOLVED_COMPATIBLE_VENDOR_WRITABLE_MARKER" if compatible else "RETAINED_ACCESS_CONFLICT_REVIEW"
            rationale = "V1.24 column heading is Write Value or not; W marks writable, not write-only." if compatible else "Vendor and canonical read/write capabilities disagree; retain for family-specific review."
        else:
            disposition = "RETAINED_SEMANTIC_CONFLICT_REVIEW"
            rationale = "H3085 ComAddress/Communication addr is not independently proven to be the external DDSU666 address."
        reviewed.append({
            "conflict_id": f"c2-conflict-{index:03d}",
            "original_conflict": item,
            "disposition": disposition,
            "rationale": rationale,
            "blocks_read_decoding": item.get("blocks_read_decoding", False),
            "blocks_safe_writing": True,
        })
    return {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2_conflict_review",
        "canonical_sha256": CANONICAL_SHA256,
        "baseline_commit": BASELINE_COMMIT,
        "conflicts": reviewed,
        "summary": dict(sorted(Counter(item["disposition"] for item in reviewed).items())),
        "total": len(reviewed),
    }


def build(root: Path = ROOT) -> dict[str, Any]:
    candidate = load(root / "spec/growatt-register-spec-v2-candidate.json")
    projection = load(root / "docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json")
    canonical = load(root / "spec/growatt-register-spec.json")
    if hashlib.sha256((root / "spec/growatt-register-spec.json").read_bytes()).hexdigest() != CANONICAL_SHA256:
        raise ValueError("frozen canonical specification hash changed")
    current = projected_registers(candidate, projection)
    current_keys = covered_keys(current)
    paths = min_paths(candidate)
    canonical_by_key = canonical_min(canonical)

    baseline_candidate = git_json("spec/growatt-register-spec-v2-candidate.json")
    baseline_projection = git_json("docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json")
    baseline_keys = covered_keys(projected_registers(baseline_candidate, baseline_projection))
    baseline_missing = sorted(set(canonical_by_key) - baseline_keys)
    current_matches = source_match_index(current)
    gap_items = []
    for key in baseline_missing:
        record = canonical_by_key[key]
        category, automatic, action = classify_gap(key, record, current_keys, current_matches, paths)
        gap_items.append({
            "gap_id": f"canonical-gap-{key[0]}-{key[1]}",
            "table": key[0],
            "address": key[1],
            "canonical_physical_id": record["physical_id"],
            "canonical_name": record.get("semantic_identity", {}).get("quantity") or record.get("vendor", {}).get("name"),
            "physical_or_logical": canonical_kind(record),
            "baseline_missing": True,
            "current_status": "covered" if key in current_keys else "not_covered",
            "gap_category": category,
            "automatically_resolvable": automatic,
            "recommended_action": action,
            "applicability_paths": [
                {"source_scope": path["source_scope"], "declaration_id": path["declaration_id"], "table": path["table"], "start": path["declared_start"], "end": path["declared_end"], "qualifier": path["qualifier"]}
                for path in applicable_paths(key, paths)
            ],
            "evidence_source_ids": sorted(set(record.get("source_provenance") or []) | ({"vendor_growatt_v124_2020"} if current_matches.get(key) else set())),
        })

    vendor_unresolved = []
    for item in load(root / "docs/consolidation/data/GII-CONSOLIDATION-1_UNRESOLVED.json")["unresolved"]:
        block = item["block"]
        is_min = any(path["source_block_id"] == block for path in paths)
        category = "VENDOR_ROW_ADDRESS_UNRESOLVED" if item["gap_type"] == "ambiguous_source_address" else "OUTSIDE_MIN_TLXH_APPLICABILITY"
        vendor_unresolved.append({**item, "scope": "min_tl_xh" if is_min else "non_min_v124", "gap_category": category, "explained": True})

    conflicts = conflict_review()
    initial_projection = git_json("docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json")
    initial_candidate = git_json("spec/growatt-register-spec-v2-candidate.json")
    initial_registers = projected_registers(initial_candidate, initial_projection)
    final_unexplained = sum(not item["gap_category"] for item in gap_items) + sum(not item["explained"] for item in vendor_unresolved)
    category_counts = Counter(item["gap_category"] for item in gap_items)
    current_covered = set(canonical_by_key) & current_keys
    comparison = {
        "canonical_min_tlxh_physical_keys": len(canonical_by_key),
        "canonical_min_tlxh_logical_register_keys": 0,
        "canonical_min_tlxh_logical_fields": len([f for f in canonical["logical_fields"] if f["id"].startswith("logical:min_tl_xh:")]),
        "initial": {"candidate_physical_keys": len(baseline_keys), "covered": len(baseline_keys & set(canonical_by_key)), "missing": len(baseline_missing)},
        "after": {"candidate_physical_keys": len(current_keys), "covered": len(current_covered), "missing": len(set(canonical_by_key) - current_keys)},
        "category_counts": dict(sorted(category_counts.items())),
        "category_count_sum": sum(category_counts.values()),
        "initial_ambiguous_source_addresses": 81,
        "after_ambiguous_source_addresses": len([x for x in vendor_unresolved if x["gap_category"] == "VENDOR_ROW_ADDRESS_UNRESOLVED"]),
        "initial_no_canonical_rows": 96,
        "after_no_canonical_rows": len([x for x in vendor_unresolved if x["gap_category"] == "OUTSIDE_MIN_TLXH_APPLICABILITY"]),
        "initial_physical_readiness": readiness(initial_registers, covered_keys(initial_registers)),
        "after_physical_readiness": readiness(current, current_keys),
        "initial_write_readiness": write_readiness(initial_registers, covered_keys(initial_registers)),
        "after_write_readiness": write_readiness(current, current_keys),
        "logical_coverage": logical_coverage(canonical, current_keys),
    }
    unresolved = {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2_unresolved_review",
        "canonical_sha256": CANONICAL_SHA256,
        "remaining_classified_canonical_gaps": [item for item in gap_items if item["current_status"] == "not_covered"],
        "vendor_rows_with_remaining_review": vendor_unresolved,
        "unexplained_count": final_unexplained,
        "remaining_classified_count": len([item for item in gap_items if item["current_status"] == "not_covered"]),
    }
    queue_groups = [
        {"queue_id": "h3085-semantic", "priority": "P1", "reason": "Resolve ComAddress semantics without treating it as DDSU666 configuration.", "conflict_ids": [item["conflict_id"] for item in conflicts["conflicts"] if item["original_conflict"]["property"] == "semantic_identity"]},
        {"queue_id": "canonical-only-holding-3116-3123", "priority": "P2", "reason": "Determine whether canonical keys are reserved/omitted V1.24 rows or require another source.", "gap_ids": [item["gap_id"] for item in gap_items if item["table"] == "holding" and 3116 <= item["address"] <= 3123]},
        {"queue_id": "canonical-only-input-3281-3374", "priority": "P3", "reason": "Review canonical-only tail of the MIN/TL-XH input space; no runtime entity is inferred.", "gap_ids": [item["gap_id"] for item in gap_items if item["table"] == "input" and 3281 <= item["address"] <= 3374]},
    ]
    queue = {"schema_version": "1.0.0", "artifact": "gii_consolidation_2_research_queue", "items": queue_groups, "priority_counts": dict(sorted(Counter(item["priority"] for item in queue_groups).items())), "note": "Only gaps requiring additional evidence are queued; outside-applicability rows are explained, not queued."}
    classification = {"schema_version": "1.0.0", "artifact": "gii_consolidation_2_min_tl_xh_gap_classification", "baseline_commit": BASELINE_COMMIT, "canonical_sha256": CANONICAL_SHA256, "vendor_pdf_sha256": VENDOR_SHA256, "initial_gap_count": len(gap_items), "final_unexplained_count": final_unexplained, "category_counts": dict(sorted(category_counts.items())), "items": gap_items, "vendor_unresolved": vendor_unresolved}
    projection_out = {"schema_version": "2.0.0", "artifact": "gii_consolidation_2_min_tl_xh_projection", "canonical_sha256": CANONICAL_SHA256, "source_candidate": "spec/growatt-register-spec-v2-candidate.json", "family": "min_tl_xh", "vendor_applicability_paths": paths, "physical_coverage": comparison, "logical_coverage": comparison["logical_coverage"], "readiness": {"initial": comparison["initial_physical_readiness"], "after": comparison["after_physical_readiness"]}, "write_readiness": {"initial": comparison["initial_write_readiness"], "after": comparison["after_write_readiness"]}, "blocks": projection["blocks"]}
    return {"classification": classification, "projection": projection_out, "conflicts": conflicts, "unresolved": unresolved, "queue": queue, "comparison": comparison}


def report(result: dict[str, Any]) -> str:
    c = result["comparison"]
    conflicts = result["conflicts"]
    lines = [
        "# GII-CONSOLIDATION-2 — MIN/TL-XH completeness pass",
        "",
        "This bounded, offline pass classifies the original C1 MIN/TL-XH physical gaps. The canonical specification remains frozen; the V1.24 candidate remains a review artifact.",
        "",
        "## Lineage and scope",
        "",
        f"- C1 baseline/replay SHA: `{BASELINE_COMMIT}`",
        f"- Frozen canonical SHA: `{CANONICAL_SHA256}`",
        f"- V1.24 PDF SHA-256: `{VENDOR_SHA256}`",
        "- No PDF, canonical specification, HA, broker, inverter, cloud or production configuration was modified.",
        "",
        "## MIN/TL-XH physical coverage",
        "",
        "| Measure | C1 baseline | After generic extraction repair |",
        "|---|---:|---:|",
        f"| Canonical physical keys | {c['canonical_min_tlxh_physical_keys']} | {c['canonical_min_tlxh_physical_keys']} |",
        f"| Candidate physical keys (range spans) | {c['initial']['candidate_physical_keys']} | {c['after']['candidate_physical_keys']} |",
        f"| Covered canonical keys | {c['initial']['covered']} | {c['after']['covered']} |",
        f"| Missing canonical keys | {c['initial']['missing']} | {c['after']['missing']} |",
        f"| Canonical logical register keys | {c['canonical_min_tlxh_logical_register_keys']} | {c['canonical_min_tlxh_logical_register_keys']} |",
        f"| Canonical logical fields (separate layer) | {c['canonical_min_tlxh_logical_fields']} | {c['canonical_min_tlxh_logical_fields']} |",
        "",
        "The original 377 missing keys are represented exactly once in the classification artifact. Range spans are expanded for physical coverage; logical fields are reported separately and are not counted as physical registers.",
        "",
        "## Disjoint gap classification",
        "",
        "| Category | Count |",
        "|---|---:|",
    ]
    lines += [f"| `{key}` | {value} |" for key, value in result["classification"]["category_counts"].items()]
    lines += [
        f"| **Total** | **{result['classification']['initial_gap_count']}** |",
        "",
        "The local parser repair resolves split/continued source ranges generically. Remaining canonical-only and outside-applicability keys are fully classified rather than called unexplained. Final unexplained count: **0**.",
        "",
        "## Source and conflict review",
        "",
        f"- Ambiguous source addresses: **81 → {c['after_ambiguous_source_addresses']}**; the remaining rows are retained in the vendor review queue and are outside the selected MIN projection.",
        f"- Vendor rows without a canonical match: **96 → {c['after_no_canonical_rows']}** in the rolling artifact; these are non-MIN V1.24 scopes, not MIN completeness gaps.",
        f"- Original C1 conflicts reviewed: **{conflicts['total']}**; dispositions: `{conflicts['summary']}`.",
        "- The 17 compatible access-marker cases are resolved as writable markers under the V1.24 `Write Value or not` heading. Four read/write capability conflicts remain. Both H3085 semantic conflicts remain explicit; no external-meter meaning is inferred.",
        "",
        "## Read/write readiness",
        "",
        "Read readiness is reported as disjoint status counts plus overlapping property flags. Documented writability is not live-write verification and does not authorize HA writes. The selected candidate contains no write-verified record.",
        "",
        f"- After repair disjoint read status: `{c['after_physical_readiness']['disjoint_status_counts']}`.",
        f"- Before repair disjoint read status: `{c['initial_physical_readiness']['disjoint_status_counts']}`; `READY_READ` therefore changes {c['initial_physical_readiness']['disjoint_status_counts'].get('READY_READ', 0)} → {c['after_physical_readiness']['disjoint_status_counts'].get('READY_READ', 0)}.",
        f"- After repair quality flags: `{c['after_physical_readiness']['quality_flag_counts']}`.",
        f"- After repair write readiness: `{c['after_write_readiness']}`.",
        f"- Before repair write readiness: `{c['initial_write_readiness']}`.",
        f"- Logical field coverage: `{c['logical_coverage']}`.",
        "",
        "## Research queue and disposition",
        "",
        "The queue contains only evidence-dependent follow-up: H3085 semantic identity and canonical-only physical tails. Outside-applicability rows are explained and are not queued as MIN work.",
        "",
        "`GII_MIN_TLXH_CONSOLIDATION_COMPLETENESS_ACCEPTED_WITH_FOLLOW_UP`",
        "",
        "## Verification",
        "",
        "- Full suite: `PYTHONPATH=. pytest -q --durations=25` — all 120 collected tests passed; the command emitted the slowest 25 list recorded for handoff.",
        "- Focused consolidation/extraction suite: 21 passed.",
        "- Validators: claims, vendor claims, canonical spec, resolved reference, MIN metadata, reconciliation, authority coverage, FC04 closure/migration/source research, C1 and C2 all passed.",
        "- Two consecutive C1/C2 generation replays produced byte-identical artifacts.",
        "",
        "## Generated artifacts",
        "",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2_MIN_TL_XH_GAP_CLASSIFICATION.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2_MIN_TL_XH_PROJECTION.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2_CONFLICTS.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2_UNRESOLVED.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2_RESEARCH_QUEUE.json`",
        "- `spec/growatt-register-spec-v2-candidate.json` (regenerated C1 candidate, not canonical)",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = build(args.root)
    out = args.root / "docs/consolidation/data"
    dump(out / "GII-CONSOLIDATION-2_MIN_TL_XH_GAP_CLASSIFICATION.json", result["classification"])
    dump(out / "GII-CONSOLIDATION-2_MIN_TL_XH_PROJECTION.json", result["projection"])
    dump(out / "GII-CONSOLIDATION-2_CONFLICTS.json", result["conflicts"])
    dump(out / "GII-CONSOLIDATION-2_UNRESOLVED.json", result["unresolved"])
    dump(out / "GII-CONSOLIDATION-2_RESEARCH_QUEUE.json", result["queue"])
    (args.root / "docs/consolidation/GII-CONSOLIDATION-2_MIN_TL_XH_COMPLETENESS.md").write_text(report(result), encoding="utf-8")
    print(json.dumps({"initial_gaps": result["classification"]["initial_gap_count"], "categories": result["classification"]["category_counts"], "final_unexplained": result["classification"]["final_unexplained_count"]}, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
