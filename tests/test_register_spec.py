"""Tests for the project-independent Growatt Register Specification."""

from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

from tools.validate_min_tlxh_metadata import check as check_min_tlxh_metadata

REPO = Path(__file__).parents[1]
SPEC_DIR = REPO / "spec"
VALIDATOR_SPEC = importlib.util.spec_from_file_location(
    "growatt_register_spec_validator", REPO / "tools" / "validate_register_spec.py"
)
assert VALIDATOR_SPEC and VALIDATOR_SPEC.loader
VALIDATOR = importlib.util.module_from_spec(VALIDATOR_SPEC)
VALIDATOR_SPEC.loader.exec_module(VALIDATOR)


def load_spec() -> dict:
    """Load the generated canonical specification."""
    return json.loads((SPEC_DIR / "growatt-register-spec.json").read_text())


def test_canonical_spec_validates_and_preserves_table_identity() -> None:
    """Canonical physical identity remains family/table/address based."""
    spec = load_spec()
    VALIDATOR.validate(spec)
    records = {record["physical_id"]: record for record in spec["registers"]}

    assert (
        records["min_tl_xh:holding:3081"]["normalized"]["name"]
        == "UPS/EPS frequency selection"
    )
    assert records["min_tl_xh:input:3081"]["normalized"]["name"] == "PV4 energy total"
    assert (
        records["min_tl_xh:holding:3081"]["table"]
        != records["min_tl_xh:input:3081"]["table"]
    )


def test_known_min_tlxh_corrections_survive_regeneration() -> None:
    """The resolved MIN control and telemetry addresses remain distinct."""
    records = {record["physical_id"]: record for record in load_spec()["registers"]}

    assert records["min_tl_xh:holding:3047"]["normalized"]["name"] == (
        "Battery-first charge power rate"
    )
    assert records["min_tl_xh:holding:3048"]["normalized"]["name"] == (
        "Battery-first stop SOC"
    )
    assert records["min_tl_xh:holding:3049"]["normalized"]["name"] == (
        "AC charging enabled"
    )
    assert records["min_tl_xh:holding:3082"]["normalized"]["name"] == (
        "Load-first stop SOC"
    )
    assert records["min_tl_xh:input:3047"]["normalized"]["name"] == (
        "Inverter runtime"
    )
    assert records["min_tl_xh:input:3081"]["normalized"]["name"] == (
        "PV4 energy total"
    )


def test_min_control_review_preserves_packed_schedules_and_table_overlaps() -> None:
    """MIN controls retain scalar/packed meanings in the holding namespace."""
    records = {record["physical_id"]: record for record in load_spec()["registers"]}

    schedule = records["min_tl_xh:holding:3038"]
    assert schedule["normalized"]["unit"] is None
    assert schedule["normalized"]["raw_type"].startswith("packed u16")
    assert schedule["review"]["disposition"] == "PROVEN"
    assert records["min_tl_xh:holding:3047"]["semantic_identity"]["quantity"] == (
        "battery.first.charge.rate"
    )
    assert records["min_tl_xh:holding:3082"]["review"]["live_observation"]
    assert records["min_tl_xh:holding:3081"]["table"] != records[
        "min_tl_xh:input:3081"
    ]["table"]


def test_min_semantic_review_keeps_bms_and_warning_fields_honest() -> None:
    """BMS, inverter-warning, and diagnostic fields are not conflated."""
    records = {record["physical_id"]: record for record in load_spec()["registers"]}

    assert records["min_tl_xh:input:110"]["length_words"] == 1
    assert records["min_tl_xh:input:111"]["length_words"] == 1
    assert records["min_tl_xh:input:3111"]["semantic_identity"]["quantity"] == (
        "inverter.present_fft_value_channel_a"
    )
    assert records["min_tl_xh:input:3164"]["semantic_identity"]["quantity"] == (
        "bdc.data_separation"
    )
    assert records["min_tl_xh:input:3196"]["semantic_identity"]["quantity"] == (
        "battery.bms_max_soc"
    )
    assert records["min_tl_xh:input:3197"]["semantic_identity"]["quantity"] == (
        "battery.bms_min_soc"
    )
    assert records["min_tl_xh:input:3217"]["normalized"]["signed"] is True
    assert records["min_tl_xh:input:3217"]["normalized"]["divisor"] == 100
    assert records["min_tl_xh:input:3230"]["normalized"]["divisor"] == 1000
    assert records["min_tl_xh:input:3231"]["normalized"]["divisor"] == 1000


