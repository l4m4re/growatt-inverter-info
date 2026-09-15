from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.validate_gii_consolidation import validate


ROOT = Path(__file__).parents[1]


def test_generated_consolidation_is_valid() -> None:
    result = validate(ROOT)
    assert result["valid"], result["errors"]


def test_vendor_native_rows_and_blocks_are_complete() -> None:
    inventory = json.loads(
        (ROOT / "sources/vendor/growatt-v1.24-blocks.json").read_text()
    )
    assert inventory["metrics"]["source_native_blocks_discovered"] == 15
    assert sum(len(block["rows"]) for block in inventory["blocks"]) == 1493
    assert len({claim_id for block in inventory["blocks"] for claim_id in block["rows"]}) == 1493


def test_h107_preserves_raw_access_and_normalizes_exact_token() -> None:
    matrix = json.loads(
        (ROOT / "docs/consolidation/data/GII-CONSOLIDATION-1_REGISTER_MATRIX.json").read_text()
    )
    h107 = [row for row in matrix["registers"] if row["table"] == "holding" and row["address"] == 107]
    assert len(h107) == 1
    assert h107[0]["vendor"]["access_raw"] == "W"
    assert h107[0]["consolidated"]["access"] == "write"


def test_canonical_spec_is_unchanged() -> None:
    digest = hashlib.sha256((ROOT / "spec/growatt-register-spec.json").read_bytes()).hexdigest()
    assert digest == "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


def test_min_projection_is_generated_from_shared_blocks() -> None:
    projection = json.loads(
        (ROOT / "docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json").read_text()
    )
    assert projection["family"] == "min_tl_xh"
    assert projection["blocks"]
    assert all(block["register_ids"] for block in projection["blocks"])


def test_all_v124_applicability_scopes_are_retained() -> None:
    candidate = json.loads(
        (ROOT / "spec/growatt-register-spec-v2-candidate.json").read_text()
    )
    assert {item["source_scope"] for item in candidate["applicability"]} == {
        "min_tl_xh",
        "tl3_max_mid_mac",
        "max_1500v_max_x_lv",
        "mod_tl3_xh",
        "storage_mix",
        "storage_spa",
        "storage_sph",
    }


def test_min_comparison_exposes_required_categories() -> None:
    projection = json.loads(
        (ROOT / "docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json").read_text()
    )
    assert set(projection["comparison_with_current_canonical"]["category_counts"]) == {
        "MATCH",
        "ENRICHED",
        "CONFLICT",
        "MISSING_IN_CANDIDATE",
        "NEW_FROM_VENDOR",
        "REPRESENTATION_ONLY",
    }
