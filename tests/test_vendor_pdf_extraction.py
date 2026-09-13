"""Public-safe tests for the PIPELINE-2 vendor source layer."""

from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from tools import extract_vendor_pdf
from tools.compare_vendor_extractions import compare
from tools.validate_vendor_claims import validate


ROOT = Path(__file__).parents[1]
CLAIM_FILES = [
    ROOT / "sources/claims/vendor/vendor_growatt_v305_2013.json",
    ROOT / "sources/claims/vendor/vendor_growatt_v314_2016.json",
    ROOT / "sources/claims/vendor/vendor_growatt_v124_2020.json",
]


def claims_by_id(path: Path) -> dict[str, dict]:
    return {claim["claim_id"]: claim for claim in json.loads(path.read_text())["claims"]}


def test_claim_artifacts_validate() -> None:
    schema = ROOT / "sources/claims/vendor/schema.json"
    assert all(validate(path, schema)["valid"] for path in CLAIM_FILES)


def test_golden_cases() -> None:
    cases = json.loads((ROOT / "tests/golden_vendor_pdf/golden_cases.json").read_text())["cases"]
    by_document = {path.stem.removeprefix("vendor_"): claims_by_id(path) for path in CLAIM_FILES}
    for case in cases:
        document_id = case["document_id"]
        claims = next(claims_by_id(path) for path in CLAIM_FILES if document_id in path.name)
        if "claim_id" in case:
            claim = claims[case["claim_id"]]
        else:
            candidates = [claim for claim in claims.values() if claim.get("register_table") == case["table"] and claim.get("parsed_address") == case["parsed_address"]]
            assert candidates
            claim = candidates[0]
        assert [claim["page"], claim["page_end"]] == [case["pages"][0], case["pages"][-1]] if "pages" in case else True
        text = claim["reconstructed_row_text"]
        assert all(value.lower() in text.lower() for value in case["must_contain"])


def test_reviewed_continuations_and_raw_split_are_explicit() -> None:
    claims = claims_by_id(ROOT / "sources/claims/vendor/vendor_growatt_v124_2020.json")
    i3165 = claims["vendor_growatt_v124_2020:input:p077:i3165:visual-review"]
    assert i3165["source_kind"] == "manual_original_document_verified"
    assert i3165["page_end"] == 78
    assert i3165["raw_variable"] == "BDCDeratingMo de"
    assert i3165["reconstructed_variable"] == "BDCDeratingMode"
    assert len(i3165["source_fragments"]) == 2
    assert "22: Battery SOC" in i3165["raw_value_text"]
    i3211 = claims["vendor_growatt_v124_2020:input:p080:i3211:visual-review"]
    assert i3211["page_end"] == 81
    assert "bit8" in i3211["raw_value_text"] and "bit9" in i3211["raw_value_text"]


def test_duplicate_address_claims_remain_distinct() -> None:
    claims = json.loads((ROOT / "sources/claims/vendor/vendor_growatt_v305_2013.json").read_text())["claims"]
    address_zero = [claim for claim in claims if claim["register_table"] == "holding" and claim["parsed_address"] == 0]
    assert len(address_zero) == 1
    input_zero = [claim for claim in claims if claim["register_table"] == "input" and claim["parsed_address"] == 0]
    assert input_zero
    assert {claim["register_table"] for claim in input_zero + address_zero} == {"holding", "input"}


def test_malformed_address_is_not_coerced() -> None:
    claims = json.loads((ROOT / "sources/claims/vendor/vendor_growatt_v124_2020.json").read_text())["claims"]
    suspicious = [claim for claim in claims if "suspicious_layout_address" in claim["diagnostics"]]
    assert suspicious
    assert all(claim["parsed_address"] is None for claim in suspicious)


def test_hash_mismatch_fails(tmp_path: Path) -> None:
    path = tmp_path / "not-a-pdf.bin"
    path.write_bytes(b"not the vendor source")
    with pytest.raises(ValueError, match="SHA-256 mismatch"):
        extract_vendor_pdf.extract_document(path, "0" * 64)


def test_validator_catches_broken_continuation_and_duplicate_id(tmp_path: Path) -> None:
    source = json.loads((ROOT / "sources/claims/vendor/vendor_growatt_v124_2020.json").read_text())
    broken = copy.deepcopy(source)
    broken["claims"][0]["continuation_refs"] = ["missing-fragment"]
    broken["claims"].append(copy.deepcopy(broken["claims"][0]))
    path = tmp_path / "broken.json"
    path.write_text(json.dumps(broken))
    result = validate(path, ROOT / "sources/claims/vendor/schema.json")
    assert not result["valid"]
    assert result["duplicate_claim_ids"]
    assert any("unresolved continuation" in error for error in result["errors"])


def test_old_new_comparison_classifies_rows() -> None:
    old = json.loads((ROOT / "sources/vendor/growatt-v1.24-tables.json").read_text())
    new = json.loads((ROOT / "sources/claims/vendor/vendor_growatt_v124_2020.json").read_text())
    result = compare(old, new)
    assert result["old_rows"] == 1457
    assert result["new_claims"] >= result["old_rows"]
    assert "new_continuation_recovered" in result["classification_counts"]
