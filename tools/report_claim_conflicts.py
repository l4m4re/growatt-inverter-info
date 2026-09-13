#!/usr/bin/env python3
"""Report differing assertions without choosing a winner."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCOPE_PATH = ROOT / "reconciliation/scope-mappings.json"
PIPELINE3_BASELINE = {"count": 201, "categories": {"access_conflict": 1, "value_conflict": 162, "wording_difference": 38}}


def key(item: dict[str, Any]) -> str:
    sub = item["subject"]
    identity = [sub["namespace"], sub.get("table"), sub.get("address"), sub.get("address_end"), sub.get("logical_object"), sub.get("field")]
    return json.dumps([identity, item["assertion"]["kind"]], separators=(",", ":"))


def category(kind: str) -> str:
    if kind == "access": return "access_conflict"
    if kind in {"unit", "scale", "divisor", "multiplier"}: return "unit_conflict"
    if kind in {"datatype", "signedness"}: return "datatype_conflict"
    if kind in {"register_name", "description", "implementation_name"}: return "wording_difference"
    if kind in {"semantic_label", "subsystem", "measurement_point"}: return "semantic_conflict"
    return "value_conflict"


def normalized_scope(item: dict[str, Any], mappings: dict[str, str]) -> str:
    values = item["subject"].get("family_scope", [])
    values = values if isinstance(values, list) else [values]
    if not values or any(value in {"unknown", None} for value in values):
        return "unknown"
    scope_ids = {mappings.get(value, "unknown") for value in values}
    return next(iter(scope_ids)) if len(scope_ids) == 1 else "unknown"


def build(data: dict[str, Any]) -> dict[str, Any]:
    scope_data = json.loads(SCOPE_PATH.read_text(encoding="utf-8"))
    mappings = {item["source_family"]: item["scope_id"] for item in scope_data["mappings"]}
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in data["claims"]:
        if item["assertion"]["kind"] == "vendor_source_row": continue
        groups[key(item)].append(item)
    conflicts = []
    excluded_scope_pairs = 0
    for group_key, items in sorted(groups.items()):
        by_scope: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for item in items:
            by_scope[normalized_scope(item, mappings)].append(item)
        excluded_scope_pairs += sum(len(left) * len(right) for left in by_scope.values() for right in by_scope.values() if left is not right) // 2
        for scope_id, scoped_items in sorted(by_scope.items()):
            values = {json.dumps(item["assertion"]["value"], sort_keys=True, ensure_ascii=False) for item in scoped_items}
            if len(values) <= 1: continue
            kind = scoped_items[0]["assertion"]["kind"]
            conflicts.append({
                "subject_assertion": json.loads(group_key),
                "scope_id": scope_id,
                "category": "potential_scope_conflict" if scope_id == "unknown" else category(kind),
                "claims": [item["claim_id"] for item in scoped_items],
                "values": [item["assertion"]["value"] for item in scoped_items],
            })
    potential = sum(item["category"] == "potential_scope_conflict" for item in conflicts)
    return {"schema_version": "1.0.0", "artifact": "growatt_generic_claim_conflicts", "scope_model": "reconciliation/scope-mappings.json", "pipeline3_baseline": PIPELINE3_BASELINE, "scope_aware_total": len(conflicts), "hard_conflict_count": len(conflicts) - potential, "potential_scope_conflict_count": potential, "excluded_disjoint_or_unknown_scope_pairs": excluded_scope_pairs, "conflicts": conflicts}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", default="sources/claims/generic-claims.json")
    parser.add_argument("--output", default="sources/claims/conflicts.json")
    args = parser.parse_args()
    data = json.loads((ROOT / args.claims).read_text(encoding="utf-8"))
    report = build(data)
    (ROOT / args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = Counter(item["category"] for item in report["conflicts"])
    print(f"conflicts={len(report['conflicts'])} hard={report['hard_conflict_count']} potential_scope={report['potential_scope_conflict_count']} categories={dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
