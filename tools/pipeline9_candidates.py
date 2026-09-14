"""Repository-wide, claim-driven candidate enumeration for PIPELINE-9."""

from __future__ import annotations

from collections import defaultdict
import json
from pathlib import Path
from typing import Any

try:
    from tools.build_authority_coverage import canonical_authority_origins, override_keys
    from tools.pipeline8_evidence import (
        SUPPORTED_QUALIFIED,
        SUPPORTED_UNCONDITIONAL,
        evidence_dimensions,
        evaluate_applicability,
        score_dimensions,
    )
    from tools.property_cell_provenance import property_cell_support, supported_property_cells
except ModuleNotFoundError:
    from build_authority_coverage import canonical_authority_origins, override_keys
    from pipeline8_evidence import SUPPORTED_QUALIFIED, SUPPORTED_UNCONDITIONAL, evidence_dimensions, evaluate_applicability, score_dimensions
    from property_cell_provenance import property_cell_support, supported_property_cells

ROOT = Path(__file__).resolve().parents[1]
V124_SOURCE = "vendor_growatt_v124_2020"
REQUIRED_SOURCE_SCOPES = (
    "max_1500v_max_x_lv",
    "min_tl_xh",
    "mod_tl3_xh",
    "storage_mix",
    "storage_spa",
    "storage_sph",
    "tl3_max_mid_mac",
)
MAX_TARGETS = 8
_CLAIMS_BY_KEY: tuple[object, dict[tuple[str, int, str], list[dict[str, Any]]]] | None = None
_CLAIMS_BY_ADDRESS: tuple[object, dict[tuple[str, int], list[dict[str, Any]]]] | None = None


