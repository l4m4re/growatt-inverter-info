"""Focused invariants for the bounded PIPELINE-6 authority migration."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest
from tools.build_pipeline6_cohort import build

pytestmark = [pytest.mark.slow, pytest.mark.legacy_pipeline]

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_CANONICAL_SHA = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"


@pytest.fixture(scope="module")
def pipeline6_data() -> dict[str, object]:
    checked_in = json.loads(
        (ROOT / "docs/pipeline/data/GII-PIPELINE-6_NEXT_AUTHORITY_COHORT.json").read_text()
    )
    return build(starting_sha=checked_in["starting_main_sha"])


@pytest.mark.slow
def test_pipeline6_is_bounded_and_physical_complete(
    pipeline6_data: dict[str, object],
) -> None:
    data = pipeline6_data
    cohort = data["selected_cohort"]
    assert cohort["physical_units"] == 26
    assert len(cohort["new_decisions"]) == 18
    assert data["canonical"]["canonical_modified"] is False
    assert data["canonical"]["sha256"] == EXPECTED_CANONICAL_SHA
    assert len(data["authority"]["parity"]) == 26
    assert all(item["classification"] in {"PARITY_MATCH", "REPRESENTATION_ONLY"} for item in data["authority"]["parity"])


def test_pipeline6_reduces_legacy_authority_without_changing_record_count() -> None:
    data = json.loads(
        (ROOT / "docs/pipeline/data/GII-PIPELINE-6_NEXT_AUTHORITY_COHORT.json").read_text()
    )
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    selected_before = data["authority"]["selected_before"]
    selected_after = data["authority"]["selected_after"]
    assert after["legacy_authoritative_property_cells"] < before["legacy_authoritative_property_cells"]
    assert after["declarative_authoritative_property_cells"] > before["declarative_authoritative_property_cells"]
    assert selected_after["canonical_records"] == selected_before["canonical_records"] == 26
    assert selected_after["legacy_authoritative_property_cells"] < selected_before["legacy_authoritative_property_cells"]


@pytest.mark.slow
def test_pipeline6_output_is_reproducible_and_canonical_is_untouched(
    pipeline6_data: dict[str, object],
) -> None:
    checked_in = json.loads((ROOT / "docs/pipeline/data/GII-PIPELINE-6_NEXT_AUTHORITY_COHORT.json").read_text())
    data = pipeline6_data
    canonical = (ROOT / "spec/growatt-register-spec.json").read_bytes()
    assert hashlib.sha256(canonical).hexdigest() == EXPECTED_CANONICAL_SHA
    assert json.dumps(data, sort_keys=True) == json.dumps(checked_in, sort_keys=True)
