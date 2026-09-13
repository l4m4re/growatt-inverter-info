#!/usr/bin/env python3
"""Build the deterministic shadow candidate from declarative decisions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def read(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def build() -> dict[str, Any]:
    claims = {item["claim_id"]: item for item in read("sources/claims/generic-claims.json")["claims"]}
    decisions: list[dict[str, Any]] = []
    for path in sorted(ROOT.glob("reconciliation/*.json")):
        if path.name in {"resolved-assertions.json", "validation-report.json", "scope-mappings.json"}:
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        for decision in data.get("decisions", []):
            missing = [claim_id for claim_id in decision["support"] if claim_id not in claims]
            missing.extend(item["claim_id"] for item in decision["conflicts"] if item["claim_id"] not in claims)
            if missing:
                raise ValueError(f"{decision['decision_id']} has missing claim IDs: {missing}")
            decisions.append({**decision, "decision_source": str(path.relative_to(ROOT))})
    decisions.sort(key=lambda item: item["decision_id"])
    counts: dict[str, int] = {}
    for item in decisions:
        status = item["decision"]["status"]
        counts[status] = counts.get(status, 0) + 1
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_reconciled_candidate_assertions",
        "generated_by": "tools/build_reconciliation.py",
        "source_claims": "sources/claims/generic-claims.json",
        "decisions": decisions,
        "decision_counts": dict(sorted(counts.items())),
        "canonical_status": "shadow_only_not_canonical",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="reconciliation/resolved-assertions.json")
    args = parser.parse_args()
    result = build()
    (ROOT / args.output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"generated {len(result['decisions'])} decisions: {result['decision_counts']}")


if __name__ == "__main__":
    main()
