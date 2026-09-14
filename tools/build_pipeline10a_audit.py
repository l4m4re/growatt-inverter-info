#!/usr/bin/env python3
"""Audit accepted reconciliation decisions at canonical property-cell level."""

from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
import subprocess
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
HISTORICAL_ACCOUNTING_SHA = "c0ba1dea54fd170e1ecd1b22494b2a84d46b6eee"
HISTORICAL_COVERAGE_PATH = "docs/pipeline/data/GII-PIPELINE-5A_AUTHORITY_COVERAGE.json"
CORRECTED_AUTHORITY_DEFINITION = (
    "Unique canonical property cells backed by accepted reconciliation decisions with "
    "explicit noncanonical property-level claim support; applicability claims establish "
    "scope only, and current PIPELINE-10 decisions are excluded from the accepted registry."
)


def _historical_coverage() -> dict[str, Any]:
    result = subprocess.run(
        ["git", "show", f"{HISTORICAL_ACCOUNTING_SHA}:{HISTORICAL_COVERAGE_PATH}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return json.loads(result.stdout)


def _cell(value: tuple[str, str, int, str]) -> dict[str, Any]:
    family, table, address, property_name = value
    return {
        "canonical_family": family,
        "table": table,
        "address": address,
        "property_name": property_name,
    }


def _cells(values: set[tuple[str, str, int, str]]) -> list[dict[str, Any]]:
    return [_cell(value) for value in sorted(values)]


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
    historical_coverage = _historical_coverage()
    historical_inventory: set[tuple[str, str, int, str]] = set()
    for record in historical_coverage.get("records", []):
        key = (record["family"], record["table"], record["address"])
        historical_inventory.update(
            (*key, property_name) for property_name in record.get("declarative_properties", [])
        )
    historical_nondecision = historical_inventory - old_unique
    historical_broad = old_unique | historical_inventory
    retained = old_unique & corrected_unique
    removed = old_unique - corrected_unique
    newly_supported = corrected_unique - old_unique
    set_bridge = {
        "old_implied_unique": _cells(old_unique),
        "corrected_supported_unique": _cells(corrected_unique),
        "retained": _cells(retained),
        "removed": _cells(removed),
        "newly_supported": _cells(newly_supported),
        "counts": {
            "old_implied_unique": len(old_unique),
            "corrected_supported_unique": len(corrected_unique),
            "retained": len(retained),
            "removed": len(removed),
            "newly_supported": len(newly_supported),
        },
        "relationships": {
            "old_equals_retained_union_removed": old_unique == retained | removed,
            "corrected_equals_retained_union_newly_supported": corrected_unique == retained | newly_supported,
            "retained_disjoint_removed": not retained & removed,
            "retained_disjoint_newly_supported": not retained & newly_supported,
            "removed_disjoint_corrected": not removed & corrected_unique,
            "newly_supported_disjoint_old": not newly_supported & old_unique,
        },
    }
    historical_bridge = {
        "historical_broad_declarative_total": len(historical_broad),
        "historical_decision_implied_unique_cells": len(old_unique),
        "historical_nondecision_declarative_cells": len(historical_nondecision),
        "historical_broad_inventory_unique_cells": len(historical_inventory),
        "historical_inventory_overlap_with_decision_implied": len(historical_inventory & old_unique),
        "historical_nondecision_cells": [
            {
                **_cell(value),
                "category": "historical_p4a_diagnostic_declarative_inventory_not_in_accepted_authority_registry",
                "source": f"{HISTORICAL_COVERAGE_PATH}@{HISTORICAL_ACCOUNTING_SHA}",
                "authority_status": historical_coverage["declarative_coverage"]["status"],
            }
            for value in sorted(historical_nondecision)
        ],
        "relationships": {
            "historical_broad_equals_decision_implied_union_nondecision": historical_broad == old_unique | historical_nondecision,
            "historical_inventory_equals_overlap_union_nondecision": historical_inventory == (historical_inventory & old_unique) | historical_nondecision,
        },
        "formula": "historical_broad = old_decision_implied ∪ historical_nondecision; historical_inventory = overlap_with_old_decision_implied ∪ historical_nondecision",
        "historical_source": f"{HISTORICAL_COVERAGE_PATH}@{HISTORICAL_ACCOUNTING_SHA}",
    }
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
            "retained_unique_physical_property_cells": len(retained),
            "removed_unique_physical_property_cells": len(removed),
            "newly_supported_unique_physical_property_cells": len(newly_supported),
        },
        "historical_accounting_bridge": historical_bridge,
        "property_set_bridge": set_bridge,
        "corrected_authority_definition": CORRECTED_AUTHORITY_DEFINITION,
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
