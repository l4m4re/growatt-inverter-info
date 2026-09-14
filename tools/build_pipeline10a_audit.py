#!/usr/bin/env python3
"""Audit accepted reconciliation decisions at canonical property-cell level."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any

try:
    from tools.build_authority_coverage import DECISION_PROPERTY_MAP
    from tools.pipeline9_candidates import accepted_decisions
    from tools.property_cell_provenance import TRACKED_PROPERTY_CELLS, authority_support_for_decision, property_cell_support, supported_property_cells
except ModuleNotFoundError:
    from build_authority_coverage import DECISION_PROPERTY_MAP
    from pipeline9_candidates import accepted_decisions
    from property_cell_provenance import TRACKED_PROPERTY_CELLS, authority_support_for_decision, property_cell_support, supported_property_cells

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_PATH = ROOT / "sources/claims/generic-claims.json"
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-10A_PROPERTY_CELL_PROVENANCE_AUDIT.json"


def build() -> dict[str, Any]:
    claims_by_id = {
        claim["claim_id"]: claim for claim in json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))["claims"]
    }
    decisions = accepted_decisions()
    audit: list[dict[str, Any]] = []
    old_unique: set[tuple[str, str, int, str]] = set()
    corrected_unique: set[tuple[str, str, int, str]] = set()
    implied_count = corrected_count = 0
    for decision in decisions:
        target = decision.get("target", {})
        if target.get("namespace") != "MODBUS":
            continue
        key = (target["canonical_family"], target["table"], target["address"])
        implied = sorted(DECISION_PROPERTY_MAP.get(target.get("property"), set()))
        supported = sorted(supported_property_cells(decision, claims_by_id))
        support = property_cell_support(decision, claims_by_id)
        implied_count += len(implied)
        corrected_count += len(supported)
        old_unique.update((*key, property_name) for property_name in implied)
        corrected_unique.update((*key, property_name) for property_name in supported)
        audit.append(
            {
                "decision_id": decision["decision_id"],
                "target": key,
                "decision_property": target.get("property"),
                "previously_implied_property_cells": implied,
                "correctly_evidence_supported_property_cells": supported,
                "cells_no_longer_promoted": sorted(set(implied) - set(supported)),
                "property_support": authority_support_for_decision(decision, claims_by_id),
                "support_claim_ids_by_property": {
                    property_name: detail["claim_ids"] for property_name, detail in sorted(support.items())
                },
            }
        )
    audit.sort(key=lambda item: item["decision_id"])
    by_decision_property = Counter(item["decision_property"] for item in audit)
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_pipeline10a_property_cell_provenance_audit",
        "generated_by": "tools/build_pipeline10a_audit.py",
        "accounting_mode": "explicit_property_cell_support",
        "accepted_decision_count": len(audit),
        "accepted_authority_registry": "reconciliation/accepted-authority-sources.json",
        "decisions": audit,
        "summary": {
            "decision_type_counts": dict(sorted(by_decision_property.items())),
            "previous_implied_declarative_property_cells_by_decision": implied_count,
            "corrected_evidence_supported_property_cells_by_decision": corrected_count,
            "over_promoted_cells_removed_by_decision": implied_count - corrected_count,
            "previous_implied_unique_physical_property_cells": len(old_unique),
            "corrected_unique_physical_property_cells": len(corrected_unique),
            "over_promoted_unique_physical_property_cells_removed": len(old_unique - corrected_unique),
            "tracked_property_cells": list(TRACKED_PROPERTY_CELLS),
        },
        "affected_historical_cohorts": [
            "PIPELINE-4A derived reconciliation infrastructure",
            "PIPELINE-5B/5D and PIPELINE-6/7/8 accepted decisions",
            "PIPELINE-9/9A H123",
        ],
    }


def main() -> None:
    result = build()
    OUTPUT_PATH.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2))


if __name__ == "__main__":
    main()