def test_min_status_words_preserve_vendor_packing_and_unsigned_flags() -> None:
    """Status words are represented by their documented byte/bit layout."""
    records = {record["physical_id"]: record for record in load_spec()["registers"]}

    status = records["min_tl_xh:input:3000"]
    assert status["normalized"]["signed"] is False
    assert status["enums"] == []
    assert [field["bits"] for field in status["packed_fields"]] == [[8, 15], [0, 7]]
    assert status["packed_fields"][0]["enum"]["3"] == "system_fault_module"
    assert status["packed_fields"][1].get("enum") is None

    bdc = records["min_tl_xh:input:3166"]
    assert bdc["enums"] == []
    assert bdc["packed_fields"][0]["enum"]["2"] == "discharge"
    assert bdc["packed_fields"][1]["enum"]["3"] == "flash"

    assert records["min_tl_xh:input:3187"]["normalized"]["signed"] is False
    assert records["min_tl_xh:input:3211"]["normalized"]["signed"] is False
    assert records["min_tl_xh:input:3104"]["bitfields"][0]["name"] == "turn_off_order"


def test_min_status_enums_are_explicit_and_not_parser_artifacts() -> None:
    """Vendor status enums have stable values and readable canonical names."""
    records = {record["physical_id"]: record for record in load_spec()["registers"]}

    assert [(item["value"], item["canonical_name"]) for item in records["min_tl_xh:input:3118"]["enums"]] == [
        (0, "no_bdc_connected"),
        (1, "bdc1_connected"),
        (2, "bdc2_connected"),
        (3, "bdc1_and_bdc2_connected"),
    ]
    assert records["min_tl_xh:input:3212"]["enums"][-1]["canonical_name"] == "update"
    assert records["min_tl_xh:input:3164"]["bitfields"] == []


def test_min_metadata_consistency_checker_catches_unit_collisions() -> None:
    """The bounded checker accepts canonical metadata and catches regressions."""
    spec = load_spec()
    assert check_min_tlxh_metadata(spec)["errors"] == []
    broken = deepcopy(spec)
    broken_record = next(
        record for record in broken["registers"] if record["physical_id"] == "min_tl_xh:input:3172"
    )
    broken_record["normalized"]["unit"] = "A"
    assert any(
        item["kind"] == "semantic_unit_contradiction"
        for item in check_min_tlxh_metadata(broken)["errors"]
    )
    broken_record["normalized"]["name"] = "Synthetic field"
    broken_record["normalized"]["raw_type"] = "u16 current"
    broken_record["normalized"]["unit"] = "V"
    assert any(
        item["kind"] == "datatype_unit_contradiction"
        for item in check_min_tlxh_metadata(broken)["errors"]
    )


def test_bms_and_storage_current_are_distinct_measurement_points() -> None:
    """I3170 and I3217 retain different subsystem meanings."""
    records = {record["physical_id"]: record for record in load_spec()["registers"]}
    storage = records["min_tl_xh:input:3170"]
    bms = records["min_tl_xh:input:3217"]

    assert (
        storage["semantic_identity"]["quantity"]
        == bms["semantic_identity"]["quantity"]
        == "battery.current"
    )
    assert storage["semantic_identity"]["subsystem"] == "storage_device"
    assert bms["semantic_identity"]["subsystem"] == "bms"
    assert storage["normalized"]["signed"] is False
    assert storage["normalized"]["signedness_status"] == (
        "v4_history_validated_non_negative_magnitude"
    )
    assert (
        bms["normalized"]["signedness_status"] == "regression_and_live_value_validated"
    )
    assert storage["relationships"] == []
    assert bms["relationships"] == []
    assert bms["normalized"]["divisor"] == 100


