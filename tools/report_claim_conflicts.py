#!/usr/bin/env python3
"""Report differing assertions without choosing a winner."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


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


def build(data: dict[str, Any]) -> dict[str, Any]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in data["claims"]:
        if item["assertion"]["kind"] == "vendor_source_row": continue
        groups[key(item)].append(item)
    conflicts = []
    for group_key, items in sorted(groups.items()):
        values = {json.dumps(item["assertion"]["value"], sort_keys=True, ensure_ascii=False) for item in items}
        if len(values) <= 1: continue
        kind = items[0]["assertion"]["kind"]
        conflicts.append({
            "subject_assertion": json.loads(group_key),
            "category": category(kind),
            "claims": [item["claim_id"] for item in items],
            "values": [item["assertion"]["value"] for item in items],
        })
    return {"schema_version": "1.0.0", "artifact": "growatt_generic_claim_conflicts", "conflicts": conflicts}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", default="sources/claims/generic-claims.json")
    parser.add_argument("--output", default="sources/claims/conflicts.json")
    args = parser.parse_args()
    data = json.loads((ROOT / args.claims).read_text(encoding="utf-8"))
    report = build(data)
    (ROOT / args.output).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    counts = Counter(item["category"] for item in report["conflicts"])
    print(f"conflicts={len(report['conflicts'])} categories={dict(sorted(counts.items()))}")


if __name__ == "__main__":
    main()
