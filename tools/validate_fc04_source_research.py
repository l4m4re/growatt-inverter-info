#!/usr/bin/env python3
"""Validate the bounded PIPELINE-5D source-research artifacts offline."""

from __future__ import annotations

import json
import re

try:
    from tools.build_fc04_source_research import (
        CANONICAL_PATH,
        CLAIMS_PATH,
        CLOSURE_PATH,
        INPUT_PATH,
        INVENTORY_PATH,
        RECONCILIATION_PATH,
        build,
        digest,
        load,
    )
except ModuleNotFoundError:
    from build_fc04_source_research import (
        CANONICAL_PATH,
        CLAIMS_PATH,
        CLOSURE_PATH,
        INPUT_PATH,
        INVENTORY_PATH,
        RECONCILIATION_PATH,
        build,
        digest,
        load,
    )


EXPECTED_ADDRESSES = [3085, 3096, 3109, 3116, 3117, 3120, 3143, 3163, 3186, 3206, 3207, 3208, 3209, 3227, 3228, 3229, 3233]


def validate() -> list[str]:
    expected = build()
    errors: list[str] = []
    for path, data in zip((INVENTORY_PATH, CLAIMS_PATH, RECONCILIATION_PATH), expected):
        if not path.is_file() or load(path) != data:
            errors.append(f"stale or missing artifact: {path}")
    if errors:
        return errors
    evidence = load(INPUT_PATH)
    inventory, claims, reconciliation = expected
    candidates = inventory["candidate_findings"]
    addresses = [item["address"] for item in candidates]
    if addresses != EXPECTED_ADDRESSES:
        errors.append("source-research inventory does not cover exactly the 17 PIPELINE-5C candidates")
    if len(claims["claims"]) != sum(len(item["properties"]) for item in candidates):
        errors.append("claim count does not match property-level findings")
    claim_ids = {claim["claim_id"] for claim in claims["claims"]}
    if len(claim_ids) != len(claims["claims"]):
        errors.append("source-research claim IDs are not unique")
    if len(reconciliation["decisions"]) != len(claims["claims"]):
        errors.append("reconciliation does not contain one decision per property finding")
    source_ids = {source["source_id"] for source in claims["sources"]}
    if any(claim["source_id"] not in source_ids for claim in claims["claims"]):
        errors.append("claim references an unknown source")
    if any(
        any(claim_id not in claim_ids for claim_id in decision["support"])
        for decision in reconciliation["decisions"]
    ):
        errors.append("reconciliation references an unknown claim")
    if inventory["canonical_modified"] or reconciliation["canonical_modified"]:
        errors.append("PIPELINE-5D changed canonical state")
    closure = load(CLOSURE_PATH)
    if digest(CANONICAL_PATH) != closure["source_inputs"]["canonical_parity_target"]:
        errors.append("canonical SHA no longer matches the PIPELINE-5C parity target")
    if inventory["resolution_counts"] != {"FULLY_RESOLVED_AT_PROTOCOL_ROLE_SCOPE": 14, "PARTIALLY_RESOLVED": 3}:
        errors.append("unexpected candidate resolution counts")
    if evidence["method"]["active_experiments"] or inventory["safety"] != {
        "canonical_modified": False,
        "live_experiment": False,
        "inverter_writes": False,
        "runtime_or_ha_changes": False,
    }:
        errors.append("source-research safety boundary changed")
    if re.search(r"wc7c6o|access[_ -]?token|session[_ -]?cookie", json.dumps(expected), re.I):
        errors.append("possible secret material in source-research artifacts")
    return errors


def main() -> None:
    validate_errors = validate()
    if validate_errors:
        print("\n".join(validate_errors))
        raise SystemExit(1)
    print("valid: PIPELINE-5D source-research artifacts pass offline checks")


if __name__ == "__main__":
    main()
