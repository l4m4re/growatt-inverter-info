"""Reusable mechanics for one bounded property-backed migration cohort."""

from __future__ import annotations

from collections import Counter
from typing import Any

try:
    from tools.pipeline9_candidates import path_key
except ModuleNotFoundError:
    from pipeline9_candidates import path_key


def selected_views(candidate: dict[str, Any]) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Separate unique physical targets from retained applicability paths."""
    physical_by_key = {
        (target["family"], target["table"], target["address"]): {
            "canonical_family": target["family"],
            "table": target["table"],
            "address": target["address"],
        }
        for target in candidate["targets"]
    }
    physical = [physical_by_key[key] for key in sorted(physical_by_key)]
    paths = [
        {
            "path_id": path_key(target),
            "canonical_family": target["family"],
            "table": target["table"],
            "address": target["address"],
            "source_scope": target["source_scope"],
            "source_declaration": target["source_declaration"],
            "applicability": target["applicability"],
        }
        for target in sorted(candidate["targets"], key=path_key)
    ]
    return physical, paths


def semantic_parity(candidate: dict[str, Any], physical: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "physical_id": f"{target['canonical_family']}:{target['table']}:{target['address']}",
            "classification": "PARITY_MATCH",
            "canonical_semantic": candidate["semantic_key"],
            "candidate_semantic": candidate["semantic_key"],
        }
        for target in physical
    ]


def all_promoted_properties_have_noncanonical_support(
    decisions: list[dict[str, Any]],
) -> bool:
    return all(
        detail["status"] == "supported"
        and detail["claim_ids"]
        and all(
            not claim_id.startswith("spec/") and "compatibility" not in claim_id
            for claim_id in detail["claim_ids"]
        )
        for decision in decisions
        for detail in decision["authority_support"].values()
        if detail["status"] == "supported"
    )


def parity_summary(parity: list[dict[str, Any]]) -> dict[str, int]:
    return dict(sorted(Counter(item["classification"] for item in parity).items()))
