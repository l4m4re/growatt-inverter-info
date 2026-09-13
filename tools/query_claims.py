#!/usr/bin/env python3
"""Small read-only query tool for the unresolved generic claim set."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--claims", default="sources/claims/generic-claims.json")
    parser.add_argument("--family")
    parser.add_argument("--table", choices=("holding", "input"))
    parser.add_argument("--address", type=int)
    parser.add_argument("--source")
    parser.add_argument("--kind")
    parser.add_argument("--namespace")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args()
    data: dict[str, Any] = json.loads((ROOT / args.claims).read_text(encoding="utf-8"))
    matches = []
    for item in data["claims"]:
        sub = item["subject"]
        family_values = sub.get("family_scope", [])
        family_text = " ".join(family_values) if isinstance(family_values, list) else str(family_values)
        if args.family and args.family.lower() not in family_text.lower(): continue
        if args.table and sub.get("table") != args.table: continue
        if args.address is not None and not (sub.get("address") <= args.address <= sub.get("address_end", sub.get("address", -1))): continue
        if args.source and item["source_id"] != args.source: continue
        if args.kind and item["assertion"]["kind"] != args.kind: continue
        if args.namespace and sub["namespace"] != args.namespace: continue
        matches.append(item)
    if args.as_json:
        print(json.dumps(matches, indent=2, ensure_ascii=False))
        return
    for item in matches:
        sub = item["subject"]
        location = sub.get("logical_object") or f"{sub.get('table','')}{sub.get('address','')}"
        value = json.dumps(item["assertion"]["value"], ensure_ascii=False, separators=(",", ":"))
        if len(value) > 180: value = value[:177] + "..."
        prov = item["provenance"]
        exact = prov.get("json_pointer") or f"page {prov.get('page')} row {prov.get('source_row')}"
        print(f"{location:24} {item['source_id']:26} {item['assertion']['kind']:32} {item['evidence']['confidence']:14} {exact}: {value}")
    print(f"count={len(matches)}")


if __name__ == "__main__":
    main()
