"""Claim-driven applicability and evidence accounting for PIPELINE-8."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def load_claims() -> list[dict[str, Any]]:
    return json.loads(
        (ROOT / "sources/claims/generic-claims.json").read_text(encoding="utf-8")
    )["claims"]


def claims_for(
    claims: list[dict[str, Any]], family: str, table: str, address: int
) -> list[dict[str, Any]]:
    return [
        claim
        for claim in claims
        if claim["subject"].get("table") == table
        and claim["subject"].get("address") == address
        and (
            claim["subject"].get("family_scope") == [family]
            or claim["source_id"] == "vendor_growatt_v124_2020"
        )
    ]


def applicability_claims_for(
    claims: list[dict[str, Any]], family: str, table: str, address: int
) -> list[dict[str, Any]]:
    return [
        claim
        for claim in claims
        if claim["assertion"]["kind"] == "document_range_applicability"
        and claim["subject"].get("family_scope") == [family]
        and claim["subject"].get("table") == table
        and claim["subject"].get("address", -1) <= address <= claim["subject"].get("address_end", -1)
    ]


def evidence_dimensions(
    claims: list[dict[str, Any]], family: str, table: str, address: int
) -> dict[str, Any]:
    target = claims_for(claims, family, table, address)
    vendor_rows = [
        claim
        for claim in target
        if claim["source_id"] == "vendor_growatt_v124_2020"
        and claim["assertion"]["kind"] == "vendor_source_row"
    ]
    def ids(items: list[dict[str, Any]]) -> list[str]:
        return sorted({item["claim_id"] for item in items})

    semantic = [
        claim
        for claim in target
        if claim["assertion"]["kind"] in {"vendor_source_row", "register_name", "description"}
        and claim["source_id"] == "vendor_growatt_v124_2020"
    ]
    enum_or_packed = [
        claim
        for claim in target
        if claim["assertion"]["kind"] in {"enum_member", "packed_field"}
        and claim["source_id"] == "vendor_growatt_v124_2020"
    ]
    access = [
        claim
        for claim in target
        if claim["assertion"]["kind"] == "access"
        and claim["source_id"] == "vendor_growatt_v124_2020"
    ]
    qualifiers = [
        claim
        for claim in target
        if claim["assertion"]["kind"] == "row_local_qualifier"
        and claim["source_id"] == "vendor_growatt_v124_2020"
    ]
    independent = [
        claim
        for claim in target
        if claim["source_id"] != "vendor_growatt_v124_2020"
    ]
    applicable = applicability_claims_for(claims, family, table, address)
    has_write = any(
        "R/W" in json.dumps(claim["assertion"].get("value", ""))
        for claim in vendor_rows
    )
    live_write = [
        claim
        for claim in independent
        if "write" in claim["assertion"]["kind"]
        or "write" in claim["scope"].get("applicability", "").lower()
    ]
    unresolved = [
        claim
        for claim in qualifiers
        if any(token in str(claim["assertion"]["value"]).lower() for token in ("used", "only", "special"))
    ]
    return {
        "physical_applicability": {
            "status": "supported" if applicable else "unresolved",
            "claim_ids": ids(applicable),
        },
        "semantic_row": {
            "status": "supported" if semantic else "unresolved",
            "claim_ids": ids(semantic),
        },
        "enum_or_packed_layout": {
            "status": "supported" if enum_or_packed else "not_present",
            "claim_ids": ids(enum_or_packed),
        },
        "access": {
            "status": "supported" if access or has_write else "not_present",
            "claim_ids": ids(access),
        },
        "model_specific_qualifier": {
            "status": "present" if qualifiers else "not_present",
            "claim_ids": ids(qualifiers),
        },
        "independent_corroboration": {
            "status": "present" if independent else "not_present",
            "claim_ids": ids(independent),
        },
        "unresolved_qualifier": {
            "status": "present" if unresolved else "not_present",
            "claim_ids": ids(unresolved),
        },
        "write_documentation": {
            "status": "documented" if has_write else "not_applicable_or_unknown",
            "claim_ids": ids(vendor_rows) if has_write else [],
        },
        "live_write_verification": {
            "status": "verified" if live_write else "absent",
            "claim_ids": ids(live_write),
        },
    }


def score_dimensions(dimensions: dict[str, Any]) -> dict[str, Any]:
    supported = sum(
        dimensions[name]["status"] in {"supported", "present", "documented", "verified"}
        for name in (
            "physical_applicability",
            "semantic_row",
            "enum_or_packed_layout",
            "access",
            "independent_corroboration",
            "write_documentation",
            "live_write_verification",
        )
    )
    unresolved = dimensions["unresolved_qualifier"]["status"] == "present"
    score = supported - int(unresolved)
    quality = "high" if score >= 4 and not (
        dimensions["physical_applicability"]["status"] != "supported"
        or dimensions["semantic_row"]["status"] != "supported"
    ) else "medium" if score >= 2 else "low"
    return {"score": score, "evidence_quality": quality, "unresolved_qualifier": unresolved}


def candidate_evidence(
    claims: list[dict[str, Any]], family: str, table: str, addresses: list[int]
) -> dict[str, Any]:
    per_record = {
        f"{family}:{table}:{address}": evidence_dimensions(claims, family, table, address)
        for address in addresses
    }
    statuses = defaultdict(int)
    for dimensions in per_record.values():
        for name, value in dimensions.items():
            statuses[name] += value["status"] in {"supported", "present", "documented", "verified"}
    aggregate = {
        name: {
            "supported_records": count,
            "record_count": len(addresses),
            "coverage": count / len(addresses) if addresses else 0,
        }
        for name, count in sorted(statuses.items())
    }
    score = sum(score_dimensions(value)["score"] for value in per_record.values())
    quality = (
        "high"
        if all(score_dimensions(value)["evidence_quality"] == "high" for value in per_record.values())
        else "medium"
        if score >= max(1, len(addresses) * 2)
        else "low"
    )
    return {
        "evidence_dimensions": aggregate,
        "per_record": per_record,
        "score": score,
        "evidence_quality": quality,
    }
