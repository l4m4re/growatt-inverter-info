"""Property-cell evidence rules for declarative authority accounting."""

from __future__ import annotations

import re
from typing import Any

TRACKED_PROPERTY_CELLS = (
    "physical_identity",
    "length_words",
    "signedness",
    "scale",
    "unit",
    "physical_quantity",
    "human_description",
    "enum_definitions",
    "packed_layout",
    "access",
    "model_applicability",
    "aliases",
    "provenance_support",
    "normalization",
    "write_semantics",
)

_PROPERTY_ALIASES = {
    "semantic_quantity": "physical_quantity",
    "semantic_mapping": "physical_quantity",
    "description": "human_description",
    "name": "human_description",
    "enum": "enum_definitions",
    "bitfield": "packed_layout",
    "packed_field": "packed_layout",
    "packed_layout": "packed_layout",
    "word_length": "length_words",
    "write_semantics": "write_semantics",
}
_SIGNEDNESS_RE = re.compile(r"\b(?:u|i)\d+\b|\b(?:un)?signed\b", re.IGNORECASE)


def _claim_value(claim: dict[str, Any]) -> Any:
    return claim.get("assertion", {}).get("value")


def _is_supported_claim(claim: dict[str, Any]) -> bool:
    evidence = claim.get("evidence", {})
    assertion = claim.get("assertion", {})
    status = str(evidence.get("status", "")).lower()
    value = assertion.get("value")
    if isinstance(value, dict):
        status = f"{status} {value.get('status', '')}".lower()
    return any(token in status for token in ("support", "proven", "confirm", "resolved", "retained", "complete"))


def _add(result: dict[str, list[str]], property_name: str, claim: dict[str, Any]) -> None:
    if property_name in TRACKED_PROPERTY_CELLS and _is_supported_claim(claim):
        result.setdefault(property_name, []).append(claim["claim_id"])


def _explicit_value_support(result: dict[str, list[str]], claim: dict[str, Any], value: dict[str, Any]) -> None:
    property_name = _PROPERTY_ALIASES.get(str(value.get("property", "")))
    if property_name and str(value.get("status", "")).upper() in {"SUPPORTED", "PROVEN", "CONFIRMED", "RESOLVED"}:
        _add(result, property_name, claim)
    if value.get("semantic_key") or value.get("canonical_name") or value.get("name"):
        _add(result, "physical_quantity", claim)
    if value.get("description") or value.get("canonical_name") or value.get("name"):
        _add(result, "human_description", claim)
    if value.get("unit") not in (None, ""):
        _add(result, "unit", claim)
    if value.get("access") not in (None, ""):
        _add(result, "access", claim)
    data_type = value.get("data_type") or value.get("datatype") or value.get("type")
    encoding = value.get("encoding")
    if data_type not in (None, ""):
        if "word" in str(data_type).lower():
            _add(result, "length_words", claim)
        if _SIGNEDNESS_RE.search(str(data_type)):
            _add(result, "signedness", claim)
    if encoding not in (None, "") and _SIGNEDNESS_RE.search(str(encoding)):
        _add(result, "signedness", claim)
    if value.get("scale") not in (None, ""):
        _add(result, "scale", claim)
    if value.get("normalization") not in (None, ""):
        _add(result, "normalization", claim)


def _claim_capabilities(claim: dict[str, Any]) -> set[str]:
    kind = claim.get("assertion", {}).get("kind")
    value = _claim_value(claim)
    result: dict[str, list[str]] = {}
    if kind in {"property_support", "property_review"} and isinstance(value, dict):
        _explicit_value_support(result, claim, value)
    elif kind == "vendor_source_row" and isinstance(value, dict):
        variable = value.get("raw_variable") or value.get("reconstructed_variable")
        description = value.get("raw_description")
        if variable or description:
            _add(result, "physical_quantity", claim)
        if description:
            _add(result, "human_description", claim)
        if value.get("raw_unit_text") and not str(value["raw_unit_text"]).strip().isdigit():
            _add(result, "unit", claim)
        if value.get("raw_access_text"):
            _add(result, "access", claim)
        if value.get("raw_type") and _SIGNEDNESS_RE.search(str(value["raw_type"])):
            _add(result, "signedness", claim)
    elif kind in {"human_interpretation", "reviewed_semantic_mapping", "description"} and isinstance(value, dict):
        _explicit_value_support(result, claim, value)
    elif kind == "register_name" and value not in (None, ""):
        _add(result, "physical_quantity", claim)
    elif kind == "access" and value not in (None, ""):
        _add(result, "access", claim)
    elif kind == "enum_member":
        _add(result, "enum_definitions", claim)
    elif kind == "packed_field":
        _add(result, "packed_layout", claim)
    return {property_name for property_name, claim_ids in result.items() if claim_ids}


def property_cell_support(
    decision: dict[str, Any], claims_by_id: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Return explicit property-cell support for a reconciliation decision."""
    explicit = decision.get("authority_support")
    if isinstance(explicit, dict):
        return {
            property_name: {
                "status": detail.get("status", "unresolved"),
                "claim_ids": sorted(detail.get("claim_ids", [])),
                "source_types": sorted(
                    {claims_by_id[claim_id]["assertion"]["kind"] for claim_id in detail.get("claim_ids", []) if claim_id in claims_by_id}
                ),
            }
            for property_name, detail in sorted(explicit.items())
        }

    support: dict[str, list[str]] = {}
    target_property = decision.get("target", {}).get("property")
    for claim_id in decision.get("support", []):
        claim = claims_by_id.get(claim_id)
        if not claim:
            continue
        for property_name in _claim_capabilities(claim):
            support.setdefault(property_name, []).append(claim_id)
    if target_property == "enum":
        support = {name: ids for name, ids in support.items() if name == "enum_definitions"}
    elif target_property in {"bitfield", "packed_encoding"}:
        support = {name: ids for name, ids in support.items() if name == "packed_layout"}
    elif target_property == "status":
        support = {"provenance_support": decision.get("support", [])} if decision.get("support") else {}
    return {
        property_name: {
            "status": "supported",
            "claim_ids": sorted(set(claim_ids)),
            "source_types": sorted({claims_by_id[claim_id]["assertion"]["kind"] for claim_id in claim_ids}),
        }
        for property_name, claim_ids in sorted(support.items())
        if claim_ids
    }


def supported_property_cells(
    decision: dict[str, Any], claims_by_id: dict[str, dict[str, Any]]
) -> set[str]:
    return {
        property_name
        for property_name, detail in property_cell_support(decision, claims_by_id).items()
        if detail.get("status") == "supported" and detail.get("claim_ids")
    }


def authority_support_for_decision(
    decision: dict[str, Any], claims_by_id: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """Return support with unresolved tracked cells visible for generated output."""
    supported = property_cell_support(decision, claims_by_id)
    return {
        property_name: supported.get(
            property_name,
            {"status": "unresolved", "claim_ids": [], "source_types": []},
        )
        for property_name in TRACKED_PROPERTY_CELLS
    }
