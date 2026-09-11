#!/usr/bin/env python3
"""Reconcile a public Home Assistant register snapshot with the GII spec."""

# ruff: noqa: T201

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[1]
DEFAULT_SPEC = REPO / "spec" / "growatt-register-spec.json"

GROUP_LAYOUT = {
    ("tlx", "holding_common"): ("min_tl_xh", "holding", "custom_components/growatt_local/API/device_type/inverter_120.py"),
    ("tlx", "input_common"): ("min_tl_xh", "input", "custom_components/growatt_local/API/device_type/inverter_120.py"),
    ("tlx", "input_tl_xh"): ("min_tl_xh", "input", "custom_components/growatt_local/API/device_type/inverter_120.py"),
    ("storage", "holding_common"): ("storage_mix", "holding", "custom_components/growatt_local/API/device_type/storage_120.py"),
    ("storage", "holding_tl_xh"): ("min_tl_xh", "holding", "custom_components/growatt_local/API/device_type/storage_120.py"),
    ("storage", "input_common"): ("storage_mix", "input", "custom_components/growatt_local/API/device_type/storage_120.py"),
    ("storage", "input_tl_xh"): ("min_tl_xh", "input", "custom_components/growatt_local/API/device_type/storage_120.py"),
}

HA_SEMANTIC_ALIASES = {
    "status_code": {"inverter.status"},
    "input_power": {"pv.total_power"},
    "output_power": {"telemetry.ac_output_power"},
    "output_energy_today": {"telemetry.output_energy_today", "telemetry.ac_energy_today"},
    "output_energy_total": {"telemetry.output_energy_total"},
    "input_energy_total": {"telemetry.pv_energy_total"},
    "operation_hours": {"inverter.runtime"},
    "grid_frequency": {"grid.frequency"},
    "real_output_power_percent": {"telemetry.output_power_percentage"},
    "derating_mode": {"diagnostic.derating_mode"},
    "fault_code": {"diagnostic.fault_code"},
    "warning_code": {"inverter.warning_flags", "inverter.warning_flags_high"},
    "present_fft_a": {"inverter.present_fft_value_channel_a"},
    "output_reactive_power": {"telemetry.output_reactive_power"},
    "output_reactive_energy_total": {"telemetry.reactive_energy_total"},
    "power_to_user": {"grid.import_power"},
    "power_to_grid": {"grid.export_power"},
    "power_user_load": {"load.house_power"},
    "energy_to_user_today": {"telemetry.load_energy_today"},
    "energy_to_user_total": {"telemetry.load_energy_total"},
    "energy_to_grid_today": {"grid.export_energy_today"},
    "energy_to_grid_total": {"grid.export_energy_total"},
    "discharge_power": {"battery.discharge_power"},
    "charge_power": {"battery.charge_power"},
    "discharge_energy_today": {"battery.discharge_energy_today"},
    "discharge_energy_total": {"battery.discharge_energy_total"},
    "charge_energy_today": {"battery.charge_energy_today"},
    "charge_energy_total": {"battery.charge_energy_total"},
    "bdc_new_flag": {"bdc.data_separation"},
    "battery_voltage": {"battery.voltage"},
    "battery_current": {"battery.current"},
    "vbus1_voltage": {"telemetry.vbus1_voltage"},
    "vbus2_voltage": {"telemetry.vbus2_voltage"},
    "buck_boost_current": {"telemetry.buck_boost_current"},
    "llc_current": {"telemetry.llc_stage_current"},
    "battery_temperature_a": {"diagnostic.battery_temperature_a"},
    "battery_temperature_b": {"diagnostic.battery_temperature_b"},
    "comm_board_temperature": {"diagnostic.communication_board_temperature"},
    "bms_max_volt_cell_no": {"battery.bms_max_cell_index"},
    "bms_min_volt_cell_no": {"battery.bms_min_cell_index"},
    "bms_avg_temp_a": {"diagnostic.bms_average_temperature_channel_a"},
    "bms_max_cell_temp_a": {"diagnostic.bms_max_cell_temperature_a"},
    "bms_avg_temp_b": {"diagnostic.bms_average_temperature_b"},
    "bms_max_cell_temp_b": {"diagnostic.bms_max_cell_temperature_channel_b"},
    "bms_avg_temp_c": {"diagnostic.bms_average_temperature_channel_c"},
    "bms_max_soc": {"battery.bms_max_soc"},
    "bms_min_soc": {"battery.bms_min_soc"},
    "parallel_battery_num": {"battery.parallel_battery_count"},
    "bms_derate_reason": {"control.bms_derate_reason"},
    "bms_gauge_fcc_ah": {"battery.bms_full_charge_capacity"},
    "bms_gauge_rm_ah": {"battery.bms_remaining_capacity"},
    "bms_protect1": {"battery.bms_protect_flags_1"},
    "bms_warn1": {"diagnostic.bms_warning_flags_1"},
    "bms_fault1": {"diagnostic.bms_fault_flags_1"},
    "bms_fault2": {"diagnostic.bms_fault_flags_2"},
    "bat_iso_status": {"diagnostic.battery_insulation_status"},
    "batt_request_flags": {"battery.request_flags"},
    "bms_status": {"diagnostic.bms_status"},
    "bms_protect2": {"battery.bms_protect_flags_2"},
    "bms_warn2": {"diagnostic.bms_warning_flags_2"},
    "bms_soc": {"battery.soc"},
    "bms_battery_voltage": {"battery.voltage"},
    "bms_battery_current": {"battery.current"},
    "bms_cell_max_temp": {"diagnostic.bms_max_cell_temperature"},
    "bms_max_charge_current": {"battery.bms_max_charge_current"},
    "bms_max_discharge_current": {"battery.bms_max_discharge_current"},
    "bms_cycle_count": {"battery.bms_cycle_count"},
    "bms_soh": {"battery.bms_soh"},
    "bms_charge_volt_limit": {"battery.bms_charge_voltage_limit"},
    "bms_discharge_volt_limit": {"battery.bms_discharge_voltage_limit"},
    "bms_warn3": {"diagnostic.bms_warning_flags_3"},
    "bms_protect3": {"battery.bms_protect_flags_3"},
    "bms_cell_volt_max": {"battery.bms_max_cell_voltage"},
    "bms_cell_volt_min": {"battery.bms_min_cell_voltage"},
    "inverter_enabled": {"control.inverter_enabled", "control.inverter_enable_flags"},
    "output_power_limit": {"control.active_power_limit_setpoint"},
    "serial number": {"control.serial_number", "field.inverter_serial_number"},
    "Inverter model": {"field.inverter_model"},
    "device type code": {"field.device_type_code"},
    "number of trackers and phases": {"field.trackers_and_phases", "field.number_of_trackers_and_phases"},
    "modbus version": {"field.modbus_version"},
    "ac_charge_enabled": {"ac.charge.enabled"},
    "current_priority": {"field.priority_mode"},
}


