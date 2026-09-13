#!/usr/bin/env python3
"""Build and validate the bounded MIN/TL-XH FC04 authority migration.

The generated claim and reconciliation files are deliberately a shadow layer.
They do not feed the canonical generator until a later reviewed cutover.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VENDOR_PATH = ROOT / "sources/vendor/growatt-v1.24-tables.json"
CURATED_PATH = ROOT / "sources/curated/growatt-registers-best-guess.json"
LIVE_PATH = ROOT / "sources/evidence/min-6000tl-xh-live-validation.json"
ORACLE_PATH = ROOT / "sources/evidence/min-6000tl-xh-cloud-oracle-validation.json"
CANONICAL_PATH = ROOT / "spec/growatt-register-spec.json"
CLAIMS_PATH = ROOT / "sources/claims/gii-pipeline-5b-fc04.json"
RECONCILIATION_PATH = ROOT / "reconciliation/min_tl_xh_fc04_3000_3249.json"
SHADOW_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-5B_FC04_SHADOW.json"

FAMILY = "min_tl_xh"
START = 3000
END = 3249


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def exact_register(value: Any) -> int | None:
    match = re.fullmatch(r"\s*(\d+)\s*", str(value))
    return int(match.group(1)) if match else None


def slug(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return value or "unnamed"


def vendor_rows() -> list[dict[str, Any]]:
    result = []
    for occurrence, row in enumerate(load(VENDOR_PATH)["input"]):
        address = exact_register(row.get("register"))
        if address is None or not START <= address <= END:
            continue
        result.append({"address": address, "occurrence": occurrence, "row": row})
    return result


def curated_rows() -> list[dict[str, Any]]:
    result = []
    for occurrence, row in enumerate(load(CURATED_PATH)["input"]):
        start = row.get("register_start", row.get("register"))
        end = row.get("register_end", start)
        if not isinstance(start, int) or not isinstance(end, int):
            continue
        if end < START or start > END:
            continue
        start = max(start, START)
        end = min(end, END)
        result.append({"start": start, "end": end, "occurrence": occurrence, "row": row})
    return result


def canonical_records() -> dict[int, dict[str, Any]]:
    return {
        record["address"]: record
        for record in load(CANONICAL_PATH)["registers"]
        if record.get("family") == FAMILY
        and record.get("table") == "input"
        and START <= record.get("address", -1) <= END
    }


def claim(
    claim_id: str,
    source_id: str,
    source_type: str,
    subject: dict[str, Any],
    assertion: dict[str, Any],
    provenance: dict[str, Any],
    applicability: str,
    method: str,
    confidence: str,
    status: str,
    grades: list[str],
) -> dict[str, Any]:
    return {
        "claim_id": claim_id,
        "source_id": source_id,
        "source_type": source_type,
        "subject": subject,
        "assertion": assertion,
        "provenance": provenance,
        "scope": {
            "family": [FAMILY],
            "model": "MIN/TL-XH",
            "protocol_revision": "V1.24",
            "applicability": applicability,
        },
        "evidence": {
            "method": method,
            "confidence": confidence,
            "status": status,
            "grade": grades,
        },
    }


def build_claims() -> dict[str, Any]:
    claims: list[dict[str, Any]] = []
    vendor_hash = digest(VENDOR_PATH)
    for item in vendor_rows():
        row = item["row"]
        address = item["address"]
        claims.append(
            claim(
                f"vendor_v124_fc04:input:{address}:{item['occurrence']}",
                "vendor_v124_fc04",
                "VENDOR_DOCUMENT_CLAIM",
                {"namespace": "MODBUS", "family_scope": [FAMILY], "table": "input", "address": address},
                {
                    "kind": "vendor_source_row",
                    "value": {
                        "variable": row.get("variable", ""),
                        "description": row.get("description", ""),
                        "datatype": row.get("value", ""),
                        "unit": row.get("unit", ""),
                        "access": row.get("write_or_not", ""),
                    },
                    "source_text": " ".join(str(row.get(key, "")).strip() for key in ("variable", "description", "value", "unit")),
                },
                {
                    "source_artifact": "sources/vendor/growatt-v1.24-tables.json",
                    "document_sha256": vendor_hash,
                    "page": row.get("page"),
                    "source_row": str(item["occurrence"]),
                    "json_pointer": f"/input/{item['occurrence']}",
                },
                "V1.24 input table row",
                "native_pdf_table_transcription",
                "high",
                "source_row",
                ["S2"],
            )
        )

    curated_hash = digest(CURATED_PATH)
    for item in curated_rows():
        row = item["row"]
        start, end = item["start"], item["end"]
        claims.append(
            claim(
                f"curated_fc04_semantics:input:{start}-{end}:{item['occurrence']}",
                "curated_fc04_semantics",
                "HUMAN_REVIEW_CLAIM",
                {
                    "namespace": "MODBUS",
                    "family_scope": [FAMILY],
                    "table": "input",
                    "address": start,
                    **({"address_end": end} if end != start else {}),
                },
                {
                    "kind": "reviewed_semantic_mapping",
                    "value": {
                        "canonical_name": row.get("name", ""),
                        "description": row.get("description", ""),
                        "data_type": row.get("data_type"),
                        "unit": row.get("unit"),
                        "access": row.get("access"),
                        "aliases": row.get("attributes", []),
                        "semantic_key": f"semantic.{slug(row.get('name', 'unnamed'))}",
                    },
                    "source_text": row.get("description", ""),
                },
                {
                    "source_artifact": "sources/curated/growatt-registers-best-guess.json",
                    "document_sha256": curated_hash,
                    "source_row": str(item["occurrence"]),
                    "json_pointer": f"/input/{item['occurrence']}",
                },
                "bounded FC04 cohort semantic source",
                "curated_source_review",
                "medium",
                "reviewed_source_mapping",
                ["S2"],
            )
        )

    live_hash = digest(LIVE_PATH)
    live = load(LIVE_PATH)
    for index, sample in enumerate(live.get("telemetry_samples", [])):
        blocks = [key for key in sample if key.startswith("fc04_")]
        for block in blocks:
            match = re.fullmatch(r"fc04_(\d+)_count(\d+)_registers", block)
            if not match:
                continue
            start, count = int(match.group(1)), int(match.group(2))
            end = start + count - 1
            if end < START or start > END:
                continue
            claims.append(
                claim(
                    f"min_live_fc04:sample:{index}:{block}",
                    "min_live_fc04",
                    "LIVE_MODBUS_OBSERVATION",
                    {"namespace": "MODBUS", "family_scope": [FAMILY], "table": "input", "address": start, "address_end": end},
                    {"kind": "read_observation", "value": {"block": block, "word_count": count, "captured_at_range": sample.get("captured_at_range")}},
                    {"source_artifact": "sources/evidence/min-6000tl-xh-live-validation.json", "document_sha256": live_hash, "json_pointer": f"/telemetry_samples/{index}"},
                    "bounded live FC04 read-only observation",
                    "read_only_capture",
                    "medium",
                    "observed_response",
                    ["P2"],
                )
            )

    oracle_hash = digest(ORACLE_PATH)
    for index, record in enumerate(load(ORACLE_PATH)["records"]):
        address = record["address"]
        mapping_id = f"min_shine_injection:input:{address}:{index}:physical"
        mapping_grade = ["P1"] if record["confidence"] == "high" and record["result"] in {"confirmed_cloud_field_correlation", "runtime_cloud_consistency"} else ["C"]
        claims.append(
            claim(
                mapping_id,
                "min_shine_injection",
                "SHINE_BOUND_INJECTION_OBSERVATION",
                {"namespace": "MODBUS", "family_scope": [FAMILY], "table": "input", "address": address},
                {
                    "kind": "physical_cloud_mapping",
                    "value": {"cloud_fields": record.get("cloud_fields", {}), "injected_value": record.get("injected_value"), "result": record.get("result")},
                    "raw_value": record.get("injected_value"),
                    "observation": {"active_interval_utc": record.get("active_interval_utc"), "valid_rewrites": record.get("valid_rewrites")},
                },
                {"source_artifact": "sources/evidence/min-6000tl-xh-cloud-oracle-validation.json", "document_sha256": oracle_hash, "record_id": str(index), "json_pointer": f"/records/{index}"},
                "Shine-bound response copy only; inverter response and HA/GII view unchanged",
                "controlled_response_injection",
                record["confidence"],
                record["result"],
                mapping_grade,
            )
        )
        for field, value in record.get("cloud_fields", {}).items():
            claims.append(
                claim(
                    f"min_cloud_oracle:input:{address}:{index}:{field}",
                    "min_cloud_oracle",
                    "GROWATT_CLOUD_API_OBSERVATION",
                    {"namespace": "MODBUS", "family_scope": [FAMILY], "table": "input", "address": address},
                    {
                        "kind": "cloud_field_observation",
                        "value": {"field": field, "value": value, "publication_timestamp_utc": record.get("cloud_publication_timestamp_utc")},
                        "raw_value": value,
                        "observation": {"result": record.get("result"), "note": record.get("note")},
                    },
                    {"source_artifact": "sources/evidence/min-6000tl-xh-cloud-oracle-validation.json", "document_sha256": oracle_hash, "record_id": str(index), "json_pointer": f"/records/{index}"},
                    "Growatt cloud/API observation after Shine publication interval",
                    "cloud_history_correlation",
                    record["confidence"],
                    record["result"],
                    ["S1"] if record["confidence"] == "high" else ["C"],
                )
            )

    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_generic_source_claims",
        "generated_by": "tools/build_fc04_migration.py",
        "sources": [
            {"source_id": "vendor_v124_fc04", "source_type": "VENDOR_DOCUMENT_CLAIM", "artifact": str(VENDOR_PATH.relative_to(ROOT)), "sha256": vendor_hash},
            {"source_id": "curated_fc04_semantics", "source_type": "HUMAN_REVIEW_CLAIM", "artifact": str(CURATED_PATH.relative_to(ROOT)), "sha256": curated_hash},
            {"source_id": "min_live_fc04", "source_type": "LIVE_MODBUS_OBSERVATION", "artifact": str(LIVE_PATH.relative_to(ROOT)), "sha256": live_hash},
            {"source_id": "min_shine_injection", "source_type": "SHINE_BOUND_INJECTION_OBSERVATION", "artifact": str(ORACLE_PATH.relative_to(ROOT)), "sha256": oracle_hash},
            {"source_id": "min_cloud_oracle", "source_type": "GROWATT_CLOUD_API_OBSERVATION", "artifact": str(ORACLE_PATH.relative_to(ROOT)), "sha256": oracle_hash},
        ],
        "source_type_vocabulary": [
            "GROWATT_CLOUD_API_OBSERVATION",
            "STOCK_SHINE_OBSERVATION",
            "SHINE_BOUND_INJECTION_OBSERVATION",
            "LIVE_MODBUS_OBSERVATION",
            "VENDOR_DOCUMENT_CLAIM",
            "EXTERNAL_IMPLEMENTATION_CLAIM",
            "RUNTIME_IMPLEMENTATION_CLAIM",
            "HUMAN_REVIEW_CLAIM",
        ],
        "claims": claims,
    }


def build_reconciliation(claims: dict[str, Any]) -> dict[str, Any]:
    by_address: dict[int, list[str]] = {}
    for item in vendor_rows():
        by_address.setdefault(item["address"], []).append(f"vendor_v124_fc04:input:{item['address']}:{item['occurrence']}")
    curated = curated_rows()
    logical_for_address: dict[int, dict[str, Any]] = {}
    decisions: list[dict[str, Any]] = []
    for item in curated:
        row = item["row"]
        start, end = item["start"], item["end"]
        decision_id = f"min-xh-fc04-semantic:{start}-{end}"
        logical = {
            "support_claim": f"curated_fc04_semantics:input:{start}-{end}:{item['occurrence']}",
            "logical_object": decision_id,
            "semantic_key": f"semantic.{slug(row.get('name', 'unnamed'))}",
            "canonical_name": row.get("name", ""),
            "description": row.get("description", ""),
            "data_type": row.get("data_type"),
            "unit": row.get("unit"),
            "access": row.get("access"),
            "aliases": row.get("attributes", []),
            "physical_span": {"table": "input", "address": start, "address_end": end},
            "authority_status": "resolved_from_claims",
        }
        support = [f"curated_fc04_semantics:input:{start}-{end}:{item['occurrence']}"]
        for address in range(start, end + 1):
            logical_for_address[address] = {"decision_id": decision_id, "logical": logical}
        decisions.append({
            "decision_id": decision_id,
            "target": {"canonical_family": FAMILY, "namespace": "LOGICAL", "logical_object": decision_id, "property": "semantic_mapping"},
            "scope": {"family": FAMILY, "model": "MIN/TL-XH", "protocol_revision": "V1.24", "applicability": "FC04 input cohort reviewed source entry"},
            "decision": {"status": "resolved", "confidence": "medium", "value": logical},
            "support": support,
            "conflicts": [],
            "rationale": "The logical mapping is sourced from a bounded reviewed data record; the source variable and physical register remain separately claim-addressable.",
            "review": {
                "status": "accepted_source_review",
                "notes": "PIPELINE-5B bounded FC04 migration decision; canonical output remains unchanged.",
                "reviewed_at": "2026-09-13",
            },
        })

    for address in range(START, END + 1):
        vendor_support = by_address.get(address, [])
        logical = logical_for_address.get(address)
        support = vendor_support[:]
        if logical:
            support.append(next(iter(logical["logical"].get("support", [])), logical["decision_id"]))
        value: dict[str, Any] = {
            "table": "input",
            "address": address,
            "length_words": 1,
            "access": "R",
            "applicability": "MIN/TL-XH FC04 input page 3000-3249",
            "source_aliases": sorted({str(item["row"].get("variable", "")).strip() for item in vendor_rows() if item["address"] == address and str(item["row"].get("variable", "")).strip()}),
        }
        if logical:
            value["logical_object"] = logical["decision_id"]
            value["support_claim"] = logical["logical"]["support_claim"]
            value["component_role"] = "logical_span_member"
        decisions.append({
            "decision_id": f"min-xh-fc04-physical:{address}",
            "target": {"canonical_family": FAMILY, "namespace": "MODBUS", "table": "input", "address": address, "property": "physical_mapping"},
            "scope": {"family": FAMILY, "model": "MIN/TL-XH", "protocol_revision": "V1.24", "applicability": "FC04 input cohort"},
            "decision": {"status": "resolved" if vendor_support else "unresolved", "confidence": "high" if vendor_support else "unknown", "value": value},
            "support": support,
            "conflicts": [],
            "rationale": "Physical identity is the FC04 table/address; one-word bus identity is distinct from any multiword logical quantity.",
            "review": {
                "status": "accepted_source_review",
                "notes": "PIPELINE-5B bounded FC04 migration decision; canonical output remains unchanged.",
                "reviewed_at": "2026-09-13",
            },
        })

    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_reconciliation_decisions",
        "migration": "GII-PIPELINE-5B",
        "canonical_input": "spec/growatt-register-spec.json",
        "canonical_modified": False,
        "cohort": {"family": FAMILY, "table": "input", "start": START, "end": END, "function_code": 4},
        "evidence_grade_vocabulary": {"P1": "controlled physical mapping", "P2": "strong passive physical correlation", "S1": "Growatt semantic/API observation", "S2": "vendor semantic interpretation", "C": "candidate/correlation only", "X": "contradicted"},
        "decisions": decisions,
    }


def build_shadow(reconciliation: dict[str, Any]) -> dict[str, Any]:
    canonical = canonical_records()
    curated = curated_rows()
    logical = {item["start"]: item for item in curated}
    physical = [item for item in reconciliation["decisions"] if item["target"]["namespace"] == "MODBUS"]
    parity = {"physical_identity": 0, "source_shape": 0, "semantic_name_exact": 0, "unresolved_semantic_differences": 0, "classifications": []}
    for item in physical:
        address = item["target"]["address"]
        candidate = item["decision"]["value"]
        current = canonical[address]
        parity["physical_identity"] += int(current["table"] == candidate["table"] and current["address"] == candidate["address"])
        parity["source_shape"] += 1
        entry = logical.get(address)
        if entry:
            name = entry["row"].get("name", "")
            if name == current.get("normalized", {}).get("name"):
                parity["semantic_name_exact"] += 1
                classification = "EXPECTED_REPRESENTATION_ONLY"
            else:
                classification = "UNRESOLVED"
        else:
            classification = "UNRESOLVED"
        parity["classifications"].append({"address": address, "classification": classification})
        if classification == "UNRESOLVED":
            parity["unresolved_semantic_differences"] += 1
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_fc04_declarative_shadow",
        "canonical_modified": False,
        "cohort": {"family": FAMILY, "table": "input", "start": START, "end": END, "function_code": 4},
        "candidate": {"source": "reconciliation/min_tl_xh_fc04_3000_3249.json", "physical_records": len(physical), "logical_decisions": len(curated), "canonical_output_not_replaced": True},
        "canonical_parity_target_sha256": digest(CANONICAL_PATH),
        "parity": parity,
    }


def build_all() -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    claims = build_claims()
    reconciliation = build_reconciliation(claims)
    return claims, reconciliation, build_shadow(reconciliation)


def write(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    expected = build_all()
    paths = (CLAIMS_PATH, RECONCILIATION_PATH, SHADOW_PATH)
    if args.check:
        errors = []
        for path, data in zip(paths, expected):
            if not path.is_file() or load(path) != data:
                errors.append(f"stale or missing artifact: {path}")
        if errors:
            print("\n".join(errors))
            raise SystemExit(1)
        print("valid: FC04 migration artifacts are deterministic")
        return
    for path, data in zip(paths, expected):
        write(path, data)
    print(json.dumps({"claims": len(expected[0]["claims"]), "decisions": len(expected[1]["decisions"]), "physical_records": expected[2]["candidate"]["physical_records"], "logical_decisions": expected[2]["candidate"]["logical_decisions"]}, indent=2))


if __name__ == "__main__":
    main()
