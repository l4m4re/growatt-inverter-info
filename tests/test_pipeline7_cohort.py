"""Focused invariants for the bounded PIPELINE-7 authority migration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from tools.build_pipeline7_cohort import build

pytestmark = pytest.mark.slow

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANONICAL_SHA = (
    "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
)


@pytest.fixture(scope="module")
def pipeline7_data() -> dict[str, object]:
    return build(starting_sha="test-start")


def test_pipeline7_ranks_and_selects_one_bounded_cohort(
    pipeline7_data: dict[str, object],
) -> None:
    data = pipeline7_data
    assert data["candidate_ranking"][0]["id"] == "min_tl_xh_holding_3083_3086"
    assert data["selected_cohort"]["addresses"] == [3083, 3084, 3085, 3086]
    assert data["selected_cohort"]["physical_units"] == 4
    assert len(data["authority"]["parity"]) == 4
    assert all(
        item["classification"]
        in {"PARITY_MATCH", "SUPPORTED_CANONICAL_CORRECTION_CANDIDATE"}
        for item in data["authority"]["parity"]
    )


def test_pipeline7_accounts_for_pipeline6_and_reduces_authority(
    pipeline7_data: dict[str, object],
) -> None:
    data = pipeline7_data
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    assert before["legacy_authoritative_property_cells"] == 49525
    assert before["declarative_authoritative_property_cells"] == 148
    assert before["legacy_exclusive_property_cells"] == 41
    assert (
        after["legacy_authoritative_property_cells"]
        < before["legacy_authoritative_property_cells"]
    )
    assert (
        after["declarative_authoritative_property_cells"]
        > before["declarative_authoritative_property_cells"]
    )
    assert (
        after["legacy_exclusive_property_cells"]
        == before["legacy_exclusive_property_cells"]
    )


def test_pipeline7_is_deterministic_and_keeps_canonical_frozen(
    pipeline7_data: dict[str, object],
) -> None:
    first = pipeline7_data
    second = build(starting_sha="test-start")
    assert json.dumps(first, sort_keys=True) == json.dumps(second, sort_keys=True)
    canonical = (ROOT / "spec/growatt-register-spec.json").read_bytes()
    assert hashlib.sha256(canonical).hexdigest() == EXPECTED_CANONICAL_SHA
    checked_in = json.loads(
        (
            ROOT / "docs/pipeline/data/GII-PIPELINE-7_NEXT_AUTHORITY_COHORT.json"
        ).read_text()
    )
    assert checked_in["canonical"] == first["canonical"]
    assert checked_in["candidate_ranking"] == first["candidate_ranking"]
