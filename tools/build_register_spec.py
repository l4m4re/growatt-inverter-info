#!/usr/bin/env python3
"""Build the project-independent Growatt Register Specification.

The resolved HA-era reference is used as a compatibility input during this
migration.  The output deliberately removes HA-specific semantics from the
public model and adds subsystem, instance, evidence, protocol and logical-field
metadata.  The old reference remains a generated compatibility view; this
directory is the canonical consumer-facing product.
"""

# ruff: noqa: D103, T201

from collections import defaultdict
import json
from pathlib import Path
import re
from typing import Any

SPEC_DIR = Path(__file__).resolve().parents[1] / "spec"
DOC_DIR = SPEC_DIR.parent
SOURCE_PATH = DOC_DIR / "knowledge" / "compatibility" / "growatt-register-reference.json"
BLOCK_PATH = DOC_DIR / "sources" / "evidence" / "min-6000tl-xh-block-validation.json"
OUTPUT_PATH = SPEC_DIR / "growatt-register-spec.json"
FAMILY_SLUGS = {
    "min_tl_xh": "MIN_TL_XH",
    "tl3_max_mid_mac": "TL3_MAX_MID_MAC",
    "mod_tl3_xh": "MOD_TL3_XH",
    "storage_mix": "MIX",
    "storage_spa": "SPA",
    "storage_sph": "SPH",
    "legacy_inverter_315": "LEGACY_315",
    "spf_offgrid": "SPF",
}

EXPECTED_HUMAN_FILES = {
    "README.md",
    "PROTOCOLS.md",
    "SEMANTIC_INDEX.md",
    *(f"families/{slug}.md" for slug in FAMILY_SLUGS.values()),
}

# Audit result from the checked-in HA-6C artifact before this correction.
HA6C_COMPONENT_ALTERNATE_EDGES = 2096

SEMANTIC_RENAMES = {
    "battery_current": "battery.current",
    "battery_voltage": "battery.voltage",
    "battery_soc": "battery.soc",
    "battery_charge_power": "battery.charge_power",
    "battery_discharge_power": "battery.discharge_power",
    "pv_total_power": "pv.total_power",
    "grid_import_power": "grid.import_power",
    "grid_export_power": "grid.export_power",
    "grid_export_energy_today": "grid.export_energy_today",
    "grid_export_energy_total": "grid.export_energy_total",
    "house_load_power": "load.house_power",
    "inverter_status": "inverter.status",
    "grid_frequency": "grid.frequency",
    "ac_phase_l3_power": "ac.phase.l3_power",
    "inverter_runtime": "inverter.runtime",
    "pv4_energy_total": "pv.mppt4.energy_total",
    "battery_charge_today": "battery.charge_energy_today",
    "battery_charge_total": "battery.charge_energy_total",
    "battery_discharge_today": "battery.discharge_energy_today",
    "battery_discharge_total": "battery.discharge_energy_total",
    "battery_charge_energy_today": "battery.charge_energy_today",
    "battery_charge_energy_total": "battery.charge_energy_total",
    "battery_discharge_energy_today": "battery.discharge_energy_today",
    "battery_discharge_energy_total": "battery.discharge_energy_total",
    "ac_charge_energy_today": "battery.ac_charge_energy_today",
    "ac_charge_energy_total": "battery.ac_charge_energy_total",
    "battery_load_voltage": "battery.load_voltage",
    "battery_pack_count": "battery.pack_count",
    "battery_request_flags": "battery.request_flags",
    "batterystate": "battery.state",
    "batterytype": "battery.type",
    "batteryvoltage": "battery.voltage",
    "bdc_data_separation": "bdc.data_separation",
    "bdc_derating_mode": "bdc.derating_mode",
    "bdc_system_mode_status": "bdc.system_mode_status",
    "bdc_fault_code": "bdc.fault_code",
    "bdc_warning_code": "bdc.warning_code",
    "inverter_warning_flags_high": "inverter.warning_flags_high",
    "inverter_warning_subcode": "inverter.warning_subcode",
    "inverter_warning_flags": "inverter.warning_flags",
    "inverter_present_fft_value_channel_a": "inverter.present_fft_value_channel_a",
    "bms_average_temperature_channel_a": "diagnostic.bms_average_temperature_channel_a",
    "bms_max_cell_temperature_channel_b": "diagnostic.bms_max_cell_temperature_channel_b",
    "bms_average_temperature_channel_c": "diagnostic.bms_average_temperature_channel_c",
    "bms_max_soc": "battery.bms_max_soc",
    "bms_min_soc": "battery.bms_min_soc",
    "battery_bms_full_charge_capacity": "battery.bms_full_charge_capacity",
    "battery_bms_remaining_capacity": "battery.bms_remaining_capacity",
    "battery_bms_discharge_voltage_limit": "battery.bms_discharge_voltage_limit",
    "battery_bms_max_cell_voltage": "battery.bms_max_cell_voltage",
    "battery_bms_min_cell_voltage": "battery.bms_min_cell_voltage",
    "battery_bms_cycle_count": "battery.bms_cycle_count",
    "battery_bms_soh": "battery.bms_soh",
}

CANONICAL_NAME_ALIASES = {
    "batterytyp e": "Battery type",
    "batterytype": "Battery type",
    "batterystate": "Battery state",
    "batteryvoltage": "Battery voltage",
    "batterycurrent": "Battery current",
    "battery charge today": "Battery charge energy today",
    "battery charge total": "Battery charge energy total",
    "battery discharge today": "Battery discharge energy today",
    "battery discharge total": "Battery discharge energy total",
    "battery load voltage": "Battery load voltage",
    "battery pack count": "Battery pack count",
    "battery request flags": "Battery request flags",
    "binvallfaultcod e": "Inverter aggregate fault code",
    "vbatstartf ordischarg e": "Battery discharge start voltage",
}

BITFIELD_OVERRIDES = {
    ("min_tl_xh", "holding", 1): [
        (0, 0, "spi_enable", "SPI enable", "System protection interface enable."),
        (1, 1, "auto_test_start", "AutoTestStart", "Automatic test start."),
        (2, 2, "lvfrt_enable", "LVFRT enable", "Low-voltage ride-through enable."),
        (3, 3, "frequency_derating_enable", "FreqDerating Enable", "Frequency derating enable."),
        (4, 4, "softstart_enable", "Softstart enable", "Soft-start enable."),
        (5, 5, "drms_enable", "DRMS enable", "Demand-response management enable."),
        (6, 6, "power_voltage_function_enable", "PowerVoltFunc Enable", "Power/voltage function enable."),
        (7, 7, "hvfrt_enable", "HVFRT enable", "High-voltage ride-through enable."),
        (8, 8, "rocof_enable", "ROCOF enable", "Rate-of-change-of-frequency protection enable."),
        (9, 9, "recover_frequency_derating_mode_enable", "Recover FreqDeratingMode Enable", "Recovery frequency-derating mode enable."),
        (10, 10, "split_phase_enable", "Split phase enable", "Split-phase enable."),
        (11, 15, "reserved", "Reserved", "Reserved by the vendor."),
    ],
    ("min_tl_xh", "input", 3187): [
        (0, 0, "charge_enabled", "ChargeEn", "BDC allows charging."),
        (1, 1, "discharge_enabled", "DischargeEn", "BDC allows discharge."),
        (2, 7, "reserved", "Resvd", "Reserved."),
        (8, 11, "warning_subcode", "WarnSubCode", "BDC sub-warning code."),
        (12, 15, "fault_subcode", "FaultSubCode", "BDC sub-error code."),
    ],
    ("min_tl_xh", "input", 3104): [
        (0, 0, "turn_off_order", "turn off Order", "Standby was requested by the turn-off order."),
        (1, 1, "pv_low", "PVLow", "PV input is below the standby threshold."),
        (2, 2, "ac_voltage_or_frequency_out_of_scope", "AC Volt/Freq out of scope", "AC voltage or frequency is out of scope."),
        (3, 7, "reserved", "Reserved", "Reserved by the vendor."),
    ],
    ("min_tl_xh", "input", 3164): [],
    ("min_tl_xh", "input", 3211): [
        (0, 0, "charging_prohibited", "Prohibit charging", "1 prohibits charging; 0 allows charging."),
        (1, 1, "strong_charge_enabled", "Enable strong charge", "1 enables strong charge; 0 disables strong charge."),
        (2, 2, "strong_charge_2_enabled", "Enable strong charge2", "1 enables strong charge2; 0 disables strong charge2."),
        (8, 8, "discharge_prohibited", "Discharge is prohibited", "1 prohibits discharge; 0 allows discharge."),
        (9, 9, "power_reduction_enabled", "Turn on power reduction", "1 turns on power reduction; 0 turns it off."),
    ],
}