def test_native_pages_are_read_observed_not_semantically_promoted() -> None:
    """Native page evidence is separate from semantic verification."""
    spec = load_spec()
    pages = spec["native_read_evidence"]["pages"]

    assert [
        (page["function_code"], page["start"], page["count"]) for page in pages
    ] == [
        (3, 0, 125),
        (3, 3000, 125),
        (4, 3000, 125),
        (4, 3125, 125),
        (4, 3250, 125),
    ]
    assert all(page["hardware_validation"]["repetitions"] == 2 for page in pages)
    assert all(
        evidence["level"] != "semantic_verified"
        for record in spec["registers"]
        for evidence in record["evidence"]
    )


def test_canonical_coverage_exposes_structures_and_enums() -> None:
    """Coverage reports the remaining normalization work explicitly."""
    coverage = load_spec()["coverage"]

    assert coverage["normalized_percentage"] > 80
    assert coverage["logical_multi_register_fields"] > 0
    assert coverage["indexed_structures"] > 0
    assert coverage["enum_bearing_records"] > 0
    assert coverage["bitfield_bearing_records"] > 0
    assert coverage["component_as_alternate_errors_found"] == 2096
    assert coverage["component_as_alternate_relationships_removed"] == 2096
    assert load_spec()["correction_audit"]["component_as_alternate_relationships"]["remaining"] == 0


def test_runtime_audit_reports_occurrences_and_unique_findings() -> None:
    """The derived HA audit keeps repeated runtime mappings distinguishable."""
    audit = load_spec()["derived_views"]["ha_runtime_audit"]

    assert audit["mapping_occurrences_checked"] == 274
    assert audit["unique_family_table_address_mappings"] == 206
    assert audit["unique_family_table_address_issue_findings"] == 22
    assert audit["finding_occurrences"] == 24
    assert audit["unique_findings"] == 22
    assert set(audit["finding_kinds"]) == {
        "length_mismatch",
        "signedness_mismatch",
    }


def test_known_min_high_low_pairs_are_logical_fields_not_alternates() -> None:
    """Vendor H/L words belong to one complete logical measurement."""
    spec = load_spec()
    records = {record["physical_id"]: record for record in spec["registers"]}
    expected = {
        3125: "battery.discharge_energy_today",
        3127: "battery.discharge_energy_total",
        3129: "battery.charge_energy_today",
        3131: "battery.charge_energy_total",
        3133: "battery.ac_charge_energy_today",
        3135: "battery.ac_charge_energy_total",
    }
    for start, quantity in expected.items():
        high = records[f"min_tl_xh:input:{start}"]
        low = records[f"min_tl_xh:input:{start + 1}"]
        assert high["component_role"] == "high_word"
        assert low["component_role"] == "low_word"
        assert high["component_of"] == low["component_of"]
        field = next(field for field in spec["logical_fields"] if field["id"] == high["component_of"])
        assert field["semantic_key"] == quantity
        assert field["length_words"] == 2
        assert field["word_order"] == "high_low"
        assert high["relationships"] == low["relationships"] == []
        assert all(
            relationship["target"] not in {high["physical_id"], low["physical_id"]}
            for relationship in field["relationships"]
        )


def test_min_canonical_units_and_physical_lengths_are_consistent() -> None:
    """Corrected units stay separate from logical field length metadata."""
    spec = load_spec()
    records = {record["physical_id"]: record for record in spec["registers"]}
    assert records["min_tl_xh:input:3172"]["normalized"]["unit"] == "V"
    assert records["min_tl_xh:input:3173"]["normalized"]["unit"] == "V"
    assert records["min_tl_xh:input:3172"]["normalized"]["signed"] is False
    assert records["min_tl_xh:input:3173"]["normalized"]["signed"] is False
    assert records["min_tl_xh:input:3217"]["normalized"]["unit"] == "A"
    assert records["min_tl_xh:input:3230"]["normalized"]["unit"] == "V"
    assert records["min_tl_xh:input:3231"]["normalized"]["unit"] == "V"
    assert records["min_tl_xh:holding:3038"]["normalized"]["unit"] is None
    assert records["min_tl_xh:holding:3050"]["normalized"]["unit"] is None
    for address in (3047, 3048, 3081, 3082, 3178, 3179, 3180, 3181):
        assert records[f"min_tl_xh:input:{address}"]["length_words"] == 1


