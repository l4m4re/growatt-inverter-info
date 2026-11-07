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
FIRMWARE_EVIDENCE_PATH = ROOT / "sources/evidence/zaba22-firmware-register-correlation.json"


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
    assert len(spec["source_native_blocks"]) == 24
    assert len(spec["blocks"]) == 24
    assert len(spec["registers"]) == 1667
    assert spec["metrics"]["conflicts"] == 0
    assert any(len(block["applicability_path_refs"]) > 1 for block in spec["blocks"])
    assert all("family" not in register for register in spec["registers"])
    assert register_at(spec, "holding", 30000)["canonical_name"] == "Equipment type (DTC)"
    assert register_at(spec, "holding", 30100)["canonical_name"] == "Control authority"
    assert register_at(spec, "input", 31000)["canonical_name"] == "Working state of energy storage machine"


def test_portal_battery_controls_are_published_as_holding_registers() -> None:
    spec = read_spec()

    assert register_at(spec, "holding", 3067)["canonical_name"] == "On-grid battery discharge stop SOC"
    assert register_at(spec, "holding", 3311)["datatype"]["scale"] == 0.1
    assert register_at(spec, "holding", 3312)["canonical_name"] == "Charge stop SOC from grid"
    assert not any(
        register["table"] == "input" and register["address"] in {3067, 3311, 3312}
        and register["semantic_key"] in {
            "battery.on_grid.discharge_stop_soc",
            "battery.grid_charge.power_limit",
            "battery.grid_charge.stop_soc",
        }
        for register in spec["registers"]
    )


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


def test_zaba22_direct_vpp_single_word_boundaries_are_preserved() -> None:
    evidence = json.loads(FIRMWARE_EVIDENCE_PATH.read_text(encoding="utf-8"))
    routes = {
        (route["table"], route["function_code"]): route
        for route in evidence["direct_routes"]
    }

    assert routes[("holding", 3)]["address_end"] == 30498
    assert routes[("input", 4)]["address_end"] == 31299
    assert "single-word direct coverage ends at 30498" in routes[("holding", 3)]["guard"]
    assert "single-word direct coverage ends at 31299" in routes[("input", 4)]["guard"]
    assert all(
        result["status"] == "no_address_specific_case_recovered"
        for result in evidence["post_table_case_search"]
    )

    direct = register_at(read_spec(), "holding", 30100)["evidence"]["other_evidence"]
    assert len(direct) == 1
    assert direct[0]["firmware_confidence"] == "high"
    assert direct[0]["firmware_read_status"] == ["direct_table_route"]
    assert direct[0]["firmware_resolved_byte_range"] == {
        "start": "0x2000aba4",
        "end": "0x2000aba5",
    }
    assert direct[0]["semantic_name_confidence"] == "source_correlation_only"

    unresolved = register_at(read_spec(), "holding", 32000)["evidence"]["other_evidence"]
    assert len(unresolved) == 1
    assert unresolved[0]["firmware_confidence"] == "unresolved"
    assert unresolved[0]["firmware_read_status"] == [
        "not_established_in_scoped_artifacts"
    ]


def test_every_vpp_register_retains_an_explicit_firmware_confidence() -> None:
    spec = read_spec()
    vpp_registers = [
        register
        for register in spec["registers"]
        if register["semantic_category"] == "vpp_v201"
    ]

    assert len(vpp_registers) == 180
    assert all(register["evidence"]["other_evidence"] for register in vpp_registers)
    assert all(
        item["semantic_name_confidence"] == "source_correlation_only"
        for register in vpp_registers
        for item in register["evidence"]["other_evidence"]
    )
    assert all(
        item["firmware_confidence"] in {"high", "medium", "unresolved"}
        for register in vpp_registers
        for item in register["evidence"]["other_evidence"]
    )


def test_every_legacy_register_retains_scoped_arm_confidence() -> None:
    spec = read_spec()
    legacy_registers = [
        register
        for register in spec["registers"]
        if not register["source_provenance"]["source_native_block_ref"].startswith("v124-portal-")
        and register["address"] is not None
        and register["address"] < 30000
    ]
    correlations = [
        next(
            item
            for item in register["evidence"]["other_evidence"]
            if item["kind"] == "zaba22_arm_legacy_register_correlation"
        )
        for register in legacy_registers
    ]

    assert len(correlations) == len(legacy_registers)
    assert all(
        item["semantic_name_confidence"] == "source_correlation_only"
        and len(item["source_report_sha256"]) == 64
        for item in correlations
    )
    matched = next(
        item
        for register, item in zip(legacy_registers, correlations, strict=True)
        if register["table"] == "holding" and register["address"] == 3
    )
    assert matched["firmware_confidence"] == "high_for_recovered_route"
    assert matched["matched_addresses"] == [3]
    unresolved = next(
        item
        for register, item in zip(legacy_registers, correlations, strict=True)
        if register["table"] == "input" and register["address"] == 11
    )
    assert unresolved["firmware_confidence"] == "unresolved"
    assert unresolved["firmware_read_status"] == ["provider_route_not_established"]


def test_zaba22_legacy_read_semantics_are_hash_pinned_and_conservative() -> None:
    evidence = json.loads(FIRMWARE_EVIDENCE_PATH.read_text(encoding="utf-8"))
    assert evidence["legacy_read_semantics_report_sha256"]
    semantics = evidence["legacy_read_semantics"]
    assert semantics["schema"] == "growatt-zaba22-legacy-read-semantics.v1"
    assert semantics["summary"]["row_count"] == 136
    assert semantics["summary"]["missing_documentation_rows"] == []
    assert semantics["confidence_boundary"]["not_proven"]


