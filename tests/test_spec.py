from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from tools.build_spec import build_model, generate, render, structured_dedup_counts
from tools.validate_spec import validate


ROOT = Path(__file__).resolve().parents[1]
SPEC_PATH = ROOT / "spec/growatt-register-spec.json"
MARKDOWN_PATH = ROOT / "spec/growatt-register-spec.md"


def read_spec(path: Path = SPEC_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def register_at(spec: dict[str, Any], table: str, address: int) -> dict[str, Any]:
    return next(
        register
        for register in spec["registers"]
        if register["table"] == table and register["address"] == address
    )


def test_product_schema_and_structural_invariants() -> None:
    spec = read_spec()

    assert validate(spec) == []
    assert len(spec["source_native_blocks"]) == 15
    assert len(spec["blocks"]) == 15
    assert len(spec["registers"]) == 1484
    assert spec["metrics"]["conflicts"] == 0
    assert any(len(block["applicability_path_refs"]) > 1 for block in spec["blocks"])
    assert all("family" not in register for register in spec["registers"])


def test_reserved_ranges_stay_compact_and_do_not_overlap_registers() -> None:
    spec = read_spec()
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")
    ranges = {(item["table"], item["start"], item["end"]) for item in spec["reserved_ranges"]}

    assert ranges == {("holding", 3115, 3124), ("input", 3281, 3374)}
    assert "H3115–H3124" in markdown
    assert "I3281–I3374" in markdown
    assert not any(
        register["table"] == table
        and register["address"] is not None
        and register["address"] <= end
        and (register.get("address_end") or register["address"]) >= start
        for table, start, end in ranges
        for register in spec["registers"]
    )
    assert not any(item["table"] == "input" and item["start"] <= 3280 <= item["end"] for item in spec["reserved_ranges"])


def test_reviewed_access_defaults_and_bdc_bms_fields_survive() -> None:
    spec = read_spec()

    for table, address in (("holding", 122), ("holding", 123), ("holding", 1002), ("holding", 1003)):
        assert register_at(spec, table, address)["access"] == "read_write"

    h1003 = register_at(spec, "holding", 1003)
    assert h1003["evidence"]["vendor_claim"]["access_raw"] == "W"
    assert h1003["access"] == "read_write"

    h3085 = register_at(spec, "holding", 3085)
    assert h3085["default"] == 1
    assert h3085["access"] == "read_write"
    assert h3085["range_raw"] == "1..254"
    assert "BDC/BMS RS485 communication address" == h3085["canonical_name"]

    h3086 = register_at(spec, "holding", 3086)
    enum_values = {
        item["value"]: item["vendor_label"]
        for group in h3086["datatype"]["structured"]
        for item in group["enums"]
    }
    assert enum_values[0] == "9600bps"
    assert enum_values[1] == "38400bps register value None"


def test_single_markdown_projection_covers_blocks_registers_and_logical_fields() -> None:
    spec = read_spec()
    markdown = MARKDOWN_PATH.read_text(encoding="utf-8")

    assert render(spec) == markdown
    assert "## Holding registers" in markdown
    assert "## Input registers" in markdown
    assert "### US Machine type Time Set" in markdown
    assert "TL-XH US; MIN 6000TL-XH" in markdown
    assert "(TL-XH; MIN 6000TL-XH)" in markdown
    assert "H3036" in markdown
    assert "H3037" in markdown
    assert "H3038" in markdown
    assert "H3047" in markdown
    assert "H3048" in markdown
    assert "H3049" in markdown
    assert "H3050" in markdown
    assert "H3082" in markdown
    assert "default 1; 1..254" in markdown
    assert "Us Tou Month Groups" in markdown
    assert "unknown_word_order" in markdown


def test_uniform_block_omits_register_scope_column() -> None:
    spec = read_spec()
    markdown = render(spec)
    first_block = next(
        block
        for block in spec["blocks"]
        if block["table"] == "holding" and block["address_start"] == 0
    )
    heading = f"### {first_block['vendor_heading_raw']}"
    block_markdown = markdown.split(heading, 1)[1].split("\n<a id=", 1)[0]

    assert "| Scope |" not in block_markdown
    assert "| Range / default | Status |" in block_markdown


def test_register_scope_exception_is_shown_only_in_its_block() -> None:
    spec = deepcopy(read_spec())
    first_block = next(
        block
        for block in spec["blocks"]
        if block["table"] == "holding" and block["address_start"] == 0
    )
    first_register_id = first_block["register_ids"][0]
    next(
        register
        for register in spec["registers"]
        if register["register_id"] == first_register_id
    )["applicability_path_refs"] = []

    markdown = render(spec)
    heading = f"### {first_block['vendor_heading_raw']}"
    block_markdown = markdown.split(heading, 1)[1].split("\n<a id=", 1)[0]

    assert "| Range / default | Scope | Status |" in block_markdown
    assert "| H0 | Inverter enable flags |" in block_markdown
    assert "| Declared range only |" in block_markdown


def test_structured_definitions_collapse_duplicates_and_keep_variants() -> None:
    spec = read_spec()
    markdown = render(spec)
    h122 = markdown.split("#### H122 — Enum values", 1)[1].split("\n#### ", 1)[0]
    h3039 = markdown.split("#### H3039 — Enum values", 1)[1].split("\n#### ", 1)[0]
    h3038_bits = markdown.split("#### H3038 — Bitfields", 1)[1].split("\n#### ", 1)[0]

    assert h122.count("| 0 | DisableexportLimit | disableexportlimit | No |") == 1
    assert "Applies to" not in h122
    assert (
        "| H122 | Export limit enable mode | ExportLimitenable | read_write | register value | — | — | /W 1/0 | ENRICHED |"
        in markdown
    )
    assert "| Applies to |" in h3039
    assert "reserved / reserved register value None" in h3039
    assert h3038_bits.count("| 0, 7 | minutes | minutes | minutes | structured |") == 1

    assert structured_dedup_counts(spec) == {
        "enums": 277,
        "bitfields": 42,
        "packed_fields": 0,
    }


def test_clean_build_is_deterministic() -> None:
    with TemporaryDirectory() as temporary_directory:
        output = Path(temporary_directory)
        generated = generate(output=output)

        generated_json = output / "growatt-register-spec.json"
        assert json.loads(generated_json.read_text(encoding="utf-8")) == read_spec()
        assert generated_json.read_bytes() == SPEC_PATH.read_bytes()
        assert (output / "growatt-register-spec.md").read_text(encoding="utf-8") == MARKDOWN_PATH.read_text(encoding="utf-8")
        assert json.dumps(generated, sort_keys=True) == json.dumps(build_model(), sort_keys=True)