def test_representative_family_components_and_legacy_identity() -> None:
    """Three-phase and storage families use the same component discipline."""
    spec = load_spec()
    records = {record["physical_id"]: record for record in spec["registers"]}
    for family in ("tl3_max_mid_mac", "storage_mix", "storage_spa", "storage_sph"):
        first = records[f"{family}:input:{40 if family == 'tl3_max_mid_mac' else 1009}"]
        second = records[f"{family}:input:{41 if family == 'tl3_max_mid_mac' else 1010}"]
        assert first["component_of"] == second["component_of"]
        assert first["relationships"] == second["relationships"] == []
    legacy = records["legacy_inverter_315:input:28"]
    assert legacy["physical_id"] == "legacy_inverter_315:input:28"
    assert legacy["relationships"] == []


def test_vendor_bitfields_packed_fields_and_placeholders_are_distinguished() -> None:
    """Explicit V1.24 bit layouts are structured; generic flags remain placeholders."""
    records = {record["physical_id"]: record for record in load_spec()["registers"]}
    h1 = records["min_tl_xh:holding:1"]["bitfields"]
    bdc = records["min_tl_xh:input:3187"]["bitfields"]
    request = records["min_tl_xh:input:3211"]["bitfields"]
    assert len(h1) == 12
    assert {item["name"] for item in h1} >= {"spi_enable", "split_phase_enable", "reserved"}
    assert {item["bits"][0] for item in bdc} >= {0, 1, 8, 12}
    assert {item["bits"][0] for item in request} >= {0, 1, 2, 8, 9}
    assert records["min_tl_xh:holding:3221"]["packed_fields"]
    placeholders = [
        item
        for record in records.values()
        for item in record["bitfields"]
        if item["status"] == "placeholder"
    ]
    assert placeholders
    assert all(item["name"] == "undocumented_flags" for item in placeholders)


def test_semantic_reconciliation_and_single_canonical_truth() -> None:
    """Curated aliases reconcile without making the compatibility view canonical."""
    spec = load_spec()
    records = {record["physical_id"]: record for record in spec["registers"]}
    assert records["storage_mix:holding:1048"]["semantic_identity"]["quantity"] == "battery.type"
    assert records["storage_mix:holding:3070"]["semantic_identity"]["quantity"] == "battery.type"
    assert not any("battery.battery" in key or "_typ_e" in key for key in spec["semantic_index"])
    assert spec["coverage"]["semantic_reconciled_records"] < spec["coverage"]["semantic_key_assigned_records"]
    compatibility = json.loads((REPO / "knowledge/compatibility/growatt-register-reference.json").read_text())
    assert spec["specification"]["canonical_truth"] is True
    assert compatibility["meta"]["canonical"] is False
    assert compatibility["meta"]["generated_compatibility_view"] is True


def test_write_risk_and_human_family_names() -> None:
    """Underspecified writes are not advertised as safe experiments."""
    spec = load_spec()
    assert spec["coverage"]["reversible_candidate_records"] == 0
    assert spec["coverage"]["unknown_write_risk_records"] > 0
    family_text = (SPEC_DIR / "families" / "MIN_TL_XH.md").read_text()
    assert "| T | Addr | Canonical name |" in family_text
    assert "Battery charge energy today (high word)" in family_text


def test_generated_human_docs_persist_and_regenerate_deterministically() -> None:
    """All Markdown release outputs survive two generator executions unchanged."""
    expected = [
        SPEC_DIR / "README.md",
        SPEC_DIR / "PROTOCOLS.md",
        SPEC_DIR / "SEMANTIC_INDEX.md",
        *(SPEC_DIR / "families" / name for name in (
            "MIN_TL_XH.md", "TL3_MAX_MID_MAC.md", "MOD_TL3_XH.md", "MIX.md",
            "SPA.md", "SPH.md", "LEGACY_315.md", "SPF.md",
        )),
        SPEC_DIR / "growatt-register-spec.json",
        SPEC_DIR / "growatt-register-spec.schema.json",
    ]
    before = {path: hashlib.sha256(path.read_bytes()).digest() for path in expected}
    subprocess.run([sys.executable, "tools/build_register_spec.py"], cwd=REPO, check=True)
    subprocess.run([sys.executable, "tools/build_register_spec.py"], cwd=REPO, check=True)
    assert all(path.is_file() for path in expected)
    assert before == {path: hashlib.sha256(path.read_bytes()).digest() for path in expected}
