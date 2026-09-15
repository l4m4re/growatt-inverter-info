from __future__ import annotations

import hashlib
import json
from pathlib import Path

from tools.build_register_spec_v2 import build_model, render
from tools.validate_register_spec_v2 import validate


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec/v2/register-spec-v2.json"


def test_v2_product_validates_and_preserves_frozen_canonical() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))

    assert validate(spec) == []
    assert spec["canonical_legacy_sha256"] == "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
    assert hashlib.sha256((ROOT / "spec/growatt-register-spec.json").read_bytes()).hexdigest() == spec["canonical_legacy_sha256"]


def test_v2_has_shared_block_definitions_and_reserved_ranges() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    shared = [block for block in spec["blocks"] if len(block["applicability_path_refs"]) > 1]

    assert shared
    assert len(spec["registers"]) == len({register["register_id"] for register in spec["registers"]})
    assert {tuple((item["table"], item["start"], item["end"])) for item in spec["reserved_ranges"]} >= {
        ("holding", 3115, 3124),
        ("input", 3281, 3374),
    }
    assert not any(item["table"] == "input" and item["start"] <= 3280 <= item["end"] for item in spec["reserved_ranges"])


def test_v2_representative_machine_and_human_projection_agree() -> None:
    spec = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    files = render(spec)
    block = next(item for item in spec["blocks"] if item["block_id"].startswith("cb-input-p070"))
    register = next(item for item in spec["registers"] if item["register_id"] == block["register_ids"][0])

    block_markdown = files[f"blocks/{block['block_id']}.md"]
    assert block["block_id"] in block_markdown
    assert str(register["address"]) in block_markdown
    assert "I3281-3374" not in block_markdown
    assert "input:3281-3374" in files["BLOCK_INDEX.md"]


def test_v2_generation_is_deterministic() -> None:
    first = build_model(ROOT)
    second = build_model(ROOT)

    assert json.dumps(first, ensure_ascii=False, sort_keys=True) == json.dumps(second, ensure_ascii=False, sort_keys=True)
    assert render(first) == render(second)
