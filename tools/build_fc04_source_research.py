#!/usr/bin/env python3
"""Build the property-level PIPELINE-5D FC04 source-research artifacts."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "sources/evidence/gii-pipeline-5d-fc04-source-research.json"
INVENTORY_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-5D_FC04_SOURCE_RESEARCH.json"
CLAIMS_PATH = ROOT / "sources/claims/gii-pipeline-5d-fc04.json"
RECONCILIATION_PATH = ROOT / "reconciliation/min_tl_xh_fc04_source_research_20260913.json"
CANONICAL_PATH = ROOT / "spec/growatt-register-spec.json"
CLOSURE_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-5C_FC04_CLOSURE.json"
AUTHORITY_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-5A_AUTHORITY_COVERAGE.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def source_digest(artifact: str, known: str) -> str:
    path = ROOT / artifact
    return digest(path) if path.is_file() else known


def resolved_scope(candidate: dict[str, Any]) -> str:
    statuses = {item["status"] for item in candidate["properties"].values()}
    if "UNRESOLVED" in statuses:
        return "PARTIALLY_RESOLVED"
    return "FULLY_RESOLVED_AT_PROTOCOL_ROLE_SCOPE"


def authority_metrics(candidates: list[dict[str, Any]]) -> dict[str, Any]:
    authority = load(AUTHORITY_PATH)
    addresses = {item["address"] for item in candidates}
    records = [
        item
        for item in authority["records"]
        if item["family"] == "min_tl_xh" and item["table"] == "input" and 3000 <= item["address"] <= 3249
    ]
    candidate_records = [item for item in records if item["address"] in addresses]
    source_property_map = {
        "physical_layout": "physical_identity",
        "word_length": "length_words",
        "semantic_quantity": "physical_quantity",
        "scale": "scale",
        "unit": "unit",
        "signedness": "signedness",
        "enum": "enum_definitions",
        "packed_field_structure": "packed_layout",
        "applicability": "model_applicability",
    }
    source_supported: Counter[str] = Counter()
    for candidate in candidates:
        for property_name, finding in candidate["properties"].items():
            if finding["status"] == "SUPPORTED":
                mapped = source_property_map.get(property_name)
                if mapped:
                    source_supported[mapped] += 1
    return {
        "authority_tool": "tools/build_authority_coverage.py",
        "before_after_5a_snapshot": {
            "cohort_declarative_authoritative_property_cells": sum(len(item["declarative_properties"]) for item in candidate_records),
            "cohort_legacy_authoritative_dependency_cells": sum(len(item["legacy_dependencies"]) for item in candidate_records),
            "repository_declarative_authoritative_property_cells": authority["authority_origin_metrics"]["canonical_property_cells"] - authority["authority_origin_metrics"]["legacy_authoritative_property_cells"],
            "repository_legacy_authoritative_property_cells": authority["authority_origin_metrics"]["legacy_authoritative_property_cells"],
            "repository_canonical_property_cells": authority["authority_origin_metrics"]["canonical_property_cells"],
            "canonical_unchanged_so_5a_metrics_after": "identical_to_before",
        },
        "five_d_source_supported_property_claims_not_yet_cutover_authority": dict(sorted(source_supported.items())),
        "note": "5D adds property-level declarative evidence and reconciliation, but canonical generator authority is intentionally frozen; the existing 5A authority report therefore remains numerically unchanged.",
    }


def build() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    evidence = load(INPUT_PATH)
    closure = load(CLOSURE_PATH)
    source_records = []
    for source in evidence["sources"]:
        item = dict(source)
        item["sha256"] = source_digest(item["artifact"], item["sha256"])
        source_records.append(item)

    candidates = sorted(evidence["candidate_findings"], key=lambda item: item["address"])
    property_counts: Counter[str] = Counter()
    status_counts: Counter[str] = Counter()
    claims: list[dict[str, Any]] = []
    decisions: list[dict[str, Any]] = []
    for candidate in candidates:
        address = candidate["address"]
        overall = resolved_scope(candidate)
        status_counts[overall] += 1
        for property_name, finding in candidate["properties"].items():
            property_counts[f"{property_name}:{finding['status']}"] += 1
            claim_id = f"gii_5d_source_review:input:{address}:{property_name}"
            claims.append(
                {
                    "claim_id": claim_id,
                    "source_id": "gii_5d_source_review",
                    "source_type": "SOURCE_RESEARCH_REVIEW",
                    "subject": {
                        "namespace": "MODBUS",
                        "family_scope": ["min_tl_xh"],
                        "table": "input",
                        "address": address,
                    },
                    "assertion": {
                        "kind": "property_support" if finding["status"] == "SUPPORTED" else "property_review",
                        "value": {
                            "property": property_name,
                            "status": finding["status"],
                            "value": finding["value"],
                            "evidence_refs": finding["evidence"],
                            "contradictions": candidate["contradictions"],
                        },
                    },
                    "provenance": {
                        "source_artifact": "sources/evidence/gii-pipeline-5d-fc04-source-research.json",
                        "source_sha256": digest(INPUT_PATH),
                        "source_property_evidence": finding["evidence"],
                    },
                    "scope": {
                        "family": ["min_tl_xh"],
                        "model": "MIN/TL-XH",
                        "protocol_revision": "V1.24",
                        "applicability": "5D source-research review of FC04 input cohort",
                    },
                    "evidence": {
                        "method": "property_level_source_review",
                        "confidence": "high" if finding["status"] in {"SUPPORTED", "NOT_APPLICABLE"} else "bounded",
                        "status": finding["status"].lower(),
                        "grade": ["S2"] if finding["status"] == "SUPPORTED" else ["S2", "E1"],
                    },
                }
            )
            decisions.append(
                {
                    "decision_id": f"min-xh-fc04-source-research:{address}:{property_name}",
                    "target": {
                        "canonical_family": "min_tl_xh",
                        "namespace": "MODBUS",
                        "table": "input",
                        "address": address,
                        "property": property_name,
                    },
                    "scope": {
                        "family": "min_tl_xh",
                        "model": "MIN/TL-XH",
                        "protocol_revision": "V1.24",
                        "applicability": "FC04 input source-research cohort",
                    },
                    "decision": {
                        "status": finding["status"].lower(),
                        "confidence": "high" if finding["status"] in {"SUPPORTED", "NOT_APPLICABLE"} else "bounded",
                        "value": finding["value"],
                        "support_claim": claim_id,
                    },
                    "support": claim_id,
                    "conflicts": candidate["contradictions"],
                }
            )

    inventory = {
        "schema_version": "1.0.0",
        "artifact": "growatt_fc04_source_research_inventory",
        "pipeline": "GII-PIPELINE-5D",
        "canonical_modified": False,
        "cohort": evidence["scope"],
        "source_inputs": {
            "pipeline_5c": digest(CLOSURE_PATH),
            "canonical_parity_target": digest(CANONICAL_PATH),
            "source_research_input": digest(INPUT_PATH),
        },
        "candidate_count": len(candidates),
        "resolution_counts": dict(status_counts),
        "property_status_counts": dict(sorted(property_counts.items())),
        "candidate_findings": candidates,
        "derived_aggregate_follow_up": evidence["derived_aggregate_follow_up"],
        "scope_boundaries": evidence["out_of_scope"],
        "authority_metrics": authority_metrics(candidates),
        "safety": {
            "canonical_modified": False,
            "live_experiment": False,
            "inverter_writes": False,
            "runtime_or_ha_changes": False,
        },
    }
    claims_document = {
        "schema_version": "1.0.0",
        "artifact": "growatt_generic_source_claims",
        "generated_by": "tools/build_fc04_source_research.py",
        "sources": [
            {
                "source_id": "gii_5d_source_review",
                "source_type": "SOURCE_RESEARCH_REVIEW",
                "artifact": "sources/evidence/gii-pipeline-5d-fc04-source-research.json",
                "sha256": digest(INPUT_PATH),
            },
            *[
                {
                    "source_id": source["source_id"],
                    "source_type": source["source_type"],
                    "artifact": source["artifact"],
                    "sha256": source["sha256"],
                }
                for source in source_records
            ],
        ],
        "source_type_vocabulary": ["SOURCE_RESEARCH_REVIEW", "VENDOR_DOCUMENT_CLAIM", "EXTERNAL_IMPLEMENTATION_CLAIM", "HUMAN_REVIEW_CLAIM", "LIVE_MODBUS_OBSERVATION", "GROWATT_CLOUD_API_OBSERVATION"],
        "claims": claims,
    }
    reconciliation = {
        "schema_version": "1.0.0",
        "artifact": "growatt_reconciliation_decisions",
        "migration": "GII-PIPELINE-5D",
        "canonical_modified": False,
        "canonical_input_sha256": digest(CANONICAL_PATH),
        "cohort": evidence["scope"],
        "source_research_input_sha256": digest(INPUT_PATH),
        "decisions": decisions,
        "derived_aggregate_follow_up": evidence["derived_aggregate_follow_up"],
    }
    if len(closure["targets"]) != 129:
        raise ValueError("PIPELINE-5C input no longer contains its expected 129 targets")
    return inventory, claims_document, reconciliation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    paths = (INVENTORY_PATH, CLAIMS_PATH, RECONCILIATION_PATH)
    if args.check:
        errors = [
            f"stale or missing artifact: {path}"
            for path, data in zip(paths, expected)
            if not path.is_file() or load(path) != data
        ]
        if errors:
            print("\n".join(errors))
            raise SystemExit(1)
        print("valid: PIPELINE-5D source-research artifacts are deterministic")
        return
    for path, data in zip(paths, expected):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"candidates": len(expected[0]["candidate_findings"]), "resolution_counts": expected[0]["resolution_counts"]}, indent=2))


if __name__ == "__main__":
    main()