def test_zaba22_executable_provider_and_capture_evidence_are_pinned() -> None:
    evidence = json.loads(FIRMWARE_EVIDENCE_PATH.read_text(encoding="utf-8"))

    provider = evidence["legacy_memory_provider"]
    assert provider["schema"] == "growatt-zaba22-legacy-memory-provider.v1"
    assert provider["summary"]["row_count"] == 122
    assert provider["summary"]["row_count_by_function_code"] == {"3": 44, "4": 78}
    assert evidence["legacy_memory_provider_report_sha256"]
    compound = evidence["legacy_compound_provider"]
    assert compound["schema"] == "growatt-zaba22-legacy-compound-provider.v1"
    assert compound["summary"]["row_count"] == 1
    assert compound["rows"][0]["public_address"] == 118
    assert compound["rows"][0]["high_source_address"] == 0x2000D8CF
    assert compound["rows"][0]["low_source_address"] == 0x2000D7D8
    assert evidence["legacy_compound_provider_report_sha256"]
    transform = evidence["legacy_transform_provider"]
    assert transform["schema"] == "growatt-zaba22-legacy-transform-provider.v1"
    assert transform["summary"]["row_count"] == 74
    assert transform["summary"]["row_count_by_function_code"] == {"3": 29, "4": 45}
    assert evidence["legacy_transform_provider_report_sha256"]
    typed = evidence["legacy_typed_concat_provider"]
    assert typed["schema"] == "growatt-zaba22-legacy-typed-concat-provider.v1"
    assert typed["summary"]["row_count"] == 284
    assert typed["summary"]["row_count_by_function_code"] == {"3": 284, "4": 0}
    assert evidence["legacy_typed_concat_provider_report_sha256"]
    typed_semantics = evidence["legacy_typed_concat_semantics"]
    assert typed_semantics["schema"] == "growatt-zaba22-legacy-typed-concat-semantics.v1"
    assert typed_semantics["summary"]["documented_row_count"] == 125
    assert typed_semantics["summary"]["undocumented_row_count"] == 159
    assert evidence["legacy_typed_concat_semantics_report_sha256"]
    status_provider = evidence["fc03_10000_provider"]
    assert status_provider["schema"] == "growatt-zaba22-fc03-10000-provider.v1"
    assert status_provider["summary"]["fixed_case_count"] == 28
    assert status_provider["summary"]["default_zero_addresses"] == 98
    assert evidence["fc03_10000_provider_report_sha256"]
    linear_provider = evidence["linear_read_provider"]
    assert linear_provider["schema"] == "growatt-zaba22-linear-read-provider.v1"
    assert linear_provider["summary"] == {"case_count": 5, "word_count": 3989}
    assert evidence["linear_read_provider_report_sha256"]

    capture = evidence["capture_conformance"]
    assert capture["schema"] == "growatt-zaba22-capture-conformance-aggregate.v1"
    assert capture["aggregate_summary"]["records"] == 16653
    assert capture["aggregate_summary"]["all_three_matches"] == 16653
    assert capture["aggregate_summary"]["write_readback_matches"] == 653
    assert evidence["capture_conformance_report_sha256"]


def test_zaba22_arm_modbus_projection_keeps_vpp_and_fc20_evidence_together() -> None:
    evidence = json.loads(FIRMWARE_EVIDENCE_PATH.read_text(encoding="utf-8"))
    projection = evidence["arm_modbus_reconstruction"]

    assert projection["schema"] == "gii.zaba22.arm-modbus-reconstruction.v1"
    assert projection["vpp"]["access_matrix"]["summary"]["matrix_row_count"] == 266
    assert len(projection["vpp"]["conformance"]["rows"]) == 1586
    direct_rows = [
        row
        for row in projection["vpp"]["access_matrix"]["rows"]
        if row.get("address_start") == 30100
        and row.get("firmware_storage_pointer_target") == "0x2000aadc"
    ]
    assert direct_rows
    assert direct_rows[0]["firmware_resolved_byte_range"] == {
        "start": "0x2000aba4",
        "end": "0x2000aba5",
    }
    assert projection["vpp"]["v203_access_policy"]["summary"]["target_count"] == 32
    control = projection["vpp"]["control_register_evidence"]
    assert control["summary"] == {
        "address_count": 8,
        "alternate_pointer_alias_count": 4,
        "explicit_write_case_count": 6,
        "generic_rejection_count": 1,
        "same_direct_table_storage_count": 2,
        "write_unknown_count": 1,
    }
    control_rows = {row["public_address"]: row for row in control["rows"]}
    assert control_rows[30101]["firmware_write"]["explicit_case"][
        "validation_conditions"
    ] == "uVar15 < 2"
    assert control_rows[30474]["operation_evidence"]["wire_direction"] == (
        "read_proven_write_rejected_on_recovered_path"
    )
    assert projection["fc20"]["producer_boundary"]["producer"]["function_byte"] == "0x64 ('d')"
    assert projection["fc20"]["state_effects"]["wire_direction"]["0x20"] == "read_only"
    assert projection["operation_conformance"]["replay_summary"]["all_three_matches"] == 15670
    assert all(item["sha256"] for item in projection["source_reports"].values())


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