PACKED_FIELD_OVERRIDES = {
    ("min_tl_xh", "input", 3000): [
        {
            "bits": [8, 15],
            "name": "mode",
            "vendor_label": "high-byte mode",
            "description": "Vendor-defined inverter mode byte.",
            "enum": {
                "0": "waiting_module",
                "1": "self_test",
                "2": "reserved",
                "3": "system_fault_module",
                "4": "flash_module",
                "5": "pv_battery_online_module",
                "6": "battery_online_module",
            },
        },
        {
            "bits": [0, 7],
            "name": "status",
            "vendor_label": "low-byte status",
            "description": "The vendor source does not enumerate the low-byte values separately.",
        },
    ],
    ("min_tl_xh", "input", 3166): [
        {
            "bits": [8, 15],
            "name": "mode",
            "vendor_label": "mode",
            "enum": {
                "0": "no_charge_or_discharge",
                "1": "charge",
                "2": "discharge",
            },
        },
        {
            "bits": [0, 7],
            "name": "status",
            "vendor_label": "status",
            "enum": {
                "0": "standby",
                "1": "normal",
                "2": "fault",
                "3": "flash",
            },
        },
    ],
    ("min_tl_xh", "holding", 3125): [
        {"bits": [0, 3], "name": "month_low", "vendor_label": "month_L"},
        {"bits": [4, 7], "name": "month_high", "vendor_label": "month_H"},
        {"bits": [8, 8], "name": "enabled", "vendor_label": "enable"},
        {"bits": [9, 15], "name": "reserved", "vendor_label": "reserve"},
    ],
    ("min_tl_xh", "holding", 3202): [
        {"bits": [0, 6], "name": "minute", "vendor_label": "min", "range": "0-59"},
        {"bits": [7, 11], "name": "hour", "vendor_label": "hour", "range": "0-23"},
        {"bits": [12, 14], "name": "priority", "vendor_label": "loadfirst/batfirst/gridfirst/anti-reflux", "enum": {"0": "load_first", "1": "battery_first", "2": "grid_first", "3": "anti_reflux"}},
        {"bits": [15, 15], "name": "enabled", "vendor_label": "enable", "enum": {"0": "disabled", "1": "enabled"}},
    ],
    ("min_tl_xh", "holding", 3220): [
        {"bits": [0, 7], "name": "day", "vendor_label": "day", "range": "0-31"},
        {"bits": [8, 14], "name": "month", "vendor_label": "month", "range": "1-12"},
        {"bits": [15, 15], "name": "enabled", "vendor_label": "enable", "enum": {"0": "disabled", "1": "enabled"}},
    ],
    ("min_tl_xh", "holding", 3221): [
        {"bits": [0, 6], "name": "minute", "vendor_label": "min", "range": "0-59"},
        {"bits": [7, 11], "name": "hour", "vendor_label": "hour", "range": "0-23"},
        {"bits": [12, 14], "name": "priority", "vendor_label": "loadfirst/batfirst/gridfirst/anti-reflux", "enum": {"0": "load_first", "1": "battery_first", "2": "grid_first", "3": "anti_reflux"}},
        {"bits": [15, 15], "name": "enabled", "vendor_label": "enable", "enum": {"0": "disabled", "1": "enabled"}},
    ],
}

ENUM_OVERRIDES = {
    ("min_tl_xh", "input", 0): {
        0: "waiting",
        1: "normal",
        3: "fault",
    },
    ("min_tl_xh", "input", 3086): {
        0: "not_derated",
        1: "pv_high",
        2: "power_constant",
        3: "grid_voltage_high",
        4: "frequency_high",
        5: "dc_source_mode",
        6: "inverter_temperature",
        7: "active_power_order",
        8: "load_speed",
        9: "over_back_by_time",
        10: "internal_temperature",
        11: "outdoor_temperature",
        12: "line_impedance_calculation",
        13: "parallel_anti_backflow",
        14: "local_anti_backflow",
        15: "bdc_load_priority",
        16: "ct_check_error",
    },
    ("min_tl_xh", "input", 3118): {
        0: "no_bdc_connected",
        1: "bdc1_connected",
        2: "bdc2_connected",
        3: "bdc1_and_bdc2_connected",
    },
    ("min_tl_xh", "input", 3164): {
        0: "no_separate_bdc_data",
        1: "separate_bdc_data",
    },
    ("min_tl_xh", "input", 3165): {
        0: "normal_unrestricted",
        1: "standby_or_fault",
        2: "maximum_discharge_current_limit",
        3: "battery_discharge_enabled",
        4: "high_bus_discharge_derating",
    },
    ("min_tl_xh", "input", 3210): {
        0: "not_detected",
        1: "detection_completed",
    },
    ("min_tl_xh", "input", 3212): {
        0: "dormancy",
        1: "charge",
        2: "discharge",
        3: "free",
        4: "standby",
        5: "soft_start",
        6: "fault",
        7: "update",
    },
}

NORMALIZED_OVERRIDES = {
    ("min_tl_xh", "input", 0): {
        "raw_type": "u16 enum",
        "signed": False,
        "divisor": None,
        "scale": 1,
    },
    ("min_tl_xh", "input", 3000): {
        "raw_type": "u16 packed: high byte mode, low byte status",
        "signed": False,
    },
    ("min_tl_xh", "input", 3104): {
        "raw_type": "u16 vendor-defined bitfield",
        "signed": False,
    },
    ("min_tl_xh", "input", 3086): {
        "raw_type": "u16 enum",
        "signed": False,
        "divisor": None,
        "scale": 1,
    },
    ("min_tl_xh", "input", 3118): {
        "raw_type": "u16 enum",
        "signed": False,
        "divisor": None,
        "scale": 1,
    },
    ("min_tl_xh", "input", 3166): {
        "raw_type": "u16 packed: upper byte mode, lower byte status",
        "signed": False,
    },
    ("min_tl_xh", "input", 3187): {
        "raw_type": "u16 bitfield",
        "signed": False,
    },
    ("min_tl_xh", "input", 3211): {
        "raw_type": "u16 bitfield",
        "signed": False,
    },
}

EXTERNAL_IMPLEMENTATIONS = {
    "grott",
    "openinverter_gateway",
    "inverter_to_mqtt",
}

EVIDENCE_LEVELS = (
    "source_documented",
    "implementation_correlated",
    "read_observed",
    "value_plausible",
    "semantic_verified",
    "write_accepted",
    "write_reversible",
    "behavior_verified",
)

