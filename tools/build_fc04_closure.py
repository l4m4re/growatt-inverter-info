#!/usr/bin/env python3
"""Classify the remaining bounded PIPELINE-5B FC04 semantic targets.

This is an evidence inventory, not a live experiment runner. It reuses the
sanitized 5B oracle and source claims and keeps the canonical output frozen.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

try:
    from tools.build_fc04_migration import (
        CANONICAL_PATH,
        CLAIMS_PATH,
        CURATED_PATH,
        END,
        FAMILY,
        ORACLE_PATH,
        SHADOW_PATH,
        START,
        VENDOR_PATH,
        curated_rows,
        digest,
        load,
        vendor_rows,
    )
except ModuleNotFoundError:
    from build_fc04_migration import (
        CANONICAL_PATH,
        CLAIMS_PATH,
        CURATED_PATH,
        END,
        FAMILY,
        ORACLE_PATH,
        SHADOW_PATH,
        START,
        VENDOR_PATH,
        curated_rows,
        digest,
        load,
        vendor_rows,
    )

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-5C_FC04_CLOSURE.json"
RECONCILIATION_PATH = ROOT / "reconciliation/min_tl_xh_fc04_closure_20260913.json"

API_INVENTORY = {
    "source": "existing sanitized GII-MIN-RE-4 evidence",
    "read_only": True,
    "surfaces": [
        {"group": "inverter", "fields": ["status", "status_text", "operating_mode", "real_op_percent"]},
        {"group": "bdc", "fields": ["bdc1_status", "bdc1_mode", "bdc1_ibat", "bdc1_vbat", "bdc1_charge_power", "bdc1_discharge_power", "bdc_derate_reason"]},
        {"group": "bms", "fields": ["bms_status", "bms_ibat", "bms_vbat", "bms_soc", "bms_soh", "bms_error", "bms_warning"]},
        {"group": "status_words", "fields": ["warn_code", "new_warn_code", "fault_type", "sys_fault_word", "sys_fault_word2", "sys_fault_word3", "sys_fault_word4", "sys_fault_word5", "sys_fault_word6", "sys_fault_word7", "warn_text"]},
        {"group": "grid_load_energy", "fields": ["pac", "p_system", "pac_to_local_load", "grid_import", "grid_export", "pv_total", "charge_energy", "discharge_energy"]},
        {"group": "winter_mode", "fields": ["win_mode", "win_request", "win_on_grid_soc", "win_off_grid_soc", "win_start", "win_end"]},
    ],
    "field_to_register_is_not_assumed": True,
}


def canonical_records() -> dict[int, dict[str, Any]]:
    return {
        record["address"]: record
        for record in load(CANONICAL_PATH)["registers"]
        if record.get("family") == FAMILY and record.get("table") == "input" and START <= record.get("address", -1) <= END
    }


def source_for(address: int) -> tuple[dict[str, Any] | None, str | None]:
    for item in curated_rows():
        if item["start"] <= address <= item["end"]:
            row = item["row"]
            return row, f"curated_fc04_semantics:input:{item['start']}-{item['end']}:{item['occurrence']}"
    return None, None


def vendor_claim_id(address: int) -> str | None:
    for item in vendor_rows():
        if item["address"] == address:
            return f"vendor_v124_fc04:input:{address}:{item['occurrence']}"
    return None


def oracle_claims(address: int) -> list[str]:
    result = []
    claims = load(CLAIMS_PATH)["claims"]
    for item in claims:
        if item["source_id"] in {"min_cloud_oracle", "min_shine_injection"} and item["subject"].get("address") == address:
            result.append(item["claim_id"])
    return result


def classify(address: int, record: dict[str, Any], source: dict[str, Any] | None) -> tuple[str, str, dict[str, Any]]:
    name = (source or {}).get("name", "")
    data_type = (source or {}).get("data_type", "") or ""
    canonical_name = record.get("normalized", {}).get("name") or ""
    quantity = record.get("semantic_identity", {}).get("quantity")
    text = f"{name} {canonical_name} {data_type}".lower()
    def dimensions(physical: str, numeric: str, semantic: str, applicability: str) -> dict[str, str]:
        scale = "source_declared" if source and source.get("data_type") else "unknown"
        signedness = "source_declared" if re.search(r"(^|_)s(?:16|32|64)", data_type) else "unknown"
        unit = "source_declared" if source and source.get("unit") is not None else "not_applicable_or_unknown"
        enum = "source_declared" if "enum" in data_type or "status" in text or "flag" in text else "not_applicable_or_unknown"
        return {"physical": physical, "scale": scale, "signedness": signedness, "unit": unit, "numeric": numeric, "semantic": semantic, "enum": enum, "applicability": applicability}
    if address in {3110, 3111, 3165, 3166, 3211, 3212}:
        return "EXISTING_EVIDENCE_SUFFICIENT", "Existing Cloud/Shine oracle evidence is already claim-backed; no repeat injection is justified.", dimensions("resolved", "source_oracle_bounded", "source_oracle_bounded", "family-scoped")
    if any(token in text for token in ("serial", "firmware", "software version", "device type", "model")):
        return "IDENTITY_OR_STATIC_METADATA", "Identity/static metadata must not be actively manipulated; retain source mapping only.", dimensions("resolved", "not_applicable", "static_source", "source-dependent")
    if any(token in text for token in ("energy", "runtime", "total", "today", "cumulative")):
        return "COUNTER_AVOID_ACTIVE_INJECTION", "Counter or cumulative semantics can be sourced/passively correlated; fake cloud values would pollute history.", dimensions("resolved", "source_declared", "counter_source_only", "family-scoped")
    if any(token in text for token in ("debug", "fft", "fault", "warning", "derating", "protect", "afci", "residual", "insulation")):
        return "OPAQUE_DIAGNOSTIC", "Diagnostic word exists, but no safe complete enum/bit meaning or useful cloud surface is retained.", dimensions("resolved", "raw_word_or_source_declared", "opaque", "family-scoped")
    if any(token in text for token in ("total", "system", "home load", "self-use", "aggregate", "power")) and ("energy" in text or "total" in text or "load" in text):
        return "DERIVED_OR_AGGREGATE", "Cloud/API may calculate or aggregate this field; a one-register causal claim must not be assumed.", dimensions("candidate", "source_declared", "derived_or_aggregate_candidate", "family-scoped")
    if not source or not source.get("name"):
        return "SOURCE_RESEARCH_CANDIDATE", "The vendor row or source name is incomplete; source/layout research is higher value than blind cloud injection.", dimensions("source_row_only", "unknown", "unknown", "unknown")
    return "INSUFFICIENT_EVIDENCE", "The source gives a label/encoding candidate, but retained evidence does not prove the exact semantic relationship needed for closure.", dimensions("resolved", "source_declared", "unresolved", "family-scoped")


def build() -> tuple[dict[str, Any], dict[str, Any]]:
    shadow = load(SHADOW_PATH)
    canonical = canonical_records()
    unresolved = [item["address"] for item in shadow["parity"]["classifications"] if item["classification"] == "UNRESOLVED"]
    targets = []
    decisions = []
    for address in unresolved:
        source, source_claim = source_for(address)
        category, rationale, dimensions = classify(address, canonical[address], source)
        supports = [claim_id for claim_id in (vendor_claim_id(address), source_claim) if claim_id]
        supports.extend(oracle_claims(address))
        target = {
            "address": address,
            "physical_id": f"{FAMILY}:input:{address}",
            "classification": category,
            "rationale": rationale,
            "dimensions": dimensions,
            "source_claims": supports,
            "experiment": {"eligible": category in {"PASSIVE_CLOUD_CANDIDATE", "ACTIVE_CLOUD_ORACLE_CANDIDATE"}, "performed": False},
        }
        targets.append(target)
        decisions.append({
            "decision_id": f"min-xh-fc04-closure:{address}",
            "target": {"canonical_family": FAMILY, "namespace": "MODBUS", "table": "input", "address": address, "property": "semantic_closure_status"},
            "scope": {"family": FAMILY, "model": "MIN/TL-XH", "protocol_revision": "V1.24", "applicability": "5C bounded unresolved-target classification"},
            "decision": {"status": "classified", "confidence": "high" if category != "INSUFFICIENT_EVIDENCE" else "medium", "value": target},
            "support": supports,
            "conflicts": [],
            "rationale": rationale,
            "review": {
                "status": "accepted_inventory_classification",
                "notes": "PIPELINE-5C bounded closure classification; canonical output remains unchanged.",
                "reviewed_at": "2026-09-13",
            },
        })
    result = {
        "schema_version": "1.0.0",
        "artifact": "growatt_fc04_semantic_closure_inventory",
        "canonical_modified": False,
        "cohort": {"family": FAMILY, "table": "input", "start": START, "end": END, "function_code": 4},
        "source_inputs": {"claims": digest(CLAIMS_PATH), "vendor": digest(VENDOR_PATH), "curated": digest(CURATED_PATH), "oracle": digest(ORACLE_PATH), "canonical_parity_target": digest(CANONICAL_PATH)},
        "original_unresolved_count": len(unresolved),
        "targets": targets,
        "api_inventory": API_INVENTORY,
        "timing": {
            "source": "existing GII-MIN-RE-4 bounded run",
            "shine_cloud_regime": "approximately 5 minutes per publication",
            "propagation": "assessed only after a held marker crossed a publication boundary",
            "new_measurement_in_5c": False,
            "reason": "existing retained timing evidence was sufficient and no new injection was required",
        },
        "active_experiments": [],
        "safety": {"shine_bound_only": True, "local_ground_truth_modified": False, "intentional_inverter_writes": False, "counters_injected": False, "identity_injected": False},
    }
    reconciliation = {
        "schema_version": "1.0.0",
        "artifact": "growatt_reconciliation_decisions",
        "migration": "GII-PIPELINE-5C",
        "canonical_modified": False,
        "cohort": result["cohort"],
        "decisions": decisions,
    }
    return result, reconciliation


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build()
    paths = (OUTPUT_PATH, RECONCILIATION_PATH)
    if args.check:
        errors = [f"stale or missing artifact: {path}" for path, data in zip(paths, expected) if not path.is_file() or load(path) != data]
        if errors:
            print("\n".join(errors))
            raise SystemExit(1)
        print("valid: FC04 closure inventory and reconciliation are deterministic")
        return
    for path, data in zip(paths, expected):
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    from collections import Counter
    print(json.dumps({"targets": len(expected[0]["targets"]), "by_classification": Counter(item["classification"] for item in expected[0]["targets"])}, indent=2))


if __name__ == "__main__":
    main()
