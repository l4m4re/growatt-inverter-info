from __future__ import annotations

import json

import pytest
from tools.build_fc04_migration import (
    CLAIMS_PATH,
    END,
    FAMILY,
    RECONCILIATION_PATH,
    SHADOW_PATH,
    START,
    build_all,
)
from tools.validate_fc04_migration import validate


@pytest.fixture(scope="module")
def fc04_data() -> tuple[dict, dict, dict]:
    return build_all()


def test_fc04_artifacts_are_current_and_safe() -> None:
    assert validate() == []


def test_claims_keep_cloud_and_shine_evidence_separate() -> None:
    claims = json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))["claims"]
    source_types = {claim["source_type"] for claim in claims}
    assert "GROWATT_CLOUD_API_OBSERVATION" in source_types
    assert "SHINE_BOUND_INJECTION_OBSERVATION" in source_types
    assert "LIVE_MODBUS_OBSERVATION" in source_types
    assert any(claim["assertion"]["kind"] == "physical_cloud_mapping" for claim in claims)
    assert any(claim["assertion"]["kind"] == "cloud_field_observation" for claim in claims)
    assert any("P1" in claim["evidence"]["grade"] for claim in claims)
    assert any("S1" in claim["evidence"]["grade"] for claim in claims)


@pytest.mark.slow
def test_fc04_cohort_and_i3000_regression(fc04_data: tuple[dict, dict, dict]) -> None:
    claims, reconciliation, shadow = fc04_data
    physical = [item for item in reconciliation["decisions"] if item["target"].get("namespace") == "MODBUS"]
    assert len(physical) == END - START + 1
    assert [item["target"]["address"] for item in physical] == list(range(START, END + 1))
    i3000 = next(item for item in physical if item["target"]["address"] == 3000)
    assert i3000["target"]["canonical_family"] == FAMILY
    assert i3000["decision"]["value"]["logical_object"] == "min-xh-fc04-semantic:3000-3000"
    assert shadow["canonical_modified"] is False
    assert shadow["parity"]["physical_identity"] == 250
    assert len(claims["claims"]) > 400


@pytest.mark.slow
def test_offline_rebuild_matches_committed_artifacts(
    fc04_data: tuple[dict, dict, dict],
) -> None:
    expected = fc04_data
    for path, data in zip((CLAIMS_PATH, RECONCILIATION_PATH, SHADOW_PATH), expected):
        assert json.loads(path.read_text(encoding="utf-8")) == data