EVIDENCE_DESCRIPTIONS = {
    "source_documented": "A retained vendor or source document explicitly describes the physical field.",
    "implementation_correlated": "Independent implementation families agree with the interpretation; generated derivatives are not counted independently.",
    "read_observed": "The physical address or native block returned successfully from real hardware; this does not establish semantics.",
    "value_plausible": "A retained raw value decodes compatibly with the claimed datatype, scale, unit and expected range.",
    "semantic_verified": "A decoded value or behavior was meaningfully compared with independently trusted device state; none is asserted without that evidence.",
    "write_accepted": "A controlled write was accepted and read back; none is asserted in this release.",
    "write_reversible": "The exact original raw value was restored and verified; none is asserted in this release.",
    "behavior_verified": "Observed device behavior matched the claimed control semantics; none is asserted in this release.",
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def slug(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9]+", " ", value).strip().lower()
    return re.sub(r"\s+", "_", value) or "unknown"


def numeric_or_none(value: Any) -> int | float | None:
    return (
        value
        if isinstance(value, (int, float)) and not isinstance(value, bool)
        else None
    )


def canonical_name(record: dict[str, Any]) -> str | None:
    value = str(record.get("semantic_name") or record.get("canonical_name") or "").strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\s+([,.;:)])", r"\1", value)
    value = re.sub(r"\((?:high|low|middle)\)", "", value, flags=re.IGNORECASE).strip()
    compact = re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()
    return CANONICAL_NAME_ALIASES.get(compact, value) or None


def semantic_quantity(record: dict[str, Any], name: str | None) -> tuple[str | None, str]:
    key = record.get("semantic_key")
    if key in SEMANTIC_RENAMES:
        return SEMANTIC_RENAMES[key], "reconciled"
    if key:
        return key.replace("_", "."), "syntactic_only"
    compact = re.sub(r"[^a-z0-9]+", "", (name or "").lower())
    direct_names = {
        "batterytype": "battery.type",
        "batterystate": "battery.state",
        "batteryvoltage": "battery.voltage",
        "batterycurrent": "battery.current",
        "batterychargetoday": "battery.charge_energy_today",
        "batterychargetotal": "battery.charge_energy_total",
        "batterydischargetoday": "battery.discharge_energy_today",
        "batterydischargetotal": "battery.discharge_energy_total",
        "batterychargeenergytoday": "battery.charge_energy_today",
        "batterychargeenergytotal": "battery.charge_energy_total",
        "batterydischargeenergytoday": "battery.discharge_energy_today",
        "batterydischargeenergytotal": "battery.discharge_energy_total",
        "acchargeenergytoday": "battery.ac_charge_energy_today",
        "acchargeenergytotal": "battery.ac_charge_energy_total",
        "batteryloadvoltage": "battery.load_voltage",
        "batterypackcount": "battery.pack_count",
        "batteryrequestflags": "battery.request_flags",
        "inverteraggregatefaultcode": "diagnostic.inverter_all_fault_code",
        "batterydischargestartvoltage": "battery.discharge_start_voltage",
    }
    if compact in direct_names:
        return direct_names[compact], "reconciled"
    if name and not name.lower().startswith(("register ", "reserved", "unknown")):
        category = {
            "battery": "battery",
            "control": "control",
            "diagnostic": "diagnostic",
            "energy": "energy",
            "telemetry": "telemetry",
        }.get(record.get("semantic_category"), "field")
        return f"{category}.{slug(name)}", "syntactic_only"
    return None, "unresolved"


def component_marker(record: dict[str, Any]) -> str | None:
    aliases = record.get("source_aliases", {}).get("vendor", [])
    text = " ".join([*aliases, str(record.get("description", "")), str(record.get("canonical_name", ""))])
    if any(re.search(r"(?:high|H)$", alias.strip()) for alias in aliases) or re.search(r"(?:high\s+word|\(high\)|\bhigh\b)", text, re.IGNORECASE):
        return "high_word"
    if any(re.search(r"(?:low|L)$", alias.strip()) for alias in aliases) or re.search(r"(?:low\s+word|\(low\)|\blow\b)", text, re.IGNORECASE):
        return "low_word"
    if any(re.search(r"(?:middle|M)$", alias.strip()) for alias in aliases) or re.search(r"(?:middle\s+word|\bmiddle\b)", text, re.IGNORECASE):
        return "middle_word"
    return None


def logical_key(record: dict[str, Any]) -> str:
    aliases = record.get("source_aliases", {}).get("vendor", [])
    for value in aliases:
        value = re.sub(r"(?:high|low|middle|[HLM])$", "", value, flags=re.IGNORECASE)
        value = re.sub(r"[^A-Za-z0-9]+", "", value).lower()
        if value:
            return value
    return re.sub(r"[^A-Za-z0-9]+", "", str(record.get("canonical_name", ""))).lower()


def subsystem(record: dict[str, Any]) -> tuple[str, str]:
    review = record.get("review") or {}
    if review.get("subsystem") and review.get("measurement_point"):
        return review["subsystem"], review["measurement_point"]
    if (
        record.get("family") == "min_tl_xh"
        and record.get("table") == "holding"
        and 3036 <= record.get("address", -1) <= 3082
    ):
        return "control", "inverter_control"
    text = " ".join(
        [
            str(record.get("canonical_name", "")),
            str(record.get("description", "")),
            " ".join(record.get("source_aliases", {}).get("vendor", [])),
        ]
    ).lower()
    address = record["address"]
    if "bms" in text or address in range(3212, 3232):
        return "bms", "bms"
    if (record.get("semantic_key") or "").startswith("battery") or "battery" in text:
        return "storage_device", "bdc_or_storage_device"
    if "mppt" in text or "pv" in text or "input" in text:
        return "pv", "pv_or_mppt"
    if "grid" in text or "frequency" in text:
        return "grid", "grid_meter_or_inverter"
    if "load" in text:
        return "load", "load_meter_or_inverter"
    if "ac phase" in text or "phase" in text:
        return "ac", "ac_phase"
    if record.get("semantic_category") == "control":
        return "control", "inverter_control"
    if "inverter" in text:
        return "inverter", "inverter"
    return "unknown", "unknown"


def instance_metadata(record: dict[str, Any], sub: str) -> dict[str, Any]:
    text = " ".join(
        [
            str(record.get("canonical_name", "")),
            *record.get("source_aliases", {}).get("vendor", []),
        ]
    )
    mppt = re.search(r"(?:PV|MPPT)\s*([1-9][0-9]*)", text, re.IGNORECASE)
    phase = re.search(r"phase\s*(L[1-3])", text, re.IGNORECASE)
    if mppt:
        return {
            "instance_kind": "mppt",
            "instance": int(mppt.group(1)),
            "instance_status": "vendor_indexed",
            "index_kind": "mppt",
            "index": int(mppt.group(1)),
        }
    if phase:
        return {
            "instance_kind": "ac_phase",
            "instance": None,
            "instance_status": "vendor_indexed",
            "index_kind": "phase",
            "index": phase.group(1).upper(),
        }
    if sub != "bms":
        return {
            "instance_kind": None,
            "instance": None,
            "instance_status": "not_applicable",
            "index_kind": None,
            "index": None,
        }
    return {
        "instance_kind": "bms",
        "instance": None,
        "instance_status": "unknown",
        "index_kind": None,
        "index": None,
        "structure_id": "bms_status_and_telemetry_block",
        "structure_note": "Repeated BMS fields are retained structurally; numeric suffixes on diagnostics do not prove separate BMS instances.",
    }


def evidence(record: dict[str, Any]) -> list[dict[str, Any]]:
    provenance = set(record.get("provenance", []))
    levels: set[str] = set()
    if "vendor_v124" in provenance or "vendor_v314" in provenance:
        levels.add("source_documented")
    if provenance & EXTERNAL_IMPLEMENTATIONS:
        levels.add("implementation_correlated")
    if any(
        item.get("source") == "min_live_validation"
        for item in record.get("validation_evidence", [])
    ):
        levels.add("read_observed")
    if (
        record["family"] == "min_tl_xh"
        and record["table"] == "input"
        and record["address"] == 3217
    ):
        levels.add("value_plausible")
    result = []
    source_ids = sorted({"vendor_v124"} & provenance)
    implementation_ids = sorted(EXTERNAL_IMPLEMENTATIONS & provenance)
    read_ids = ["min_live_validation"] if "min_live_validation" in provenance else []
    for level in EVIDENCE_LEVELS:
        if level in levels:
            sources = {
                "source_documented": source_ids,
                "implementation_correlated": implementation_ids,
                "read_observed": read_ids,
                "value_plausible": ["ha5_regression_tests", "min_live_validation"],
            }.get(level, [])
            result.append({"level": level, "sources": sources})
    return result