def iter_mappings(snapshot: dict[str, Any]) -> Iterable[dict[str, Any]]:
    for device, groups in snapshot["devices"].items():
        for group, entries in groups.items():
            layout = GROUP_LAYOUT.get((device, group))
            if layout is None:
                continue
            family, table, source_file = layout
            for entry in entries:
                yield {
                    "device": device,
                    "group": group,
                    "family": family,
                    "table": table,
                    "source_file": source_file,
                    **entry,
                }


def sensor_descriptors(snapshot: dict[str, Any], device: str) -> dict[str, dict[str, Any]]:
    names = ("storage",) if device == "storage" else ("inverter", "storage")
    result: dict[str, dict[str, Any]] = {}
    for category in names:
        for descriptor in snapshot["metadata"]["sensor_types"].get(category, []):
            result.setdefault(descriptor["key"], descriptor)
    return result


def effective_decoder(
    entry: dict[str, Any], decoder_behavior: str = "legacy"
) -> dict[str, Any]:
    value_type = entry["value_type"]
    length = entry["length"]
    signed = bool(entry.get("signed", False))
    if value_type == "float" and length == 2:
        datatype = "s32" if decoder_behavior == "legacy" or signed else "u32"
        return {"datatype": datatype, "signed": datatype == "s32", "scale": entry["scale"]}
    if value_type == "float":
        return {"datatype": "s16" if signed else "u16", "signed": signed, "scale": entry["scale"]}
    if value_type == "int":
        return {"datatype": "s16" if signed else "u16", "signed": signed, "scale": None}
    if value_type == "str":
        return {"datatype": "string", "signed": None, "scale": None}
    return {"datatype": "custom_function", "signed": None, "scale": None}