def load_json(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def source_scope_catalog(claims: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    """Return all retained V1.24 declarations, without merging source scopes."""
    result: dict[str, dict[str, Any]] = {}
    for claim in claims:
        if claim["assertion"]["kind"] != "document_range_applicability":
            continue
        subject = claim["subject"]
        scope = subject["source_scope"]
        entry = result.setdefault(
            scope,
            {
                "source_scope": scope,
                "canonical_family": subject["family_scope"][0],
                "source_declarations": set(),
                "range_claim_ids": [],
                "ranges": [],
            },
        )
        entry["source_declarations"].add(subject["source_declaration"])
        entry["range_claim_ids"].append(claim["claim_id"])
        entry["ranges"].append(
            {
                "claim_id": claim["claim_id"],
                "table": subject["table"],
                "function_code": claim["assertion"]["value"]["function_code"],
                "start": subject["address"],
                "end": subject["address_end"],
                "qualifier": claim["assertion"]["value"].get("qualifier"),
                "source_declaration": subject["source_declaration"],
            }
        )
    for entry in result.values():
        entry["source_declarations"] = sorted(entry["source_declarations"])
        entry["range_claim_ids"].sort()
        entry["ranges"].sort(key=lambda item: (item["table"], item["start"], item["end"], item["function_code"]))
    return dict(sorted(result.items()))


def _vendor_rows(claims: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return sorted(
        (
            claim
            for claim in claims
            if claim["source_id"] == V124_SOURCE
            and claim["assertion"]["kind"] == "vendor_source_row"
            and claim["subject"].get("table") in {"holding", "input"}
            and isinstance(claim["subject"].get("address"), int)
        ),
        key=lambda claim: claim["claim_id"],
    )


def _canonical_indexes() -> tuple[dict[tuple[str, str, int], dict[str, Any]], dict[tuple[str, str, int], dict[str, Any]]]:
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in load_json("spec/growatt-register-spec.json")["registers"]
    }
    authority = {
        (item["family"], item["table"], item["address"]): item
        for item in load_json("docs/pipeline/data/GII-PIPELINE-8_VENDOR_APPLICABILITY_AND_NEXT_COHORT.json").get("authority", {}).get("records", [])
    }
    if not authority:
        try:
            from tools.build_authority_coverage import build
        except ModuleNotFoundError:
            from build_authority_coverage import build

        authority = {
            (item["family"], item["table"], item["address"]): item
            for item in build()["records"]
        }
    return canonical, authority


def accepted_decisions(*, exclude_sources: set[str] | None = None) -> list[dict[str, Any]]:
    """Read accepted authority decisions from the checked-in registry."""
    registry = load_json("reconciliation/accepted-authority-sources.json")
    excluded = exclude_sources or set()
    result: list[dict[str, Any]] = []
    for source in registry["sources"]:
        path = source["path"]
        if path in excluded:
            continue
        decisions = load_json(path)["decisions"]
        selector = source.get("selector")
        if selector and selector["kind"] == "modbus_holding_addresses_from_artifact":
            addresses = set(load_json(selector["artifact"])["selected_cohort"]["addresses"])
            decisions = [
                item
                for item in decisions
                if item["target"].get("namespace") == "MODBUS"
                and item["target"].get("table") == "holding"
                and item["target"].get("address") in addresses
            ]
        result.extend(decisions)
    return sorted(result, key=lambda item: item["decision_id"])


def promoted_properties(decisions: list[dict[str, Any]]) -> dict[tuple[str, str, int], set[str]]:
    claims_by_id = {
        claim["claim_id"]: claim for claim in load_json("sources/claims/generic-claims.json")["claims"]
    }
    result: dict[tuple[str, str, int], set[str]] = defaultdict(set)
    for item in decisions:
        target = item.get("target", {})
        if target.get("namespace") != "MODBUS":
            continue
        result[(target["canonical_family"], target["table"], target["address"])].update(
            supported_property_cells(item, claims_by_id)
        )
    return result


def _claims_at(claims: list[dict[str, Any]], table: str, address: int, kind: str) -> list[dict[str, Any]]:
    global _CLAIMS_BY_KEY
    if _CLAIMS_BY_KEY is None or _CLAIMS_BY_KEY[0] is not claims:
        index: dict[tuple[str, int, str], list[dict[str, Any]]] = defaultdict(list)
        for claim in claims:
            if claim["source_id"] != V124_SOURCE:
                continue
            table_name = claim["subject"].get("table")
            address_value = claim["subject"].get("address")
            if table_name in {"holding", "input"} and isinstance(address_value, int):
                index[(table_name, address_value, claim["assertion"]["kind"])].append(claim)
        for values in index.values():
            values.sort(key=lambda claim: claim["claim_id"])
        _CLAIMS_BY_KEY = (claims, index)
    return _CLAIMS_BY_KEY[1].get((table, address, kind), [])


def _claims_at_address(
    claims: list[dict[str, Any]], table: str, address: int
) -> list[dict[str, Any]]:
    global _CLAIMS_BY_ADDRESS
    if _CLAIMS_BY_ADDRESS is None or _CLAIMS_BY_ADDRESS[0] is not claims:
        index: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
        for claim in claims:
            table_name = claim["subject"].get("table")
            address_value = claim["subject"].get("address")
            if table_name in {"holding", "input"} and isinstance(address_value, int):
                index[(table_name, address_value)].append(claim)
        _CLAIMS_BY_ADDRESS = (claims, index)
    return _CLAIMS_BY_ADDRESS[1].get((table, address), [])


def _target_key(target: dict[str, Any]) -> tuple[str, str, int]:
    return target["family"], target["table"], target["address"]


def path_identity(target: dict[str, Any]) -> tuple[str, str, int, str, str]:
    """Identify an evidence path without conflating it with a physical target."""
    return (
        target["family"] if "family" in target else target["canonical_family"],
        target["table"],
        target["address"],
        target["source_scope"],
        target["source_declaration"],
    )


def path_key(target: dict[str, Any]) -> str:
    return json.dumps(path_identity(target), ensure_ascii=False, separators=(",", ":"))


def _property_support(
    claims: list[dict[str, Any]],
    row_claim: dict[str, Any],
    target: dict[str, Any],
    dimensions: dict[str, Any],
) -> dict[str, list[str]]:
    table = target["table"]
    address = target["address"]
    support: dict[str, list[str]] = {
        "semantic_mapping": [row_claim["claim_id"], *dimensions["physical_applicability"]["claim_ids"]],
    }
    enums = _claims_at(claims, table, address, "enum_member")
    packed = _claims_at(claims, table, address, "packed_field")
    if enums:
        support["enum"] = [claim["claim_id"] for claim in enums]
    if packed:
        support["packed_encoding"] = [claim["claim_id"] for claim in packed]
    qualifiers = dimensions["model_specific_qualifier"]["claim_ids"]
    if qualifiers:
        support["semantic_mapping"].extend(qualifiers)
    return {key: sorted(set(value)) for key, value in support.items()}


def _dimension_extensions(
    claims: list[dict[str, Any]],
    row_claim: dict[str, Any],
    target: dict[str, Any],
    dimensions: dict[str, Any],
    authority_record: dict[str, Any],
) -> dict[str, Any]:
    value = row_claim["assertion"].get("value", {})
    independent = dimensions["independent_corroboration"]["claim_ids"]
    live = [
        claim_id
        for claim_id in independent
        if any(
            token in next(claim["source_type"] for claim in claims if claim["claim_id"] == claim_id).lower()
            for token in ("live", "cloud", "shine")
        )
    ]
    unit_scale_present = bool(value.get("raw_unit_text") or value.get("raw_value_text") or value.get("raw_type"))
    source_conflicts = [
        claim["claim_id"]
        for claim in _claims_at_address(claims, target["table"], target["address"])
        if claim["evidence"].get("status") in {"conflict", "contradictory"}
    ]
    return {
        "unit_scale": {
            "status": "present" if unit_scale_present else "not_present",
            "claim_ids": [row_claim["claim_id"]] if unit_scale_present else [],
            "raw_unit_text": value.get("raw_unit_text"),
            "raw_value_text": value.get("raw_value_text"),
        },
        "source_conflict": {
            "status": "present" if source_conflicts else "not_present",
            "claim_ids": sorted(source_conflicts),
        },
        "runtime_live_evidence": {
            "status": "present" if live else "not_present",
            "claim_ids": sorted(live),
        },
        "unresolved_property_count": {
            "status": "derived_from_authority_inventory",
            "count": len(authority_record.get("missing_declarative_properties", [])),
            "properties": sorted(authority_record.get("missing_declarative_properties", [])),
        },
    }


def _target_evidence(
    claims: list[dict[str, Any]],
    row_claim: dict[str, Any],
    target: dict[str, Any],
    authority_record: dict[str, Any],
    source_scope: str,
) -> dict[str, Any]:
    dimensions = evidence_dimensions(
        claims,
        target["family"],
        target["table"],
        target["address"],
        source_scope=source_scope,
    )
    dimensions["selected_vendor_row"] = {
        "status": "supported",
        "claim_ids": [row_claim["claim_id"]],
        "variable": row_claim["assertion"]["value"].get("reconstructed_variable")
        or row_claim["assertion"]["value"].get("raw_variable"),
    }
    dimensions.update(_dimension_extensions(claims, row_claim, target, dimensions, authority_record))
    return dimensions


def _candidate_properties(
    claims: list[dict[str, Any]],
    row_claim: dict[str, Any],
    target: dict[str, Any],
    dimensions: dict[str, Any],
) -> dict[str, list[str]]:
    support = _property_support(claims, row_claim, target, dimensions)
    if dimensions["semantic_row"]["status"] != "supported":
        support.pop("semantic_mapping", None)
    return support


def _authority_delta(
    authority_record: dict[str, Any],
    canonical_record: dict[str, Any],
    accepted: dict[tuple[str, str, int], set[str]],
    supported_cells: set[str],
    overrides: set[tuple[str, str, int, str]] | None = None,
) -> dict[str, Any]:
    origins = canonical_authority_origins(canonical_record, overrides or override_keys())
    legacy = {
        name
        for name, detail in origins.items()
        if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
    }
    key = (canonical_record["family"], canonical_record["table"], canonical_record["address"])
    already = accepted.get(key, set())
    promoted = set(supported_cells)
    return {
        "legacy_before": len(legacy - already),
        "declarative_before": len(already),
        "expected_reduction": len((legacy - already) & promoted),
        "promoted_properties": sorted(promoted),
    }


def _candidate_authority_support(
    claims: list[dict[str, Any]], properties: dict[str, list[str]]
) -> dict[str, dict[str, Any]]:
    claims_by_id = {claim["claim_id"]: claim for claim in claims}
    result: dict[str, dict[str, Any]] = {}
    for decision_property, support in properties.items():
        decision = {
            "target": {"property": decision_property},
            "support": support,
            "decision": {"value": {}},
        }
        for property_name, detail in property_cell_support(decision, claims_by_id).items():
            existing = result.setdefault(property_name, {"status": "supported", "claim_ids": [], "source_types": []})
            existing["claim_ids"].extend(detail["claim_ids"])
            existing["source_types"].extend(detail["source_types"])
    return {
        property_name: {
            "status": detail["status"],
            "claim_ids": sorted(set(detail["claim_ids"])),
            "source_types": sorted(set(detail["source_types"])),
        }
        for property_name, detail in sorted(result.items())
    }


def enumerate_candidates(*, exclude_accepted_sources: set[str] | None = None) -> dict[str, Any]:
    claims = load_json("sources/claims/generic-claims.json")["claims"]
    claim_by_id = {claim["claim_id"]: claim for claim in claims}
    canonical, authority = _canonical_indexes()
    scopes = source_scope_catalog(claims)
    rows = _vendor_rows(claims)
    targets_by_scope: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for scope, declaration in scopes.items():
        family = declaration["canonical_family"]
        for key, record in sorted(authority.items()):
            if key[0] != family or key not in canonical:
                continue
            applicability = evaluate_applicability(
                claims, family, key[1], key[2], source_scope=scope
            )
            if applicability["status"] not in {SUPPORTED_UNCONDITIONAL, SUPPORTED_QUALIFIED}:
                continue
            targets_by_scope[scope].append(
                {
                    "family": family,
                    "table": key[1],
                    "address": key[2],
                    "source_scope": scope,
                    "source_declarations": sorted(
                        {
                            claim_by_id[claim_id]["subject"]["source_declaration"]
                            for claim_id in applicability["claim_ids"]
                        }
                    ),
                    "applicability": applicability,
                }
            )
            targets_by_scope[scope][-1]["source_declaration"] = targets_by_scope[scope][-1]["source_declarations"][0]

    accepted = promoted_properties(accepted_decisions(exclude_sources=exclude_accepted_sources))
    overrides = override_keys()
    grouped: dict[tuple[str, str, int, str], list[dict[str, Any]]] = defaultdict(list)
    targets_by_location: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
    for scope, targets in targets_by_scope.items():
        for target in targets:
            targets_by_location[(scope, target["table"], target["address"])].append(target)

    for row in rows:
        table = row["subject"]["table"]
        address = row["subject"]["address"]
        for scope in scopes:
            for target in targets_by_location.get((scope, table, address), []):
                canonical_record = canonical[(target["family"], table, address)]
                semantic_key = canonical_record["semantic_identity"].get("quantity")
                if not semantic_key:
                    continue
                authority_record = authority[(target["family"], table, address)]
                dimensions = _target_evidence(claims, row, target, authority_record, scope)
                properties = _candidate_properties(claims, row, target, dimensions)
                if not properties:
                    continue
                grouped[(row["claim_id"], table, address, semantic_key)].append(
                    {
                        "target": target,
                        "canonical": canonical_record,
                        "authority": authority_record,
                        "evidence": dimensions,
                        "properties": properties,
                    }
                )

    candidates: list[dict[str, Any]] = []
    for (row_id, table, address, semantic_key), items in sorted(grouped.items()):
        unique_targets = {
            (_target_key(item["target"]), item["target"]["source_scope"]): item
            for item in items
        }
        items = [unique_targets[key] for key in sorted(unique_targets)]
        if len(items) > MAX_TARGETS:
            continue
        target_evidence = {path_key(item["target"]): item["evidence"] for item in items}
        physical_groups: dict[tuple[str, str, int], list[dict[str, Any]]] = defaultdict(list)
        for item in items:
            physical_groups[_target_key(item["target"])].append(item)
        expected = {}
        properties_by_physical_target = {}
        authority_support_by_physical_target = {}
        for key, physical_items in sorted(physical_groups.items()):
            combined_properties: dict[str, list[str]] = defaultdict(list)
            for item in physical_items:
                for property_name, support in item["properties"].items():
                    combined_properties[property_name].extend(support)
            combined_properties = {
                property_name: sorted(set(support))
                for property_name, support in combined_properties.items()
            }
            first = physical_items[0]
            authority_support = _candidate_authority_support(claims, combined_properties)
            expected[key] = _authority_delta(
                first["authority"],
                first["canonical"],
                accepted,
                set(authority_support),
                overrides,
            )
            properties_by_physical_target[":".join(map(str, key))] = combined_properties
            authority_support_by_physical_target[":".join(map(str, key))] = authority_support
        expected_reduction = sum(item["expected_reduction"] for item in expected.values())
        if expected_reduction <= 0:
            continue
        scores = [score_dimensions(item["evidence"]) for item in items]
        statuses = [item["target"]["applicability"]["status"] for item in items]
        unresolved = sum(
            1
            for item in items
            if item["evidence"]["unresolved_qualifier"]["status"] == "present"
            or not item["target"]["applicability"]["qualifier_context_known"]
        )
        total_score = sum(score["score"] for score in scores)
        evidence_completeness = total_score / (len(items) * 8)
        source_scopes = sorted({item["target"]["source_scope"] for item in items})
        families = sorted({item["target"]["family"] for item in items})
        cross_family = len(families)
        qualifier_complexity = sum(status == SUPPORTED_QUALIFIED for status in statuses)
        rank_score = (
            expected_reduction * 1000
            + evidence_completeness * 100
            + len(items) * 4
            + cross_family * 3
            - unresolved * 25
            - qualifier_complexity * 10
        )
        candidates.append(
            {
                "id": f"v124-row-{table}-{address}-{row_id.rsplit(':', 1)[-1]}",
                "kind": "shared_vendor_row" if len(source_scopes) > 1 else "source_row",
                "vendor_row_claim_id": row_id,
                "table": table,
                "address": address,
                "semantic_key": semantic_key,
                "source_scopes": source_scopes,
                "canonical_families": families,
                "targets": [item["target"] for item in items],
                "physical_units": len(physical_groups),
                "canonical_physical_target_count": len(physical_groups),
                "applicability_path_count": len(items),
                "target_count": len(physical_groups),
                "evidence_dimensions": target_evidence,
                "evidence_score": total_score,
                "evidence_completeness": round(evidence_completeness, 6),
                "unresolved_or_qualified_count": unresolved + qualifier_complexity,
                "qualifier_complexity": qualifier_complexity,
                "cross_family_count": cross_family,
                "expected_reduction": expected_reduction,
                "authority_by_target": {
                    ":".join(map(str, key)): value for key, value in expected.items()
                },
                "properties_by_physical_target": properties_by_physical_target,
                "authority_support_by_physical_target": authority_support_by_physical_target,
                "properties_by_target": {
                    path_key(item["target"]): item["properties"]
                    for item in items
                },
                "source_conflict": any(
                    item["evidence"]["source_conflict"]["status"] == "present" for item in items
                ),
                "runtime_live_evidence": any(
                    item["evidence"]["runtime_live_evidence"]["status"] == "present" for item in items
                ),
                "write_documentation": any(
                    item["evidence"]["write_documentation"]["status"] == "documented" for item in items
                ),
                "live_write_verification": any(
                    item["evidence"]["live_write_verification"]["status"] == "verified" for item in items
                ),
                "bounded": True,
                "rank_score": round(rank_score, 6),
            }
        )

    candidates.sort(key=lambda item: (-item["rank_score"], item["id"]))
    for rank, candidate in enumerate(candidates, 1):
        candidate["rank"] = rank

    coverage: dict[str, dict[str, Any]] = {}
    for scope in REQUIRED_SOURCE_SCOPES:
        applicable = targets_by_scope.get(scope, [])
        target_keys = {_target_key(item) for item in applicable}
        partly = sum(bool(accepted.get(key)) for key in target_keys if key in authority)
        legacy_cells = sum(
            _authority_delta(
                authority[key], canonical[key], accepted, {}, overrides
            ).get("legacy_before", 0)
            for key in target_keys
            if key in canonical
        )
        scoped_candidates = [item for item in candidates if scope in item["source_scopes"]]
        qualified = sum(
            any(target["source_scope"] == scope and target["applicability"]["status"] == SUPPORTED_QUALIFIED for target in item["targets"])
            for item in scoped_candidates
        )
        coverage[scope] = {
            "canonical_family": scopes.get(scope, {}).get("canonical_family"),
            "declared_range_count": len(scopes.get(scope, {}).get("ranges", [])),
            "applicable_physical_records_found": len(target_keys),
            "partly_declarative_records": partly,
            "remaining_legacy_authoritative_cells": legacy_cells,
            "evidence_supported_candidate_count": len(scoped_candidates),
            "unresolved_or_qualified_candidate_count": qualified,
            "best_bounded_candidate": scoped_candidates[0]["id"] if scoped_candidates else None,
            "best_expected_reduction": scoped_candidates[0]["expected_reduction"] if scoped_candidates else 0,
        }
    missing = sorted(set(REQUIRED_SOURCE_SCOPES) - set(scopes))
    return {
        "source_scopes": scopes,
        "required_source_scopes": list(REQUIRED_SOURCE_SCOPES),
        "missing_source_scopes": missing,
        "candidate_ranking": candidates,
        "coverage": coverage,
        "candidate_universe": {
            "candidate_count": len(candidates),
            "shared_vendor_row_count": sum(item["kind"] == "shared_vendor_row" for item in candidates),
            "source_row_count": sum(item["kind"] == "source_row" for item in candidates),
            "non_min_candidate_count": sum("min_tl_xh" not in item["source_scopes"] for item in candidates),
            "max_targets": MAX_TARGETS,
        },
    }
