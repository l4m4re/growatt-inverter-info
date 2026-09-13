"""Regression tests for the PIPELINE-5A authority inventory."""

import json
from pathlib import Path

from tools.build_authority_coverage import build
from tools.validate_authority_coverage import validate


ROOT = Path(__file__).resolve().parents[1]
COVERAGE_PATH = ROOT / "docs" / "pipeline" / "data" / "GII-PIPELINE-5A_AUTHORITY_COVERAGE.json"


def test_authority_inventory_covers_every_canonical_record() -> None:
    """Every canonical physical record appears exactly once in the inventory."""
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    canonical = json.loads((ROOT / "spec" / "growatt-register-spec.json").read_text(encoding="utf-8"))
    physical_ids = [record["physical_id"] for record in coverage["records"]]
    assert len(physical_ids) == len(canonical["registers"])
    assert len(set(physical_ids)) == len(physical_ids)
    assert coverage["counts"]["canonical_records"] == 4048


def test_authority_inventory_recognizes_pipeline4a_targets() -> None:
    """The historical declarative diagnostic layer remains measurable."""
    coverage = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    assert coverage["declarative_coverage"]["decision_record_count"] == 29
    assert coverage["declarative_coverage"]["physical_targets"] == 18
    assert coverage["declarative_coverage"]["canonical_family_target_matches"] == 18


def test_authority_inventory_is_deterministic_and_current() -> None:
    """Repeated inventory generation matches the committed artifact exactly."""
    assert build() == json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    assert validate() == []