def normalized_unit(unit: str | None) -> str | None:
    """Normalize the scale notation used by some Growatt source rows."""
    if unit is None:
        return None
    match = re.fullmatch(r"(?:\d+(?:[.,]\d+)?\s*)?(V|A|W|kW|Wh|kWh|var|kvarh|Hz|°C|Ah|%)", unit.strip())
    return match.group(1) if match else unit


def semantic_match(name: str, canonical_key: str | None) -> bool | None:
    if canonical_key is None:
        return None
    if canonical_key in HA_SEMANTIC_ALIASES.get(name, set()):
        return True
    if name in {"firmware", "soc", "inverter_temperature", "ipm_temperature", "boost_temperature", "p_bus_voltage", "n_bus_voltage", "grid_frequency", "inv_start_delay"}:
        return canonical_key in {
            "field.firmware", "battery.soc", "diagnostic.inverter_temperature",
            "diagnostic.ipm_temperature", "diagnostic.boost_temperature",
            "telemetry.p_bus_voltage", "telemetry.n_bus_voltage", "grid.frequency",
            "field.inverter_start_delay",
        }
    match = re.fullmatch(r"input_(\d+)_(voltage|amperage|power|energy_today|energy_total)", name)
    if match:
        index, quantity = match.groups()
        if quantity == "voltage":
            return canonical_key in {f"telemetry.pv{index}_dc_voltage", f"telemetry.pv{index}_voltage"}
        if quantity == "amperage":
            return canonical_key in {f"telemetry.pv{index}_dc_current", f"telemetry.pv{index}_current"}
        if quantity == "power":
            return canonical_key in {"pv.total_power", f"telemetry.pv{index}_power", f"telemetry.pv{index}_dc_power"}
        return canonical_key in {f"telemetry.pv{index}_{quantity}"}
    match = re.fullmatch(r"output_(\d+)_(voltage|amperage|power)", name)
    if match:
        index, quantity = match.groups()
        phase = {"1": "l1", "2": "l2", "3": "l3"}[index]
        suffix = {"voltage": "voltage", "amperage": "current", "power": "power"}[quantity]
        return canonical_key in {f"telemetry.ac_phase_{phase}_{suffix}", f"ac.phase.{phase}_{suffix}"}
    if name.startswith("xh_schedule_"):
        return canonical_key.startswith(("grid.first.schedule.", "battery.first.schedule."))
    return name.replace(" ", "_").replace("-", "_") == canonical_key.replace(".", "_")


def continuity_risk(canonical: dict[str, Any], mismatch: str) -> str:
    key = canonical.get("semantic_key") or ""
    if mismatch in {"SIGNEDNESS_MISMATCH", "SCALE_MISMATCH", "LENGTH_MISMATCH"}:
        if "energy" in key or canonical.get("unit") == "kWh":
            return "COUNTER_CONTINUITY_RISK"
        if mismatch == "SIGNEDNESS_MISMATCH":
            return "VALUE_SIGN_CHANGE"
        return "VALUE_SCALE_CHANGE"
    if mismatch == "UNIT_MISMATCH":
        return "ENTITY_METADATA_ONLY"
    if mismatch == "SEMANTIC_MISMATCH":
        return "SEMANTIC_CHANGE"
    return "NONE"


