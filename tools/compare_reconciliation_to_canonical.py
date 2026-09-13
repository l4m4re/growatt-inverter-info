#!/usr/bin/env python3
"""Compare the reconciliation shadow with canonical output, read-only."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PARITY = [("input", address) for address in [3000, 3101, 3165, 3166, 3170, 3211, 3212, 3217]] + [("holding", address) for address in [3036, 3037, 3047, 3048, 3049, 3081, 3082]]


def normalize_key(value: Any) -> Any:
    if not isinstance(value, str): return value
    return value


def semantic_keys_match(candidate: Any, current: Any) -> bool:
    if not isinstance(candidate, str) or not isinstance(current, str):
        return False
    return candidate == current or candidate.replace("_", ".") == current or candidate == current.replace(".", "_")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="reconciliation/compare-to-canonical.json")
    args = parser.parse_args()
    candidate = json.loads((ROOT / "reconciliation/resolved-assertions.json").read_text())
    canonical = json.loads((ROOT / "spec/growatt-register-spec.json").read_text())
    records = {(item["table"], item["address"]): item for item in canonical["registers"] if item["family"] == "min_tl_xh"}
    physical = [item for item in candidate["decisions"] if item["target"]["namespace"] == "MODBUS" and "address" in item["target"]]
    comparisons = []
    for item in physical:
        target = item["target"]
        current = records.get((target.get("table"), target.get("address")))
        candidate_value = item["decision"]["value"]
        current_value = current.get("semantic_identity", {}).get("quantity") if current else None
        candidate_key = candidate_value.get("semantic_key") if isinstance(candidate_value, dict) else None
        comparisons.append({
            "decision_id": item["decision_id"],
            "physical_id": f"{target.get('table')}:{target.get('address')}",
            "classification": "missing_in_canonical" if current is None else "expected_semantic_delta" if candidate_key and not semantic_keys_match(candidate_key, current_value) else "candidate_available_for_parity_review",
            "candidate_status": item["decision"]["status"],
            "candidate_value": candidate_value,
            "current_canonical_semantic": current_value,
        })
    xh_current = {f"{table}:{address}": records[(table, address)]["normalized"].get("name") for table, address in [("holding", a) for a in range(3038, 3046)] + [("holding", a) for a in range(3050, 3060)]}
    expected = {
        "xh_generic_slots": {"classification":"expected_semantic_correction", "decision_ids":[f"min-xh-slot-{number}" for number in range(1,5)] + ["min-xh-slot-5-through-9"], "candidate":"Slots 1-9 use the same generic priority codec; H3046 is reserved."},
        "schedule_enum_removal": {"classification":"expected_semantic_correction", "decision_id":"min-xh-template-start-control-v124", "candidate":"Only minute/hour/priority/enable fields are retained; parser artifacts such as 6, 7, 12 and 15 are not enum members."},
        "packed_fields_introduction": {"classification":"expected_semantic_correction", "decision_ids":["min-xh-template-start-control-v124","min-xh-template-end-v124"], "candidate":"Reusable packed start/control and end codecs."},
        "current_schedule_names": xh_current,
    }
    parity = []
    for table, address in PARITY:
        relevant = [item for item in physical if item["target"].get("table") == table and item["target"].get("address") == address]
        parity.append({"physical_id":f"{table}:{address}","decision_ids":[item["decision_id"] for item in relevant],"canonical_present":(table,address) in records,"status":relevant[0]["decision"]["status"] if relevant else "missing_in_reconciliation"})
    output = {"schema_version":"1.0.0","artifact":"growatt_reconciliation_shadow_comparison","canonical_input":"spec/growatt-register-spec.json","canonical_modified":False,"comparisons":comparisons,"expected_corrections":expected,"parity":parity}
    (ROOT / args.output).write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n")
    print(f"compared {len(comparisons)} physical decisions; canonical_modified=false")


if __name__ == "__main__":
    main()
