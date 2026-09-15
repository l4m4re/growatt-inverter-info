#!/usr/bin/env python3
"""Validate the generated GII-CONSOLIDATION-1 artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def overlaps(start: int | None, end: int | None, other_start: int, other_end: int) -> bool:
    if start is None:
        return False
    return not (end or start) < other_start and not start > other_end


def validate(root: Path = ROOT) -> dict[str, Any]:
    inventory = load(root / "sources/vendor/growatt-v1.24-blocks.json")
    candidate = load(root / "spec/growatt-register-spec-v2-candidate.json")
    matrix = load(root / "docs/consolidation/data/GII-CONSOLIDATION-1_REGISTER_MATRIX.json")
    conflicts = load(root / "docs/consolidation/data/GII-CONSOLIDATION-1_CONFLICTS.json")
    unresolved = load(root / "docs/consolidation/data/GII-CONSOLIDATION-1_UNRESOLVED.json")
    projection = load(root / "docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json")
    claims = load(root / "sources/claims/vendor/vendor_growatt_v124_2020.json")
    canonical = load(root / "spec/growatt-register-spec.json")

    errors: list[str] = []
    native_claim_ids = {
        claim["claim_id"]
        for claim in claims["claims"]
        if claim.get("source_kind") == "vendor_pdf_extraction"
        and not claim.get("exclude_from_duplicate", False)
    }
    member_ids = [claim_id for block in inventory["blocks"] for claim_id in block["rows"]]
    if set(member_ids) != native_claim_ids:
        errors.append(
            f"source row accounting mismatch: blocks={len(member_ids)} claims={len(native_claim_ids)}"
        )
    if len(member_ids) != len(set(member_ids)):
        errors.append("a source-native claim occurs in more than one block")

    claim_by_id = {claim["claim_id"]: claim for claim in claims["claims"]}
    for block in inventory["blocks"]:
        if block["address_start"] is not None and block["address_end"] is not None:
            for claim_id in block["rows"]:
                claim = claim_by_id[claim_id]
                if claim["parsed_address"] is not None and not overlaps(
                    claim["parsed_address"],
                    claim.get("parsed_address_end"),
                    block["address_start"],
                    block["address_end"],
                ):
                    errors.append(f"row {claim_id} falls outside block {block['source_block_id']}")

    candidate_registers = candidate["registers"]
    matrix_registers = matrix["registers"]
    if [r["register_id"] for r in candidate_registers] != [r["register_id"] for r in matrix_registers]:
        errors.append("candidate and register matrix ordering/content differ")
    if len(candidate_registers) != len(member_ids):
        errors.append("candidate register count does not equal source-native row count")
    if candidate["canonical_comparison"]["sha256"] != EXPECTED_CANONICAL_SHA256:
        errors.append("candidate canonical comparison hash is not the frozen expected hash")
    if inventory["source_pdf"]["sha256"] != claims["document"]["document_sha256"]:
        errors.append("inventory PDF hash differs from the source claim artifact")

    h107 = [r for r in candidate_registers if r["table"] == "holding" and r["address"] == 107]
    if len(h107) != 1:
        errors.append("H107 is not represented exactly once")
    else:
        if h107[0]["vendor"]["access_raw"] != "W":
            errors.append(f"H107 raw vendor access is {h107[0]['vendor']['access_raw']!r}, expected 'W'")
        if h107[0]["consolidated"]["access"] != "write":
            errors.append("H107 normalized access was not derived as write")
        if h107[0]["vendor"]["access_raw"] == h107[0]["consolidated"]["access"]:
            errors.append("H107 raw and normalized access were not kept distinct")

    block_ids = {block["consolidated_block_id"] for block in candidate["blocks"]}
    if len(block_ids) != len(candidate["blocks"]):
        errors.append("consolidated block IDs are not unique")
    for register in candidate_registers:
        if register["consolidated_block_id"] not in block_ids:
            errors.append(f"register references missing block: {register['register_id']}")
        for ref in register.get("conflict_refs", []):
            if not any(ref.startswith(f"{item['block']}:{item['register']}:") for item in conflicts["conflicts"]):
                errors.append(f"unresolved conflict reference: {ref}")
    for path in candidate["applicability_paths"]:
        key = (
            path["source_block_id"],
            path["source_scope"],
            path["declared_start"],
            path["declared_end"],
            path["qualifier"],
        )
        if sum(
            (
                item["source_block_id"],
                item["source_scope"],
                item["declared_start"],
                item["declared_end"],
                item["qualifier"],
            )
            == key
            for item in candidate["applicability_paths"]
        ) != 1:
            errors.append(f"duplicate applicability path: {key}")
    if candidate["overrides"]:
        errors.append("candidate unexpectedly contains unreviewed overrides")
    expected_scopes = {
        "min_tl_xh",
        "tl3_max_mid_mac",
        "max_1500v_max_x_lv",
        "mod_tl3_xh",
        "storage_mix",
        "storage_spa",
        "storage_sph",
    }
    actual_scopes = {item["source_scope"] for item in candidate["applicability"]}
    if actual_scopes != expected_scopes:
        errors.append(f"applicability declarations changed: {sorted(actual_scopes)}")
    if any("current_canonical" not in item for item in matrix_registers):
        errors.append("register matrix does not expose current canonical evidence")
    expected_categories = {
        "MATCH",
        "ENRICHED",
        "CONFLICT",
        "MISSING_IN_CANDIDATE",
        "NEW_FROM_VENDOR",
        "REPRESENTATION_ONLY",
    }
    if set(projection["comparison_with_current_canonical"]["category_counts"]) != expected_categories:
        errors.append("MIN/TL-XH comparison category summary is incomplete")
    if matrix["canonical_sha256"] != EXPECTED_CANONICAL_SHA256:
        errors.append("matrix canonical hash is not frozen")
    if conflicts["canonical_sha256"] != EXPECTED_CANONICAL_SHA256:
        errors.append("conflict canonical hash is not frozen")
    if not unresolved.get("unresolved"):
        errors.append("unresolved queue is unexpectedly empty")
    if projection["family"] != "min_tl_xh" or not projection["blocks"]:
        errors.append("MIN/TL-XH projection is missing or empty")
    if not any(item["property"] == "semantic_identity" and item["register"] == 3085 for item in conflicts["conflicts"]):
        errors.append("H3085 review candidate is missing from conflicts")
    for block in inventory["blocks"]:
        if block["role_status"] == "unresolved_ordinal_label" and block["normalized_role"] is not None:
            errors.append(f"vague heading received a normalized role: {block['source_block_id']}")
    if len(canonical["registers"]) != 4048:
        errors.append("canonical register count changed unexpectedly")

    return {
        "valid": not errors,
        "errors": errors,
        "source_native_claims": len(native_claim_ids),
        "candidate_registers": len(candidate_registers),
        "source_blocks": len(inventory["blocks"]),
        "consolidated_blocks": len(candidate["blocks"]),
    }


def main() -> None:
    result = validate()
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result["valid"] else 1)


if __name__ == "__main__":
    main()