def compare(
    mapping: dict[str, Any],
    canonical: dict[str, Any] | None,
    descriptor: dict[str, Any] | None,
    logical_fields: list[dict[str, Any]],
    decoder_behavior: str = "legacy",
) -> dict[str, Any]:
    ha_decoder = effective_decoder(mapping, decoder_behavior)
    result: dict[str, Any] = {
        "canonical_physical_id": canonical["physical_id"] if canonical else f"{mapping['family']}:{mapping['table']}:{mapping['register']}",
        "table": mapping["table"],
        "address": mapping["register"],
        "ha": {
            "device": mapping["device"],
            "group": mapping["group"],
            "source_file": mapping["source_file"],
            "field": mapping["name"],
            "read_length_words": mapping["length"],
            "value_type": mapping["value_type"],
            "decoder_datatype": ha_decoder["datatype"],
            "decoder_signed": ha_decoder["signed"],
            "scale": mapping["scale"],
            "read_write": mapping["read_write"],
            "function": mapping["function_path"],
            "entity": descriptor,
            "unique_id_template": "growatt_local_<config_serial>_<field_key>" if descriptor else None,
        },
        "canonical": None,
        "mismatch_classification": "UNSUPPORTED_OR_RESERVED",
        "required_action": "DO_NOT_EXPOSE_YET",
        "continuity_risk": "NONE",
        "notes": [],
    }
    if canonical is None:
        result["notes"].append("No canonical family/table/address record was found.")
        return result

    normalized = canonical["normalized"]
    semantic_key = canonical["semantic_identity"].get("quantity")
    logical_length = None
    if canonical.get("logical_field_id"):
        logical = next(field for field in logical_fields if field["id"] == canonical["logical_field_id"])
        logical_length = logical.get("length_words")
    result["canonical"] = {
        "family": canonical["family"],
        "semantic_key": semantic_key,
        "name": normalized.get("name"),
        "datatype": normalized.get("raw_type"),
        "signed": normalized.get("signed"),
        "scale": normalized.get("divisor"),
        "unit": normalized.get("unit"),
        "physical_length_words": canonical["length_words"],
        "logical_length_words": logical_length,
        "access": normalized.get("access"),
        "resolution": canonical.get("resolution"),
        "evidence": canonical.get("evidence"),
    }

    # The canonical physical word is one word even when an automatically
    # grouped logical field is present. A current HA multiword declaration is
    # accepted when it starts a contiguous canonical logical field; this keeps
    # the comparison aligned with the existing GII runtime audit while still
    # flagging I3110's unsupported two-word read.
    expected_length = canonical["length_words"]
    if mapping["value_type"] != "str" and mapping["length"] > 1 and logical_length:
        expected_length = logical_length
    if mapping["value_type"] == "str":
        expected_length = mapping["length"]
    if mapping["length"] != expected_length:
        result["mismatch_classification"] = "LENGTH_MISMATCH"
        result["required_action"] = "DECODE_FIX_REQUIRED"
        result["notes"].append("HA read length differs from the canonical physical/logical length.")
    elif ha_decoder["signed"] is not None and bool(normalized.get("signed", False)) != ha_decoder["signed"]:
        result["mismatch_classification"] = "SIGNEDNESS_MISMATCH"
        result["required_action"] = "DECODE_FIX_REQUIRED"
        result["notes"].append("HA's effective decoder signedness differs from canonical signedness.")
    elif mapping["value_type"] == "float" and normalized.get("divisor") is not None and mapping["scale"] != normalized["divisor"]:
        result["mismatch_classification"] = "SCALE_MISMATCH"
        result["required_action"] = "DECODE_FIX_REQUIRED"
        result["notes"].append("HA numeric scale differs from canonical divisor.")
    elif mapping["value_type"] == "float" and normalized.get("divisor") is None:
        result["mismatch_classification"] = "NEEDS_LIVE_VALIDATION"
        result["required_action"] = "NEEDS_MORE_EVIDENCE"
        result["notes"].append("Canonical scale is unresolved; HA's current scale is recorded but not endorsed.")
    else:
        match = semantic_match(mapping["name"], semantic_key)
        if match is False and semantic_key is not None:
            result["mismatch_classification"] = "SEMANTIC_MISMATCH"
            result["required_action"] = "GII_FOLLOW_UP_REQUIRED"
            result["notes"].append("The current HA field name is not an established alias of the canonical semantic key.")
        elif descriptor and normalized_unit(descriptor.get("native_unit_of_measurement")) not in (None, normalized_unit(normalized.get("unit"))):
            result["mismatch_classification"] = "UNIT_MISMATCH"
            result["required_action"] = (
                "GII_FOLLOW_UP_REQUIRED"
                if normalized_unit(normalized.get("unit")) not in {"V", "A", "W", "kW", "VA", "var", "Wh", "kWh", "Hz", "°C", "Ah", "%"}
                else "SAFE_METADATA_FIX"
            )
            result["notes"].append("HA entity unit differs from canonical engineering unit.")
        else:
            result["mismatch_classification"] = "MATCH"
            result["required_action"] = "NO_HA_CHANGE"
    result["continuity_risk"] = continuity_risk(result["canonical"], result["mismatch_classification"])
    return result