def write_policy(record: dict[str, Any]) -> str:
    if record.get("access") not in {"W", "R/W"}:
        return "read_only"
    text = f"{record.get('canonical_name', '')} {record.get('description', '')}".lower()
    dangerous = (
        "reset",
        "factory",
        "firmware",
        "bootloader",
        "baud",
        "modbus address",
        "country",
        "grid code",
        "safety",
        "on/off",
        "shutdown",
        "reboot",
    )
    if any(token in text for token in dangerous):
        return "never_test"
    if any(
        token in text
        for token in ("schedule", "mode", "enable", "frequency", "voltage")
    ):
        return "conditional"
    return "unknown_write_risk"


def resolution_from_evidence(
    record: dict[str, Any], evidence_items: list[dict[str, Any]]
) -> dict[str, Any]:
    review = record.get("review") or {}
    if review.get("resolution_status"):
        result = {
            "status": review["resolution_status"],
            "confidence": review.get("confidence"),
        }
        if review.get("rationale"):
            result["note"] = review["rationale"]
        return result
    name = str(record.get("canonical_name", ""))
    if name.lower().startswith(("register ", "reserved", "unknown")):
        return {"status": "unknown_reserved", "confidence": "low"}
    levels = {item["level"] for item in evidence_items}
    has_vendor = "source_documented" in levels
    has_implementation = "implementation_correlated" in levels
    if has_vendor and has_implementation:
        status = "resolved_with_notes" if record.get("conflicts") else "resolved"
        confidence = "medium" if record.get("conflicts") else "high"
    elif has_vendor:
        status, confidence = "source_only", "medium"
    elif has_implementation:
        status, confidence = "source_only", "low"
    else:
        status, confidence = "unknown_reserved", "low"
    result = {"status": status, "confidence": confidence}
    if record.get("conflicts"):
        result["note"] = "; ".join(
            item.get("detail", "") for item in record["conflicts"]
        )
    return result


def normalized_enums(record: dict[str, Any]) -> list[dict[str, Any]]:
    key = (record["family"], record["table"], record["address"])
    if key in PACKED_FIELD_OVERRIDES or (
        key in BITFIELD_OVERRIDES and BITFIELD_OVERRIDES[key]
    ):
        return []
    if key in ENUM_OVERRIDES:
        return [
            {
                "value": value,
                "canonical_name": label,
                "vendor_label": label,
                "ambiguous": False,
            }
            for value, label in ENUM_OVERRIDES[key].items()
        ]
    grouped: dict[int, set[str]] = defaultdict(set)
    definitions = list(record.get("enum_definitions", []))
    text = " ".join(
        str(record.get(key, "")) for key in ("canonical_name", "description", "encoding", "unit")
    )
    definitions.extend(
        {"value": int(match.group(1)), "label": match.group(2).strip()}
        for match in re.finditer(
            r"(?<![A-Za-z])(\d{1,3})\s*[:=]\s*(.*?)(?=\s+\d{1,3}\s*[:=]|[,;]|$)",
            text,
        )
    )
    for item in definitions:
        label = str(item.get("label", "")).strip()
        unit = str(record.get("unit") or "").strip()
        if unit and label.lower().endswith(f" {unit.lower()} {unit.lower()}"):
            label = label[: -len(unit) - 1].rstrip()
        if label:
            grouped[int(item["value"])].add(label)
    return [
        {
            "value": value,
            "canonical_name": slug("_".join(sorted(labels))),
            "vendor_label": " / ".join(sorted(labels)),
            "ambiguous": len(labels) > 1,
        }
        for value, labels in sorted(grouped.items())
    ]


def bitfields(record: dict[str, Any]) -> list[dict[str, Any]]:
    key = (record["family"], record["table"], record["address"])
    definitions = BITFIELD_OVERRIDES.get(key)
    if definitions is None:
        text = " ".join(
            str(record.get(item, ""))
            for item in ("canonical_name", "description", "encoding")
        )
        definitions = []
        for match in re.finditer(
            r"bit\s*(\d+)(?:\s*[~\-–]\s*(\d+))?\s*[:：]\s*([^;]+)",
            text,
            re.IGNORECASE,
        ):
            start = int(match.group(1))
            end = int(match.group(2) or start)
            label = match.group(3).strip()
            definitions.append((start, end, slug(label), label, None))
        if not definitions and re.search(r"flags?|flag word|bitfield", text, re.IGNORECASE):
            return [
                {
                    "bits": [0, 15],
                    "name": "undocumented_flags",
                    "vendor_label": "undocumented flag word",
                    "status": "placeholder",
                    "description": "The source identifies a packed flag word but does not define safe individual meanings.",
                    "provenance": ["vendor_v124"],
                }
            ]
    result = []
    for start, end, name, vendor_label, description in definitions:
        result.append(
            {
                "bits": [start] if start == end else [start, end],
                "name": name,
                "vendor_label": vendor_label,
                "status": "structured",
                "description": description or vendor_label,
                "provenance": ["vendor_v124"],
            }
        )
    return result


def packed_fields(record: dict[str, Any]) -> list[dict[str, Any]] | None:
    override = PACKED_FIELD_OVERRIDES.get(
        (record["family"], record["table"], record["address"])
    )
    if override:
        return [
            {**field, "status": "source_explicit", "provenance": ["vendor_v124"]}
            for field in override
        ]
    text = " ".join(
        str(record.get(item, "")) for item in ("canonical_name", "description", "encoding")
    )
    if not re.search(r"bit\s*\d|packed|flags?", text, re.IGNORECASE):
        return None
    return None


