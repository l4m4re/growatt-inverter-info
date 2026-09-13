from __future__ import annotations

import json
from collections import Counter

from tools.build_fc04_closure import OUTPUT_PATH, RECONCILIATION_PATH, build
from tools.validate_fc04_closure import validate


def test_closure_covers_all_5b_unresolved_targets() -> None:
    inventory, reconciliation = build()
    assert validate() == []
    assert inventory["original_unresolved_count"] == 129
    assert len(inventory["targets"]) == 129
    assert len(reconciliation["decisions"]) == 129


def test_closure_preserves_evidence_and_safety_boundaries() -> None:
    inventory, _ = build()
    counts = Counter(target["classification"] for target in inventory["targets"])
    assert counts["EXISTING_EVIDENCE_SUFFICIENT"] == 3
    assert inventory["active_experiments"] == []
    assert inventory["safety"]["local_ground_truth_modified"] is False
    assert inventory["safety"]["intentional_inverter_writes"] is False
    assert any(target["address"] == 3110 and target["source_claims"] for target in inventory["targets"])


def test_closure_artifacts_rebuild_deterministically() -> None:
    expected = build()
    assert json.loads(OUTPUT_PATH.read_text(encoding="utf-8")) == expected[0]
    assert json.loads(RECONCILIATION_PATH.read_text(encoding="utf-8")) == expected[1]
