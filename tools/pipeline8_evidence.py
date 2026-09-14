"""Claim-driven applicability and evidence accounting for PIPELINE-8."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
_APPLICABILITY_INDEX: tuple[object, dict[tuple[str, str], list[dict[str, Any]]]] | None = None
_CLAIM_INDEX: tuple[object, dict[tuple[str, int], list[dict[str, Any]]]] | None = None

SUPPORTED_UNCONDITIONAL = "SUPPORTED_UNCONDITIONAL"
SUPPORTED_QUALIFIED = "SUPPORTED_QUALIFIED"
NOT_SUPPORTED_BY_DECLARATION = "NOT_SUPPORTED_BY_DECLARATION"
UNRESOLVED = "UNRESOLVED"


def load_claims() -> list[dict[str, Any]]:
    return json.loads(
        (ROOT / "sources/claims/generic-claims.json").read_text(encoding="utf-8")
    )["claims"]


def claims_for(
    claims: list[dict[str, Any]], family: str, table: str, address: int
) -> list[dict[str, Any]]:
    global _CLAIM_INDEX
    if _CLAIM_INDEX is None or _CLAIM_INDEX[0] is not claims:
        index: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
        for claim in claims:
            claim_table = claim["subject"].get("table")
            claim_address = claim["subject"].get("address")
            if claim_table is not None and isinstance(claim_address, int):
                index[(claim_table, claim_address)].append(claim)
        _CLAIM_INDEX = (claims, index)
    indexed = _CLAIM_INDEX[1].get((table, address), [])
    return [
        claim
        for claim in indexed
        if (
            claim["subject"].get("family_scope") == [family]
            or claim["source_id"] == "vendor_growatt_v124_2020"
        )
    ]


def applicability_claims_for(
    claims: list[dict[str, Any]],
    family: str,
    table: str,
    address: int,
    source_scope: str | None = None,
) -> list[dict[str, Any]]:
    global _APPLICABILITY_INDEX
    if _APPLICABILITY_INDEX is None or _APPLICABILITY_INDEX[0] is not claims:
        index: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
        for claim in claims:
            if claim["assertion"]["kind"] != "document_range_applicability":
                continue
            family_scope = claim["subject"].get("family_scope", [])
            table_name = claim["subject"].get("table")
            if len(family_scope) == 1 and table_name is not None:
                index[(family_scope[0], table_name)].append(claim)
        _APPLICABILITY_INDEX = (claims, index)
    index = _APPLICABILITY_INDEX[1]
    return [
        claim
        for claim in index.get((family, table), [])
        if (source_scope is None or claim["subject"].get("source_scope") == source_scope)
        and claim["subject"].get("address", -1) <= address <= claim["subject"].get("address_end", -1)
    ]


def _qualifier_matches(qualifier: str | None, model_variant: str | None) -> bool | None:
    if qualifier is None:
        return True
    if model_variant is None:
        return None
    def normalize(value: str) -> str:
        return " ".join(str(value).lower().replace("/", " ").split())
    wanted = normalize(qualifier)
    actual = normalize(model_variant)
    return wanted == actual or wanted in actual


def evaluate_applicability(
    claims: list[dict[str, Any]],
    family: str,
    table: str,
    address: int,
    *,
    source_scope: str | None = None,
    model_variant: str | None = None,
) -> dict[str, Any]:
    all_matches = applicability_claims_for(claims, family, table, address)
    matches = applicability_claims_for(
        claims, family, table, address, source_scope=source_scope
    )
    if source_scope is not None and not matches:
        status = NOT_SUPPORTED_BY_DECLARATION
    elif not matches:
        status = UNRESOLVED
    else:
        source_scopes = {claim["subject"].get("source_scope") for claim in matches}
        has_external_scope = any(scope != family for scope in source_scopes)
        qualified = [
            claim
            for claim in matches
            if claim["assertion"]["value"].get("qualifier")
        ]
        if has_external_scope and source_scope is None:
            status = UNRESOLVED
        elif qualified:
            status = SUPPORTED_QUALIFIED
        else:
            status = SUPPORTED_UNCONDITIONAL
    qualifiers = [
        claim["assertion"]["value"].get("qualifier")
        for claim in matches
        if claim["assertion"]["value"].get("qualifier")
    ]
    qualifier_results = [
        _qualifier_matches(qualifier, model_variant) for qualifier in qualifiers
    ]
    return {
        "status": status,
        "claim_ids": sorted({claim["claim_id"] for claim in matches}),
        "source_scopes": sorted({claim["subject"].get("source_scope") for claim in matches}),
        "qualifiers": sorted(set(qualifiers)),
        "qualifier_satisfied": (
            True
            if not qualifier_results
            else any(result is True for result in qualifier_results)
        ),
        "qualifier_context_known": all(result is not None for result in qualifier_results),
        "candidate_claim_count": len(all_matches),
    }


def evidence_dimensions(
    claims: list[dict[str, Any]],
    family: str,
    table: str,
    address: int,
    *,
    source_scope: str | None = None,
    model_variant: str | None = None,
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
    applicability = evaluate_applicability(
        claims,
        family,
        table,
        address,
        source_scope=source_scope,
        model_variant=model_variant,
    )
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
            **applicability,
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
    physical = dimensions["physical_applicability"]
    physical_supported = physical["status"] == SUPPORTED_UNCONDITIONAL or (
        physical["status"] == SUPPORTED_QUALIFIED
        and physical["qualifier_satisfied"]
        and physical["qualifier_context_known"]
    )
    supported = sum(
        (
            physical_supported
            if name == "physical_applicability"
            else dimensions[name]["status"]
            in {"supported", "present", "documented", "verified"}
        )
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
        not physical_supported
        or dimensions["semantic_row"]["status"] != "supported"
    ) else "medium" if score >= 2 else "low"
    return {"score": score, "evidence_quality": quality, "unresolved_qualifier": unresolved}


def candidate_evidence(
    claims: list[dict[str, Any]],
    family: str,
    table: str,
    addresses: list[int],
    *,
    source_scope: str | None = None,
    model_variant: str | None = None,
) -> dict[str, Any]:
    per_record = {
        f"{family}:{table}:{address}": evidence_dimensions(
            claims,
            family,
            table,
            address,
            source_scope=source_scope,
            model_variant=model_variant,
        )
        for address in addresses
    }
    statuses = defaultdict(int)
    for dimensions in per_record.values():
        for name, value in dimensions.items():
            statuses[name] += value["status"] in {
                SUPPORTED_UNCONDITIONAL,
                SUPPORTED_QUALIFIED,
                "supported",
                "present",
                "documented",
                "verified",
            }
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