def logical_fields(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lookup = {(r["family"], r["table"], r["address"]): r for r in records}
    explicit: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for record in records:
        marker = component_marker(record)
        if marker:
            explicit[(record["family"], record["table"], logical_key(record))].append(record)

    groups: list[tuple[list[dict[str, Any]], str, str]] = []
    assigned: set[str] = set()
    for candidates in explicit.values():
        candidates.sort(key=lambda item: item["address"])
        if len(candidates) < 2:
            continue
        for start in range(len(candidates) - 1):
            pair = candidates[start : start + 2]
            if pair[1]["address"] != pair[0]["address"] + 1:
                continue
            roles = [component_marker(item) for item in pair]
            if roles == ["high_word", "low_word"]:
                groups.append((pair, "high_low", "source_explicit"))
                assigned.update(item["physical_id"] for item in pair)
                break
        if len(candidates) >= 3 and all(component_marker(item) for item in candidates):
            addresses = [item["address"] for item in candidates]
            if addresses == list(range(addresses[0], addresses[-1] + 1)):
                groups.append((candidates, "high_middle_low", "source_explicit"))
                assigned.update(item["physical_id"] for item in candidates)

    fields: list[dict[str, Any]] = []
    for components, order, evidence_status in groups:
        first = components[0]
        identity = first["semantic_identity"]
        field_id = f"logical:{first['family']}:{first['table']}:{first['address']}:{slug(identity['quantity'] or first['normalized']['name'] or 'field')}"
        for item in components:
            item["logical_field_id"] = field_id
            item["component_role"] = component_marker(item) or "word"
            item["length_words"] = 1
            role_name = item["component_role"].replace("_", " ")
            item["normalized"]["name"] = f"{identity['canonical_name']} ({role_name})"
        fields.append(
            {
                "id": field_id,
                "semantic_key": identity["quantity"],
                "canonical_name": identity["canonical_name"],
                "canonical_description": first["vendor"]["description"],
                "subsystem": identity["subsystem"],
                "measurement_point": identity["measurement_point"],
                "instance": first["instance"],
                "resolution": first["resolution"],
                "length_words": len(components),
                "physical_registers": [
                    {
                        "physical_id": item["physical_id"],
                        "family": item["family"],
                        "table": item["table"],
                        "address": item["address"],
                        "role": component_marker(item) or "word",
                    }
                    for item in components
                ],
                "encoding": first["normalized"]["raw_type"],
                "word_order": order,
                "word_order_status": evidence_status,
                "divisor": first["normalized"]["divisor"],
                "scale": first["normalized"]["scale"],
                "unit": first["normalized"]["unit"],
                "relationship_role": "supported",
                "relationships": [],
                "status": "source_explicit",
            }
        )

    for record in records:
        if record["physical_id"] in assigned or record["length_words"] < 2:
            continue
        length = min(record["length_words"], 8)
        component_records = [
            lookup.get((record["family"], record["table"], record["address"] + offset))
            for offset in range(length)
        ]
        if any(item is None for item in component_records):
            continue
        if any(item.get("logical_field_id") for item in component_records if item is not None):
            continue
        field_id = f"logical:{record['physical_id']}"
        for offset, item in enumerate(component_records):
            assert item is not None
            item["logical_field_id"] = field_id
            item["component_role"] = f"word_{offset + 1}"
            item["length_words"] = 1
        identity = record["semantic_identity"]
        fields.append(
            {
                    "id": field_id,
                    "semantic_key": identity["quantity"],
                    "canonical_name": identity["canonical_name"],
                    "canonical_description": record["vendor"]["description"],
                    "subsystem": identity["subsystem"],
                    "measurement_point": identity["measurement_point"],
                    "instance": record["instance"],
                    "resolution": record["resolution"],
                    "length_words": len(component_records),
                    "physical_registers": [
                        {
                            "physical_id": item["physical_id"],
                            "family": item["family"],
                            "table": item["table"],
                            "address": item["address"],
                            "role": f"word_{offset + 1}",
                        }
                        for offset, item in enumerate(component_records)
                    ],
                    "encoding": record["normalized"]["raw_type"],
                    "word_order": "unknown",
                    "word_order_status": "unknown",
                    "divisor": record["normalized"]["divisor"],
                    "scale": record["normalized"]["scale"],
                    "unit": record["normalized"]["unit"],
                    "relationship_role": "supported",
                    "relationships": [],
                    "status": "unknown_word_order",
            }
        )
    return fields


def native_blocks(block_validation: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        {
            "id": item["id"],
            "table": item["table"],
            "function_code": item["function_code"],
            "start": item["start"],
            "end": item["end"],
            "count": item["count"],
            "polling_policy": item["polling_class"],
            "applicability": item["applicability"],
            "hardware_validation": {
                "model": block_validation["meta"]["model"],
                "repetitions": len(item["response_word_counts"]),
                "response_word_counts": item["response_word_counts"],
                "exceptions": item["exceptions"],
                "timeouts": item["timeouts"],
                "retries": item["retries"],
                "crc_bad": item["crc_bad"],
                "observed_response_seconds": item["observed_response_seconds"],
                "evidence_level": "read_observed",
            },
        }
        for item in block_validation["validated_ranges"]
    ]


def runtime_audit_projection(source: dict[str, Any]) -> dict[str, Any]:
    runtime = source["runtime_audit"]
    ha_mapping = load(DOC_DIR / "sources" / "runtime" / "ha-local-registers.snapshot.json")
    occurrences = 0
    identities: set[tuple[str, str, int]] = set()
    family_by_group = {
        ("tlx", "holding_common"): "min_tl_xh",
        ("tlx", "input_common"): "min_tl_xh",
        ("tlx", "input_tl_xh"): "min_tl_xh",
        ("storage", "holding_common"): "storage_mix",
        ("storage", "holding_tl_xh"): "min_tl_xh",
        ("storage", "input_common"): "storage_mix",
        ("storage", "input_tl_xh"): "min_tl_xh",
    }
    for payload_name, payload in ha_mapping.get("devices", {}).items():
        for group, rows in payload.items():
            if not isinstance(rows, list):
                continue
            table = "holding" if "holding" in group else "input"
            for row in rows:
                if isinstance(row, dict) and "register" in row:
                    occurrences += 1
                    identities.add(
                        (family_by_group[(payload_name, group)], table, int(row["register"]))
                    )
    finding_occurrences = sum(
        len(item.get("issues", [])) for item in runtime["findings"]
    )
    unique_findings = {
        (item["family"], item["table"], item["address"], issue["kind"])
        for item in runtime["findings"]
        for issue in item.get("issues", [])
    }
    return {
        "mapping_occurrences_checked": occurrences,
        "unique_family_table_address_mappings": len(identities),
        "unique_physical_mappings_checked": len(identities),
        "finding_occurrences": finding_occurrences,
        "unique_family_table_address_issue_findings": len(unique_findings),
        "unique_findings": len(unique_findings),
        "finding_kinds": sorted({kind for *_, kind in unique_findings}),
        "classification_policy": "Derived consumer audit; aliases, legitimate legacy maps, repeated instances and missing HA entity exposure are not register-map errors.",
        "findings": runtime["findings"],
    }


def build() -> dict[str, Any]:
    source = load(SOURCE_PATH)
    block = load(BLOCK_PATH)
    source_records = source["records"]
    records = []
    for old in source_records:
        sub, point = subsystem(old)
        identity = instance_metadata(old, sub)
        normalized_name = canonical_name(old)
        semantic_quantity_value, semantic_status = semantic_quantity(old, normalized_name)
        semantic = {
            "quantity": semantic_quantity_value,
            "canonical_name": normalized_name,
            "reconciliation_status": semantic_status,
            "subsystem": sub,
            "measurement_point": point,
            **identity,
        }
        vendor_aliases = old.get("source_aliases", {}).get("vendor", [])
        physical_id = f"{old['family']}:{old['table']}:{old['address']}"
        evidence_items = evidence(old)
        normalized = {
            "name": normalized_name,
            "description": old.get("description"),
            "raw_type": old.get("encoding"),
            "signed": old.get("signed"),
            "divisor": numeric_or_none(old.get("divisor")),
            "multiplier": old.get("multiplier"),
            "scale": numeric_or_none(old.get("scale"))
            or numeric_or_none(old.get("multiplier")),
            "unit": old.get("unit"),
            "access": old.get("access"),
        }
        normalized.update(NORMALIZED_OVERRIDES.get(
            (old["family"], old["table"], old["address"]), {}
        ))
        if (
            old["family"] == "min_tl_xh"
            and old["table"] == "input"
            and old["address"] == 3170
        ):
            normalized["signedness_status"] = (
                "v4_history_validated_non_negative_magnitude"
            )
            normalized["signedness_note"] = (
                "Growatt V4 bdc1_ibat is non-negative in 66 charge and 77 discharge records; I3170 is distinct from directional BMS current I3217."
            )
        elif (
            old["family"] == "min_tl_xh"
            and old["table"] == "input"
            and old["address"] == 3101
        ):
            normalized["signedness_status"] = "v4_history_validated_non_negative"
            normalized["signedness_note"] = (
                "Growatt V4 real_op_percent was non-negative in all 145 retained history records, with an observed range of 0..43%."
            )
        elif (
            old["family"] == "min_tl_xh"
            and old["table"] == "input"
            and old["address"] == 3217
        ):
            normalized["signedness_status"] = "regression_and_live_value_validated"
            normalized["signedness_note"] = (
                "HA-5 regression 0xFEB6 decodes to -3.30 A at 0.01 A resolution; retained live BMS sample is also negative."
            )
        review = old.get("review")
        public_review = (
            {
                key: review[key]
                for key in (
                    "disposition",
                    "rationale",
                    "live_observation",
                    "source_basis",
                    "resolution_status",
                    "confidence",
                )
                if key in review
            }
            if review is not None
            else None
        )
        record_output = {
                "physical_id": physical_id,
                "family": old["family"],
                "family_name": old["family_name"],
                "table": old["table"],
                "address": old["address"],
                "length_words": old["length_registers"],
                "vendor": {
                    "variable_names": vendor_aliases,
                    "description": old.get("description"),
                    "datatype_notation": old.get("encoding"),
                    "unit_notation": old.get("unit"),
                    "access": old.get("access"),
                    "applicability": old.get("model_applicability", []),
                },
                "normalized": normalized,
                "semantic_identity": semantic,
                "instance": identity,
                "enums": normalized_enums(old),
                "bitfields": bitfields(old),
                "packed_fields": packed_fields(old),
                "relationships": [],
                "resolution": resolution_from_evidence(old, evidence_items),
                "normalization": {
                    "status": "assigned" if semantic["quantity"] else "unresolved",
                    "semantic_key_status": "assigned" if semantic["quantity"] else "unassigned",
                    "semantic_reconciliation_status": semantic_status,
                    "reason": None
                    if semantic["quantity"]
                    else "No stable non-placeholder semantic identity was supportable from the retained corpus.",
                },
                "evidence": evidence_items,
                "source_provenance": old.get("provenance", []),
                "source_aliases": old.get("source_aliases", {}),
                "validation_evidence": old.get("validation_evidence", []),
                "write_policy": write_policy(old),
                "native_read_blocks": [],
                "review": public_review,
            }
        if record_output["review"] is None:
            del record_output["review"]
        records.append(record_output)

    fields = logical_fields(records)
    field_by_component = {
        component["physical_id"]: field
        for field in fields
        for component in field["physical_registers"]
    }
    representatives: list[dict[str, Any]] = [
        record for record in records if record["physical_id"] not in field_by_component
    ]
    representatives.extend(fields)
    by_relation: defaultdict[tuple[Any, ...], list[dict[str, Any]]] = defaultdict(list)
    for representative in representatives:
        identity = representative.get("semantic_identity") or {
            "quantity": representative["semantic_key"],
            "subsystem": representative["subsystem"],
            "instance_kind": representative["instance"]["instance_kind"],
            "instance": representative["instance"]["instance"],
        }
        if identity["quantity"] and identity["instance_kind"] != "bms":
            by_relation[
                (
                    representative["family"] if "family" in representative else representative["physical_registers"][0]["family"],
                    identity["quantity"],
                    identity["subsystem"],
                    identity["instance_kind"],
                    identity.get("instance"),
                )
            ].append(representative)
    for group in by_relation.values():
        preferred = next(
            (r for r in group if r["resolution"]["status"] == "resolved"), group[0]
        )
        for representative in group:
            if len(group) == 1:
                continue
            if representative is preferred:
                role = "preferred"
            elif representative["resolution"]["status"] == "source_only":
                role = "legacy_or_supported"
            else:
                role = "alternate"
            representative["relationships"] = [
                {
                    "type": "alternate",
                    "target": other["id"] if "id" in other else other["physical_id"],
                }
                for other in group
                if other is not representative
            ]
            if "semantic_identity" in representative:
                representative["semantic_identity"]["relationship_role"] = role
    for record in records:
        if record.get("logical_field_id"):
            record["component_of"] = record["logical_field_id"]
            record["relationships"] = []
            record["semantic_identity"]["relationship_role"] = "component"
    for record in records:
        record["native_read_blocks"] = [
            page["id"]
            for page in block["validated_ranges"]
            if page["family"] == record["family"]
            and page["table"] == record["table"]
            and page["start"] <= record["address"] <= page["end"]
            and record["address"] + record["length_words"] - 1 <= page["end"]
        ]
        if record["family"] == "min_tl_xh" and record["address"] == 3170:
            record["resolution"] = {
                "status": "resolved",
                "confidence": "high",
                "note": "Growatt V4 bdc1_ibat is non-negative in 66 charge and 77 discharge records; I3170 is distinct from directional BMS current I3217.",
            }
        if (
            record["family"] == "min_tl_xh"
            and record["table"] == "input"
            and record["address"] == 3217
        ):
            record["semantic_identity"]["subsystem"] = "bms"
            record["semantic_identity"]["measurement_point"] = "bms"
            record["semantic_identity"]["relationship_role"] = "supported"
            record["relationships"] = []

    records.sort(key=lambda item: (item["family"], item["table"], item["address"]))
    families = []
    for family in source["families"]:
        family_records = [r for r in records if r["family"] == family["id"]]
        families.append(
            {
                "id": family["id"],
                "name": family["name"],
                "slug": FAMILY_SLUGS.get(family["id"], slug(family["id"]).upper()),
                "protocol_group": family["protocol_group"],
                "aliases": family.get("aliases", []),
                "models": family.get("models", []),
                "notes": family.get("notes", ""),
                "record_count": len(family_records),
                "live_hardware_observed": family["id"] == "min_tl_xh",
            }
        )
    semantic_index: dict[str, list[str]] = defaultdict(list)
    for record in records:
        if record["semantic_identity"]["quantity"] and not record.get("component_of"):
            semantic_index[record["semantic_identity"]["quantity"]].append(
                record["physical_id"]
            )
    for field in fields:
        if field["semantic_key"]:
            semantic_index[field["semantic_key"]].append(field["id"])
    semantic_assigned = sum(bool(r["semantic_identity"]["quantity"]) for r in records)
    semantic_reconciled = sum(
        r["semantic_identity"]["reconciliation_status"] == "reconciled"
        for r in records
    )
    component_count = sum(bool(r.get("component_of")) for r in records)
    bitfield_source_indicated = sum(bool(r["bitfields"]) for r in records)
    bitfield_structured = sum(
        any(item.get("status") == "structured" for item in r["bitfields"])
        for r in records
    )
    bitfield_placeholder = sum(
        any(item.get("status") == "placeholder" for item in r["bitfields"])
        for r in records
    )
    logical_classes = {
        "source_explicit": sum(f["word_order_status"] == "source_explicit" for f in fields),
        "implementation_correlated": sum(f["word_order_status"] == "implementation_correlated" for f in fields),
        "inferred": sum(f["word_order_status"] == "inferred_with_notes" for f in fields),
        "unknown_word_order": sum(f["word_order_status"] == "unknown" for f in fields),
    }
    return {
        "specification": {
            "name": "Growatt Register Specification",
            "version": "1.0",
            "identity": "family + table + address",
            "canonical_truth": True,
            "canonical_source_model": {
                "kind": "neutral_register_graph",
                "maintained_in": "tools/build_register_spec.py",
                "upstream_corpus": "retained vendor, implementation and live-evidence corpus",
                "migration_inputs": ["knowledge/compatibility/growatt-register-reference.json"],
                "status": "bounded_migration",
            },
            "migration_input": "knowledge/compatibility/growatt-register-reference.json",
            "artifact_role": "canonical_machine_and_human_product",
            "scope": "Project-independent Growatt register and protocol knowledge product.",
        },
        "evidence_vocabulary": {
            level: {"description": EVIDENCE_DESCRIPTIONS[level]}
            for level in EVIDENCE_LEVELS
        },
        "source_catalog": {
            **source["meta"]["source_files"],
            "protocol_v314": {
                "label": "Growatt V3.14/3.15 protocol constraints",
                "kind": "primary_source_claim",
                "path": "Growatt-PV-Inverter-Modbus-RS485-RTU-Protocol-V3-14.pdf",
                "independent": True,
            },
            "min_status_reconciliation": {
                "label": "MIN/TL-XH status, fault and warning reconciliation",
                "kind": "model_specific_status_review",
                "path": "docs/reverse-engineering/GII-MIN-RE-3_STATUS_FAULT_WARNING_RECONCILIATION.md",
                "independent": False,
            },
        },
        "families": families,
        "protocols": {
            "120_v124": {
                "minimum_cmd_period_ms": 850,
                "recommended_cmd_period_ms": 1000,
                "maximum_read_words": 125,
                "maximum_write_words": 125,
                "native_read_blocks": source["read_plans"]["vendor_declared_blocks"],
                "source": "vendor_v124",
            },
            "legacy_315": {
                "minimum_cmd_period_ms": 850,
                "recommended_cmd_period_ms": 1000,
                "maximum_read_words": 45,
                "maximum_write_words": 45,
                "boundary_rules": "Vendor V3.14/3.15 grouping restrictions apply.",
                "source": "protocol_v314",
            },
        },
        "registers": records,
        "logical_fields": fields,
        "correction_audit": {
            "component_as_alternate_relationships": {
                "source": "checked-in HA-6C canonical artifact",
                "found": HA6C_COMPONENT_ALTERNATE_EDGES,
                "removed": HA6C_COMPONENT_ALTERNATE_EDGES,
                "remaining": 0,
            }
        },
        "semantic_index": dict(sorted(semantic_index.items())),
        "native_read_evidence": {
            "source": "min_block_validation",
            "capture": {
                key: block["meta"].get(key)
                for key in (
                    "model",
                    "endpoint",
                    "unit",
                    "captured_at",
                    "capture_artifact",
                    "capture_sha256",
                    "analysis",
                )
                if key in block["meta"]
            },
            "pages": native_blocks(block),
            "semantic_claim_policy": "Native-page readability contributes read_observed only; it does not promote every contained register to semantic_verified.",
        },
        "derived_views": {
            "ha_runtime_audit": runtime_audit_projection(source),
            "ha_read_plans": source["read_plans"]["profiles"],
            "min_status_fault_warning_reconciliation": {
                "source": "min_status_reconciliation",
                "disposition": "GII_MIN_STATUS_FAULT_WARNING_RECONCILIATION_WITH_FOLLOW_UP",
                "model": "MIN 6000TL-XH",
                "live_read": {
                    "function_code": 4,
                    "blocks": [
                        {"start": 3000, "count": 125, "response_words": 125},
                        {"start": 3125, "count": 125, "response_words": 125},
                    ],
                },
                "safe_structures": [
                    "I0 legacy inverter status enum",
                    "I3000 packed inverter mode/status word",
                    "I104/I3086 derating mode enum",
                    "I141 PID status enum",
                    "I206 SVG/APF packed ratio/status word",
                    "I238/I3112 AFCI status enum",
                    "I3118 BDC connection enum",
                    "I3119 dry-contact enum",
                    "I3164 BDC data-separation enum",
                    "I3165 BDC derating enum",
                    "I3166 packed BDC mode/status word",
                    "I3187 BDC flag word",
                    "I3210 battery insulation enum",
                    "I3211 battery request flag word",
                    "I3212 BMS status enum",
                ],
                "retained_raw_unknowns": [
                    "I105/I3105 inverter fault words",
                    "I106/I3106 inverter warning words",
                    "I107/I3107 and I108/I3108 subcodes",
                    "I110/I3110 warning bitfield without safe individual meanings",
                    "I115 and I1001-I1008 aggregate/system fault words",
                    "I3167/I3168 BDC fault/warning codes",
                    "I3199 and I3202-I3205/I3213-I3214/I3225-I3226 BMS diagnostic words",
                ],
                "follow_up": [
                    "I3110/I3111 live values versus cloud sys_fault_word3/sys_fault_word4 mapping",
                    "I3165 live value 22 versus the documented 0..4 enum and cloud derate reason",
                    "cloud Warning401 without a proven physical register mapping",
                ],
            },
        },
        "coverage": {
            "physical_registers": len(records),
            "holding_registers": sum(r["table"] == "holding" for r in records),
            "input_registers": sum(r["table"] == "input" for r in records),
            "meaningful_vendor_defined": sum(
                bool(r["vendor"]["variable_names"] or r["vendor"]["description"])
                for r in records
            ),
            "unknown_or_reserved": sum(
                r["resolution"]["status"] == "unknown_reserved" for r in records
            ),
            "semantic_concepts": len(semantic_index),
            "semantic_key_assigned_records": semantic_assigned,
            "semantic_reconciled_records": semantic_reconciled,
            "semantic_unreconciled_records": semantic_assigned - semantic_reconciled,
            "semantic_unresolved_records": len(records) - semantic_assigned,
            "semantic_reconciled_percentage": round(100 * semantic_reconciled / len(records), 2),
            "normalized_records": semantic_assigned,
            "normalized_percentage": round(
                100 * semantic_assigned / len(records),
                2,
            ),
            "logical_multi_register_fields": len(fields),
            "source_explicit_logical_fields": logical_classes["source_explicit"],
            "implementation_correlated_logical_fields": logical_classes["implementation_correlated"],
            "inferred_logical_fields": logical_classes["inferred"],
            "unknown_word_order_logical_fields": logical_classes["unknown_word_order"],
            "component_physical_registers": component_count,
            "component_as_alternate_errors_found": HA6C_COMPONENT_ALTERNATE_EDGES,
            "component_as_alternate_relationships_removed": HA6C_COMPONENT_ALTERNATE_EDGES,
            "indexed_structures": sum(
                bool(r["semantic_identity"].get("index_kind")) for r in records
            ),
            "enum_bearing_records": sum(bool(r["enums"]) for r in records),
            "bitfield_bearing_records": bitfield_source_indicated,
            "bitfield_source_indicated_records": bitfield_source_indicated,
            "bitfield_structured_records": bitfield_structured,
            "bitfield_partially_structured_records": sum(
                any(item.get("status") == "partially_structured" for item in r["bitfields"])
                for r in records
            ),
            "bitfield_placeholder_records": bitfield_placeholder,
            "defined_bitfield_ranges": sum(
                len(r["bitfields"]) for r in records if any(item.get("status") != "placeholder" for item in r["bitfields"])
            ),
            "defined_bit_or_range_count": sum(
                len(r["bitfields"]) for r in records if any(item.get("status") != "placeholder" for item in r["bitfields"])
            ),
            "known_indexed_instances": sum(
                r["semantic_identity"].get("instance_status") == "vendor_indexed" for r in records
            ),
            "unknown_instance_structures": sum(
                r["semantic_identity"].get("instance_status") == "unknown" for r in records
            ),
            "read_only_records": sum(r["write_policy"] == "read_only" for r in records),
            "never_test_records": sum(r["write_policy"] == "never_test" for r in records),
            "conditional_records": sum(r["write_policy"] == "conditional" for r in records),
            "reversible_candidate_records": sum(r["write_policy"] == "reversible_candidate" for r in records),
            "unknown_write_risk_records": sum(r["write_policy"] == "unknown_write_risk" for r in records),
        },
    }


def markdown_record(record: dict[str, Any]) -> str:
    normalized = record["normalized"]
    status = record["resolution"]["status"]
    return (
        f"| {record['table'][0].upper()} | {record['address']} | "
        f"{normalized['name'] or 'Unknown'} | {normalized['raw_type']} | "
        f"{normalized['unit'] or '—'} | {normalized['access']} | {status} |"
    )


def render_family(spec: dict[str, Any], family: dict[str, Any]) -> str:
    records = [r for r in spec["registers"] if r["family"] == family["id"]]
    lines = [
        f"# {family['name']}",
        "",
        family["notes"],
        "",
        "| T | Addr | Canonical name | Type | Unit | Access | Status |",
        "|---|---:|---|---|---|---|---|",
    ]
    lines.extend(markdown_record(record) for record in records)
    interesting = [
        r
        for r in records
        if r["enums"]
        or r["bitfields"]
        or r["relationships"]
        or r["write_policy"] != "read_only"
        or r.get("component_of")
        or r["length_words"] > 1
    ]
    if interesting:
        lines.extend(["", "## Details", ""])
        for record in interesting:
            identity = record["semantic_identity"]
            lines.extend(
                [
                    f"### {record['table']} {record['address']} — {record['normalized']['name']}",
                    "",
                    f"Canonical description: {record['normalized']['description'] or '—'}",
                    f"Physical identity: `{record['physical_id']}`.",
                    f"Semantic: `{identity['quantity'] or 'unknown'}`; subsystem: `{identity['subsystem']}`; measurement point: `{identity['measurement_point']}`; instance/index: `{identity.get('instance_status', '—')}/{identity.get('index', '—')}`.",
                    f"Logical field: `{record.get('component_of', 'none')}`; component role: `{record.get('component_role', 'complete_value')}`.",
                    f"Vendor names: {', '.join(record['vendor']['variable_names']) or '—'}; vendor description: {record['vendor']['description'] or '—'}; vendor unit/type: {record['vendor']['unit_notation'] or '—'} / {record['vendor']['datatype_notation'] or '—'}.",
                    f"Normalized type/signedness/scale: `{record['normalized']['raw_type']}` / `{record['normalized'].get('signed')}` / `{record['normalized'].get('divisor') or record['normalized'].get('scale') or '—'}`.",
                    f"Applicability: {', '.join(record['vendor']['applicability']) or 'family-level'}; relationships: {', '.join(item['type'] + ':' + item['target'] for item in record['relationships']) or 'none'}.",
                    f"Evidence: {', '.join(item['level'] for item in record['evidence']) or 'none'}; resolution: `{record['resolution']['status']}`; write policy: `{record['write_policy']}`; native blocks: {', '.join(record['native_read_blocks']) or 'none'}.",
                    "",
                ]
            )
            if record["enums"]:
                lines.append(
                    "Enums: "
                    + "; ".join(
                        f"{item['value']}={item['canonical_name']} ({item['vendor_label']})"
                        for item in record["enums"]
                    )
                )
            if record["bitfields"]:
                lines.append(
                    "Bitfields: "
                    + "; ".join(
                        f"{item['bits']}={item['name']} ({item.get('status', 'unknown')})" for item in record["bitfields"]
                    )
                )
            if record["packed_fields"]:
                lines.append(
                    "Packed fields: "
                    + "; ".join(
                        f"{item['bits']}={item['name']}" for item in record["packed_fields"]
                    )
                )
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_semantic_index(spec: dict[str, Any]) -> str:
    lines = [
        "# Semantic index",
        "",
        "This index preserves subsystem and instance distinctions; entries are not automatically interchangeable.",
        "",
    ]
    for key, ids in spec["semantic_index"].items():
        lines.extend([f"## `{key}`", ""])
        for item_id in ids:
            if item_id.startswith("logical:"):
                field = next(item for item in spec["logical_fields"] if item["id"] == item_id)
                components = ", ".join(
                    f"I{item['address']} {item['role']}" for item in field["physical_registers"]
                )
                lines.append(
                    f"- logical field `{field['id']}` — {field['subsystem']} / {field['measurement_point']} — `{field['relationship_role']}` — {field['word_order']} / {field['unit'] or 'unitless'} — {components}"
                )
            else:
                record = next(item for item in spec["registers"] if item["physical_id"] == item_id)
                identity = record["semantic_identity"]
                role = identity.get("relationship_role", "supported")
                lines.append(
                    f"- `{record['family']}` {record['table']} {record['address']} — {identity['subsystem']} / {identity['measurement_point']} — `{role}`"
                )
        lines.append("")
    return "\n".join(lines)


def render_readme(spec: dict[str, Any]) -> str:
    coverage = spec["coverage"]
    return f"""# Growatt Register Specification v1

This is the project-independent canonical Growatt register/protocol knowledge
product. It is intended for Home Assistant, Grott-like tools, gateways,
ESP/MQTT projects and diagnostic software. Home Assistant is one consumer and
one corroborating implementation, not the source of truth.

The machine-readable canonical artifact is [`growatt-register-spec.json`](growatt-register-spec.json), validated by [`growatt-register-spec.schema.json`](growatt-register-spec.schema.json). It is generated by the neutral register-graph projection in `tools/build_register_spec.py` from the retained source/evidence corpus. The former compatibility reference is an explicit bounded-migration input, not a second maintained semantic truth.

## Model

Physical identity is always `family + table + address`; holding and input
registers never merge. Records retain vendor wording and aliases alongside
normalized decoding, semantic quantity, subsystem, measurement point,
instance status, relationships, provenance, evidence and write policy.

Repeated BMS fields are represented as a structural BMS group with unknown
instance unless evidence proves an index. Diagnostic suffixes do not create
false BMS instances. Native page reads establish `read_observed`, not
`semantic_verified`.

Coverage: **{coverage["physical_registers"]}** physical records, **{coverage["holding_registers"]}** holding, **{coverage["input_registers"]}** input. Stable semantic keys are assigned to **{coverage["semantic_key_assigned_records"]}** records; **{coverage["semantic_reconciled_records"]}** are semantically reconciled (**{coverage["semantic_reconciled_percentage"]}%**), while **{coverage["semantic_unreconciled_records"]}** remain syntactic-only and **{coverage["semantic_unresolved_records"]}** unresolved. There are **{coverage["logical_multi_register_fields"]}** logical fields (**{coverage["source_explicit_logical_fields"]}** source-explicit, **{coverage["unknown_word_order_logical_fields"]}** unknown word order), **{coverage["enum_bearing_records"]}** enum-bearing records, and **{coverage["bitfield_structured_records"]}** structured versus **{coverage["bitfield_placeholder_records"]}** placeholder bitfield records.

See [`SEMANTIC_INDEX.md`](SEMANTIC_INDEX.md), [`PROTOCOLS.md`](PROTOCOLS.md),
and the generated [GII-2 MIN/TL-XH evidence-review matrix](../docs/reverse-engineering/GII-2_MIN_TL_XH_AUDIT_MATRIX.md),
the family pages [`MIN_TL_XH.md`](families/MIN_TL_XH.md),
[`TL3_MAX_MID_MAC.md`](families/TL3_MAX_MID_MAC.md),
[`MOD_TL3_XH.md`](families/MOD_TL3_XH.md), [`MIX.md`](families/MIX.md),
[`SPA.md`](families/SPA.md), [`SPH.md`](families/SPH.md),
[`LEGACY_315.md`](families/LEGACY_315.md), [`SPF.md`](families/SPF.md),
and [`CLEANUP_MANIFEST.md`](CLEANUP_MANIFEST.md).
"""


def render_protocols(spec: dict[str, Any]) -> str:
    return """# Protocol and native read blocks

## V1.24 / modern 120-family

- minimum command period: 850 ms
- recommended period: 1000 ms
- maximum read/write: 125 words
- native pages and family applicability are in the machine-readable `protocols.120_v124` object.

## V3.14 / 3.15 family

- minimum command period: 850 ms
- recommended period: 1000 ms
- maximum read/write: 45 words
- vendor grouping/boundary restrictions remain family-specific.

The five MIN/TL-XH pages in `native_read_evidence` are bounded live hardware
readability evidence. They are not a Home Assistant polling prescription and
do not promote every returned register to a verified semantic interpretation.
"""


def main() -> None:
    spec = build()
    OUTPUT_PATH.write_text(
        json.dumps(spec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    (SPEC_DIR / "README.md").write_text(render_readme(spec), encoding="utf-8")
    (SPEC_DIR / "SEMANTIC_INDEX.md").write_text(
        render_semantic_index(spec), encoding="utf-8"
    )
    (SPEC_DIR / "PROTOCOLS.md").write_text(render_protocols(spec), encoding="utf-8")
    for family in spec["families"]:
        (SPEC_DIR / "families" / f"{family['slug']}.md").write_text(
            render_family(spec, family), encoding="utf-8"
        )
    missing = [name for name in sorted(EXPECTED_HUMAN_FILES) if not (SPEC_DIR / name).is_file()]
    if missing:
        raise SystemExit(f"generated human documentation is incomplete: {missing}")
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