def build_audit(
    spec: dict[str, Any],
    snapshot: dict[str, Any],
    consumer_commit: str,
    decoder_behavior: str = "legacy",
) -> dict[str, Any]:
    records = {
        (record["family"], record["table"], record["address"]): record
        for record in spec["registers"]
    }
    mappings = list(iter_mappings(snapshot))
    comparisons = []
    for mapping in mappings:
        descriptor = sensor_descriptors(snapshot, mapping["device"]).get(mapping["name"])
        canonical = records.get((mapping["family"], mapping["table"], mapping["register"]))
        comparisons.append(
            compare(
                mapping,
                canonical,
                descriptor,
                spec["logical_fields"],
                decoder_behavior,
            )
        )

    by_physical: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in comparisons:
        by_physical[item["canonical_physical_id"]].append(item)
    findings = []
    for physical_id, items in sorted(by_physical.items()):
        nonmatches = [item for item in items if item["mismatch_classification"] != "MATCH"]
        if not nonmatches:
            continue
        primary = nonmatches[0]
        findings.append(
            {
                **primary,
                "occurrences": [
                    {
                        "device": item["ha"]["device"],
                        "group": item["ha"]["group"],
                        "field": item["ha"]["field"],
                    }
                    for item in items
                ],
                "secondary_classifications": sorted(
                    {item["mismatch_classification"] for item in nonmatches[1:]}
                ),
            }
        )

    existing_by_id: dict[str, dict[str, Any]] = {}
    for finding in spec["derived_views"]["ha_runtime_audit"]["findings"]:
        physical_id = finding["reference_id"].removeprefix("register:")
        item = existing_by_id.setdefault(
            physical_id,
            {
                "physical_id": physical_id,
                "family": finding["family"],
                "table": finding["table"],
                "address": finding["address"],
                "issue_kinds": set(),
                "occurrences": [],
                "audit_status": "reviewed_in_this_reconciliation",
            },
        )
        item["issue_kinds"].update(issue["kind"] for issue in finding["issues"])
        item["occurrences"].append(
            {"device": finding["device"], "group": finding["group"], "field": finding["runtime_name"]}
        )
    existing = []
    for item in existing_by_id.values():
        item["issue_kinds"] = sorted(item["issue_kinds"])
        existing.append(item)
    existing.sort(key=lambda item: item["physical_id"])

    mismatch_counts = Counter(item["mismatch_classification"] for item in comparisons)
    action_counts = Counter(item["required_action"] for item in comparisons)
    unique_ids = {item["canonical_physical_id"] for item in comparisons}
    return {
        "schema_version": 1,
        "audit": "HA-GII-1 read-side reconciliation",
        "canonical": {"spec": "spec/growatt-register-spec.json", "commit": spec["specification"].get("source_commit", "4296c596091bc118c953c69c39b8d625107fb083")},
        "consumer": {"source": snapshot.get("source"), "commit": consumer_commit},
        "decoder_behavior": decoder_behavior,
        "scope": {
            "families": ["min_tl_xh", "storage_mix"],
            "tables": ["holding", "input"],
            "source_snapshot_is_temporary": True,
            "private_runtime_state_excluded": True,
        },
        "summary": {
            "mapping_occurrences_checked": len(comparisons),
            "unique_family_table_address_mappings": len(unique_ids),
            "findings": len(findings),
            "existing_gii_runtime_findings": len(existing),
            "mismatch_classification_counts": dict(sorted(mismatch_counts.items())),
            "required_action_counts": dict(sorted(action_counts.items())),
        },
        "existing_gii_runtime_findings": existing,
        "findings": findings,
        "mappings": comparisons,
        "gii2a_correction_impact": {
            "I3021": "HA exposes reactive wattage with W metadata; canonical meaning is reactive power in var: future metadata fix required.",
            "I3071_I3074": "HA field names are retained energy-to-grid aliases; decoder signedness remains a current finding and energy continuity must be protected.",
            "I3104": "No current HA mapping found in the inspected register groups.",
            "I3172_I3173": "HA already uses V and /10; no consumer metadata change is required.",
            "I3210_I3212": "HA already exposes unitless raw enum values; no consumer metadata change is required.",
            "I3232": "Canonical battery-load-voltage correction has no current HA mapping; do not create an entity in this audit.",
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--spec", type=Path, default=DEFAULT_SPEC)
    parser.add_argument("--ha-snapshot", type=Path, required=True)
    parser.add_argument("--consumer-commit", required=True)
    parser.add_argument(
        "--decoder-behavior",
        choices=("legacy", "mapping_declared"),
        default="legacy",
        help="Model the historical or mapping-declared two-word decoder.",
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    snapshot = json.loads(args.ha_snapshot.read_text(encoding="utf-8"))
    result = build_audit(
        spec, snapshot, args.consumer_commit, args.decoder_behavior
    )
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result["summary"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
