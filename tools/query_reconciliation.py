#!/usr/bin/env python3
"""Show source claims, declarative decisions, and shadow candidate together."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def normalized_scope(family_values: Any, mappings: dict[str, str]) -> str:
    values = family_values if isinstance(family_values, list) else [family_values]
    if not values or any(value in {"unknown", None} for value in values): return "unknown"
    scopes = {mappings.get(value, "unknown") for value in values}
    return next(iter(scopes)) if len(scopes) == 1 else "unknown"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--family", default="min_tl_xh")
    parser.add_argument("--table", choices=("holding", "input"))
    parser.add_argument("--address", type=int)
    parser.add_argument("--logical-object")
    args = parser.parse_args()
    scope_data = json.loads((ROOT / "reconciliation/scope-mappings.json").read_text())
    mappings = {item["source_family"]: item["scope_id"] for item in scope_data["mappings"]}
    claims = json.loads((ROOT / "sources/claims/generic-claims.json").read_text())["claims"]
    decisions = json.loads((ROOT / "reconciliation/resolved-assertions.json").read_text())["decisions"]
    logical_objects_by_address: dict[int, set[str]] = {}
    for item in decisions:
        target = item["target"]
        if target.get("namespace") != "LOGICAL": continue
        value_text = json.dumps(item["decision"].get("value", {}), ensure_ascii=False)
        for raw_address in re.findall(r"[HI](\d{3,5})", value_text):
            logical_objects_by_address.setdefault(int(raw_address), set()).add(target["logical_object"])
    for label, items in (("source assertions", claims), ("reconciliation/candidate", decisions)):
        print(f"[{label}]")
        found = 0
        for item in items:
            sub = item.get("subject", item.get("target", {}))
            value_text = json.dumps(item.get("decision", {}).get("value", {}), ensure_ascii=False)
            logical_reference = item.get("decision") and (
                f"H{args.address}" in value_text or f"I{args.address}" in value_text
            ) if args.address is not None else False
            logical_reference = logical_reference or (
                bool(item.get("decision"))
                and sub.get("logical_object") in logical_objects_by_address.get(args.address, set())
            )
            if args.table and sub.get("table") != args.table and not logical_reference: continue
            if args.address is not None:
                if isinstance(sub.get("address"), int):
                    if not sub.get("address") <= args.address <= sub.get("address_end", sub.get("address", -1)): continue
                elif not logical_reference:
                    continue
            if args.logical_object and sub.get("logical_object") != args.logical_object: continue
            if args.family:
                item_scope = sub.get("canonical_family") or normalized_scope(sub.get("family_scope", []), mappings)
                if item_scope != args.family: continue
            print(json.dumps({"id":item.get("claim_id", item.get("decision_id")),"kind":item.get("assertion", {}).get("kind", item.get("target", {}).get("property")),"status":item.get("decision", {}).get("status", item.get("evidence", {}).get("status")),"value":item.get("assertion", {}).get("value", item.get("decision", {}).get("value"))},ensure_ascii=False))
            found += 1
        print(f"count={found}")


if __name__ == "__main__":
    main()
