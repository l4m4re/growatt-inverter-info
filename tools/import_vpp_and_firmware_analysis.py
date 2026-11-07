#!/usr/bin/env python3
"""Import the VPP source and the public-safe ZABA22 analysis projection.

The binary firmware stays outside this repository. This tool imports only
normalized VPP rows and derived static-analysis evidence, so the GII source
corpus remains reproducible without redistributing firmware or captures.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_MODBUS = ROOT.parent / "Growatt_ModbusTCP"
DEFAULT_FIRMWARE = ROOT.parent / "growatt-firmware"
BLOCK_SOURCE = ROOT / "sources/consolidated/register-blocks.json"


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_revision(path: Path) -> str | None:
    try:
        return subprocess.check_output(["git", "-C", str(path), "rev-parse", "HEAD"], text=True).strip()
    except (OSError, subprocess.CalledProcessError):
        return None


def git_worktree_dirty(path: Path) -> bool | None:
    try:
        return bool(subprocess.check_output(["git", "-C", str(path), "status", "--porcelain"], text=True).strip())
    except (OSError, subprocess.CalledProcessError):
        return None


def portable_path(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(ROOT.parent.resolve()))
    except ValueError:
        return str(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def report_reference(report_root: Path, name: str, value: dict[str, Any]) -> dict[str, Any]:
    """Return a portable identity and summary for a derived firmware report."""

    report_path = report_root / name
    reference = {
        "path": portable_path(report_path),
        "sha256": sha256(report_path),
        "schema": value.get("schema"),
    }
    if "summary" in value:
        reference["summary"] = value["summary"]
    return reference


def valid_vpp_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    for row in read_csv(path):
        if row.get("Register_Type") not in {"Hold", "Input"} or not row.get("Address", "").isdigit():
            continue
        address = int(row["Address"])
        count = int(row["Register_Count"] or "1")
        table = "holding" if row["Register_Type"] == "Hold" else "input"
        rows.append(
            {
                "table": table,
                "function_code": 3 if table == "holding" else 4,
                "address": address,
                "address_end": address + count - 1,
                "length_words": count,
                "name": row.get("Parameter_Name") or "Reserved",
                "access": row.get("Read_Write") or None,
                "data_type": row.get("Data_Type") or None,
                "unit_raw": row.get("Unit") or None,
                "range_notes": row.get("Range_Notes") or None,
                "source_row": row.get("NO") or None,
                "source_register_type": row.get("Register_Type"),
            }
        )
    return rows


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "reserved"


def normalized_unit(unit: str | None) -> tuple[float | None, str | None]:
    if not unit or unit == "-":
        return None, None
    match = re.fullmatch(r"([0-9]+(?:\.[0-9]+)?)(.*)", unit.strip())
    if match is None:
        return 1.0, unit
    return float(match.group(1)), match.group(2) or None


def access(value: str | None) -> str | None:
    return {"RO": "read", "RW": "read_write", "R": "read", "R/W": "read_write"}.get(value or "", value)


def source_row_id(row: dict[str, Any]) -> str:
    return f"growatt_vpp_v201:{row['table']}:{row['address']}"


def write_vpp_source(
    path: Path,
    csv_path: Path,
    rows: list[dict[str, Any]],
    *,
    source_id: str = "vendor_growatt_vpp_v201",
    title: str = "Growatt VPP communication protocol V2.01 register rows",
    revision: str = "V2.01",
    scope: str | None = None,
    source_pdf: Path | None = None,
) -> None:
    meta = {
        "source_id": source_id,
        "title": title,
        "revision": revision,
        "source_csv": portable_path(csv_path),
        "source_csv_sha256": sha256(csv_path),
        "redistribution": "normalized register rows only; source workbook/PDF remains external",
        **({"scope": scope} if scope else {}),
    }
    if source_pdf is not None:
        meta["source_pdf"] = portable_path(source_pdf)
        meta["source_pdf_sha256"] = sha256(source_pdf)
    dump(
        path,
        {
            "meta": meta,
            "rows": rows,
        },
    )


def write_modbus_snapshot(
    path: Path,
    modbus_root: Path,
    vpp_rows: list[dict[str, Any]],
    vpp_delta_rows: list[dict[str, Any]],
    firmware_root: Path,
) -> None:
    tracked = [
        modbus_root / "Protocols/growatt_vpp_protocol_v2.01_registers.csv",
        modbus_root / "Protocols/growatt_vpp_protocol_v2.03_delta.csv",
        modbus_root / "Protocols/growatt_modbus_rtu_v139_registers.csv",
        modbus_root / "custom_components/growatt_modbus/profiles/vpp_v201.py",
        modbus_root / "custom_components/growatt_modbus/profiles/wit.py",
        modbus_root / "custom_components/growatt_modbus/profiles/tl_xh.py",
        modbus_root / "custom_components/growatt_modbus/growatt_register_map.py",
    ]
    dump(
        path,
        {
            "meta": {
                "source_id": "growatt_modbus_tcp_register_source",
                "repository": "Growatt_ModbusTCP",
                "repository_revision": git_revision(modbus_root),
                "repository_worktree_dirty": git_worktree_dirty(modbus_root),
                "firmware_analysis_revision": git_revision(firmware_root),
                "role": "bidirectional source snapshot for GII reconciliation",
            },
            "artifacts": [{"path": portable_path(item), "sha256": sha256(item)} for item in tracked if item.exists()],
            "vpp_rows": vpp_rows,
            "vpp_v203_delta_rows": vpp_delta_rows,
        },
    )


def write_firmware_evidence(path: Path, firmware_root: Path) -> None:
    report = firmware_root / "reports/ZABA22/focused"
    legacy_join_path = report / "ZABA22_provider_register_join.json"
    memory = read_csv(report / "ZABA22_register_memory_map.csv")
    concordance = read_csv(report / "ZABA22_register_document_concordance.csv")
    providers = read_csv(report / "ZABA22_legacy_provider_cases.csv")
    writes = read_csv(report / "ZABA22_write_case_map.csv")
    profiles = read_csv(report / "ZABA22_vpp_profile_registers.csv")
    read_routes = load(report / "ZABA22_arm_read_provider_routes.json")
    legacy_read_semantics = load(report / "ZABA22_legacy_read_semantics.json")
    legacy_memory_provider = load(report / "ZABA22_legacy_memory_provider.json")
    legacy_compound_provider = load(
        report / "ZABA22_legacy_compound_provider.json"
    )
    legacy_transform_provider = load(report / "ZABA22_legacy_transform_provider.json")
    legacy_typed_concat_provider = load(
        report / "ZABA22_legacy_typed_concat_provider.json"
    )
    legacy_typed_concat_semantics = load(
        report / "ZABA22_legacy_typed_concat_semantics.json"
    )
    fc03_10000_provider = load(report / "ZABA22_fc03_10000_provider.json")
    linear_read_provider = load(report / "ZABA22_linear_read_provider.json")
    capture_conformance = load(report / "ZABA22_capture_conformance_aggregate.json")
    vpp_access_matrix = load(report / "ZABA22_vpp_register_access_matrix.json")
    vpp_conformance = load(report / "ZABA22_vpp_register_conformance.json")
    vpp_access_policy = load(report / "ZABA22_vpp_access_policy_audit.json")
    vpp_control_register_evidence = load(
        report / "ZABA22_vpp_control_register_evidence.json"
    )
    fc20_channel0 = load(report / "ZABA22_channel0_response_parser.json")
    fc20_provider_correlations = load(report / "ZABA22_fc20_provider_correlations.json")
    fc20_producer_boundary = load(report / "ZABA22_fc20_producer_boundary.json")
    fc20_state_effects = load(report / "ZABA22_fc20_fc22_state_effects.json")
    operation_conformance = load(report / "ZABA22_function_operation_conformance.json")
    legacy_register_join = load(legacy_join_path)
    source_files = [
        firmware_root / "ALBA18/ZABA22-payload.bin",
        report / "ZABA22_register_memory_map.csv",
        report / "ZABA22_register_document_concordance.csv",
        report / "ZABA22_legacy_provider_cases.csv",
        report / "ZABA22_write_case_map.csv",
        report / "ZABA22_register_conflicts.md",
        report / "ZABA22_vpp_profile_registers.csv",
        report / "ZABA22_arm_read_provider_routes.json",
        report / "ZABA22_legacy_read_semantics.json",
        report / "ZABA22_legacy_memory_provider.json",
        report / "ZABA22_legacy_compound_provider.json",
        report / "ZABA22_legacy_transform_provider.json",
        report / "ZABA22_legacy_typed_concat_provider.json",
        report / "ZABA22_legacy_typed_concat_semantics.json",
        report / "ZABA22_fc03_10000_provider.json",
        report / "ZABA22_linear_read_provider.json",
        report / "ZABA22_capture_conformance_aggregate.json",
        report / "ZABA22_vpp_register_access_matrix.json",
        report / "ZABA22_vpp_register_conformance.json",
        report / "ZABA22_vpp_access_policy_audit.json",
        report / "ZABA22_vpp_control_register_evidence.json",
        report / "ZABA22_channel0_response_parser.json",
        report / "ZABA22_fc20_provider_correlations.json",
        report / "ZABA22_fc20_producer_boundary.json",
        report / "ZABA22_fc20_fc22_state_effects.json",
        report / "ZABA22_function_operation_conformance.json",
        legacy_join_path,
    ]
    direct_routes = [
        {
            "table": "holding",
            "function_code": 3,
            "address_start": 30000,
            "address_end": 30498,
            "storage_symbol": "ZABA22_FC03_VPP_HOLDING_TABLE_PTR",
            "offset_formula": "2 * (address - 30000)",
            "guard": "complete request remains at or below 0x7723; single-word direct coverage ends at 30498",
            "evidence": "modbus_fc03_register_table_read at 0x0802a594; literal 0x0802ae24",
            "confidence": "high",
        },
        {
            "table": "input",
            "function_code": 4,
            "address_start": 31000,
            "address_end": 31299,
            "storage_symbol": "ZABA22_FC04_VPP_INPUT_TABLE_PTR",
            "offset_formula": "2 * (address - 31000)",
            "guard": "complete request remains below 0x7a45; single-word direct coverage ends at 31299",
            "evidence": "modbus_fc04_input_read at 0x0801e756; literal 0x0802ae28",
            "confidence": "high",
        },
    ]
    provider_ranges = [
        {
            "function_code": 3,
            "address_start": 5000,
            "address_end": 5079,
            "provider": "modbus_fc03_legacy_5000_window_read",
            "storage_formula": "DAT_08025620 + DAT_0802561c + 2 * address",
            "confidence": "high",
        },
        {
            "function_code": 3,
            "address_start": 5400,
            "address_end": 7959,
            "provider": "modbus_register_window_read",
            "storage_formula": "DAT_0802a588 + DAT_0802a550 + 2 * address",
            "confidence": "high",
        },
        {
            "function_code": 3,
            "address_start": 10000,
            "address_end": 10125,
            "provider": "modbus_fc03_10000_status_read",
            "storage_formula": "provider switch at 0x080279c0",
            "confidence": "high",
        },
        {
            "function_code": 3,
            "address_start": 40000,
            "address_end": 41000,
            "provider": "modbus_fc03_40000_window_read",
            "storage_formula": "DAT_08027cbc + 2 * (address - 40000)",
            "confidence": "high",
        },
        {
            "function_code": 4,
            "address_start": 4000,
            "address_end": 4107,
            "provider": "modbus_fc04_input_read",
            "storage_formula": "DAT_08025624 + DAT_08025628 + 2 * address + field adjustment",
            "confidence": "high",
        },
        {
            "function_code": 4,
            "address_start": 5080,
            "address_end": 5319,
            "provider": "modbus_fc04_input_read",
            "storage_formula": "DAT_0802a590 + DAT_0802a58c + 2 * address",
            "confidence": "high",
        },
    ]
    selected = [
        row
        for row in memory
        if row.get("firmware_route") or row.get("firmware_read_evidence") or row.get("firmware_write_evidence")
    ]
    dump(
        path,
        {
            "meta": {
                "source_id": "zaba22_firmware_register_correlation",
                "model": "Growatt MIN 2.5-6KTL-XH/XH2 ALBA18/ZABA22",
                "analysis_type": "static firmware reverse engineering",
                "hardware_policy": "no hardware access; firmware copies and derived reports only",
                "firmware_root": "external/growatt-firmware",
                "firmware_revision": git_revision(firmware_root),
                "input_hashes": {
                    str(item.relative_to(firmware_root)): sha256(item) for item in source_files if item.exists()
                },
                "limitations": [
                    "Provider symbols are not runtime RAM addresses until indirect pointer resolution is recovered.",
                    "Direct holding-table evidence is bounded by the firmware request guard through address 30498 for single-word reads; 30499 falls through.",
                    "Direct input-table evidence is bounded by the firmware request guard through address 31299 for single-word reads; 31300 falls through.",
                    "Write cases describe recovered firmware branches; they are not hardware write experiments.",
                    "Holding and input identities remain separate even when numeric addresses match.",
                    "No address-specific fallback case was recovered for input 31300..31399, input 31500..31599 or holding 32000..32099 in the scoped provider artifacts; fallback behavior remains unresolved.",
                    "The memory-backed provider evaluates caller-supplied SRAM snapshots; it does not prove stock initialization, producer ownership, scaling, persistence or write behavior.",
                    "The capture aggregate proves only the listed offline replay comparisons; response-derived FC20 fixtures, unobserved states and physical timing remain unresolved.",
                ],
            },
            "direct_routes": direct_routes,
            "read_provider_routes": read_routes["routes"],
            "post_table_case_search": read_routes["post_table_case_search"],
            "read_provider_report_sha256": sha256(report / "ZABA22_arm_read_provider_routes.json"),
            "legacy_read_semantics_report_sha256": sha256(
                report / "ZABA22_legacy_read_semantics.json"
            ),
            "legacy_memory_provider_report_sha256": sha256(
                report / "ZABA22_legacy_memory_provider.json"
            ),
            "legacy_compound_provider_report_sha256": sha256(
                report / "ZABA22_legacy_compound_provider.json"
            ),
            "legacy_transform_provider_report_sha256": sha256(
                report / "ZABA22_legacy_transform_provider.json"
            ),
            "legacy_typed_concat_provider_report_sha256": sha256(
                report / "ZABA22_legacy_typed_concat_provider.json"
            ),
            "legacy_typed_concat_semantics_report_sha256": sha256(
                report / "ZABA22_legacy_typed_concat_semantics.json"
            ),
            "fc03_10000_provider_report_sha256": sha256(
                report / "ZABA22_fc03_10000_provider.json"
            ),
            "linear_read_provider_report_sha256": sha256(
                report / "ZABA22_linear_read_provider.json"
            ),
            "capture_conformance_report_sha256": sha256(
                report / "ZABA22_capture_conformance_aggregate.json"
            ),
            "arm_modbus_reconstruction": {
                "schema": "gii.zaba22.arm-modbus-reconstruction.v1",
                "scope": "public-safe static correlation of ZABA22 ARM Modbus routes and FC20 runtime state",
                "source_reports": {
                    "vpp_access_matrix": report_reference(
                        report, "ZABA22_vpp_register_access_matrix.json", vpp_access_matrix
                    ),
                    "vpp_conformance": report_reference(
                        report, "ZABA22_vpp_register_conformance.json", vpp_conformance
                    ),
                    "vpp_access_policy": report_reference(
                        report, "ZABA22_vpp_access_policy_audit.json", vpp_access_policy
                    ),
                    "vpp_control_register_evidence": report_reference(
                        report,
                        "ZABA22_vpp_control_register_evidence.json",
                        vpp_control_register_evidence,
                    ),
                    "fc20_channel0_parser": report_reference(
                        report, "ZABA22_channel0_response_parser.json", fc20_channel0
                    ),
                    "fc20_provider_correlations": report_reference(
                        report, "ZABA22_fc20_provider_correlations.json", fc20_provider_correlations
                    ),
                    "fc20_producer_boundary": report_reference(
                        report, "ZABA22_fc20_producer_boundary.json", fc20_producer_boundary
                    ),
                    "fc20_state_effects": report_reference(
                        report, "ZABA22_fc20_fc22_state_effects.json", fc20_state_effects
                    ),
                    "function_operation_conformance": report_reference(
                        report, "ZABA22_function_operation_conformance.json", operation_conformance
                    ),
                    "legacy_typed_concat_provider": report_reference(
                        report,
                        "ZABA22_legacy_typed_concat_provider.json",
                        legacy_typed_concat_provider,
                    ),
                    "legacy_compound_provider": report_reference(
                        report,
                        "ZABA22_legacy_compound_provider.json",
                        legacy_compound_provider,
                    ),
                    "legacy_typed_concat_semantics": report_reference(
                        report,
                        "ZABA22_legacy_typed_concat_semantics.json",
                        legacy_typed_concat_semantics,
                    ),
                },
                "vpp": {
                    "access_matrix": {
                        "schema": vpp_access_matrix["schema"],
                        "scope": vpp_access_matrix["scope"],
                        "summary": vpp_access_matrix["summary"],
                        "rows": vpp_access_matrix["rows"],
                    },
                    "conformance": {
                        "schema": vpp_conformance["schema"],
                        "scope": vpp_conformance["scope"],
                        "summary": vpp_conformance["summary"],
                        "rows": vpp_conformance["rows"],
                        "limitations": vpp_conformance["limitations"],
                    },
                    "v203_access_policy": {
                        "schema": vpp_access_policy["schema"],
                        "scope": vpp_access_policy["scope"],
                        "summary": vpp_access_policy["summary"],
                        "target_addresses": vpp_access_policy["target_addresses"],
                        "rows": vpp_access_policy["rows"],
                    },
                    "control_register_evidence": {
                        "schema": vpp_control_register_evidence["schema"],
                        "scope": vpp_control_register_evidence["scope"],
                        "summary": vpp_control_register_evidence["summary"],
                        "rows": vpp_control_register_evidence["rows"],
                        "interpretation_boundary": vpp_control_register_evidence[
                            "interpretation_boundary"
                        ],
                    },
                },
                "fc20": {
                    "channel0_parser": {
                        "schema": fc20_channel0["schema"],
                        "framing": fc20_channel0["framing"],
                        "request_builder": fc20_channel0["request_builder"],
                        "response_layout": fc20_channel0["response_layout"],
                        "common_runtime_object": fc20_channel0["common_runtime_object"],
                        "confidence_boundary": fc20_channel0["confidence_boundary"],
                    },
                    "provider_correlations": fc20_provider_correlations,
                    "producer_boundary": fc20_producer_boundary,
                    "state_effects": fc20_state_effects,
                },
                "operation_conformance": {
                    "schema": operation_conformance["schema"],
                    "replay_summary": operation_conformance["replay_summary"],
                    "rows": operation_conformance["rows"],
                    "limitations": operation_conformance["limitations"],
                },
                "legacy_register_join": {
                    "schema": legacy_register_join["schema"],
                    "scope": "hash-pinned ZABA22 provider/register join; documentation names remain separate",
                    "source_report": portable_path(legacy_join_path),
                    "source_report_sha256": sha256(legacy_join_path),
                    "rows": [
                        {
                            "table": row["table"],
                            "address": row["public_address"],
                            "address_end": row["address_end"],
                            "function_code": row["function_code"],
                            "evidence_class": row["evidence_class"],
                            "firmware_route": row.get("firmware_route"),
                            "firmware_offset": row.get("firmware_offset"),
                            "firmware_offset_formula": row.get("firmware_offset_formula"),
                            "firmware_storage_symbol": row.get("firmware_storage_symbol"),
                            "firmware_write_evidence": row.get("firmware_write_evidence"),
                            "pointer_status": row.get("pointer_status"),
                            "pointer_targets": row.get("pointer_targets", []),
                            "capture_confidence": (row.get("capture_observation") or {}).get("confidence"),
                            "capture_observation_count": (row.get("capture_observation") or {}).get("observation_count", 0),
                        }
                        for row in legacy_register_join["rows"]
                    ],
                },
                "legacy_compound_provider": legacy_compound_provider,
                "interpretation": {
                    "vpp_rows": "Each row retains documentation identity and the recovered firmware read/write class; source-only documentation is not promoted to implemented behavior.",
                    "fc20": "The public FC20/FC22 path is kept separate from the internal 0x64 producer discriminator; protocol bookkeeping writes are not classified as inverter-register writes.",
                    "confidence": "Names and units remain documentation correlations unless the firmware report supplies an address-specific storage or data-flow match.",
                },
            },
            "provider_ranges": provider_ranges,
            "register_memory_evidence": selected,
            "profile_register_rows": profiles,
            "provider_case_count": len(providers),
            "provider_cases_with_documentation_match": sum(bool(row.get("documented_names")) for row in providers),
            "write_cases": writes,
            "documented_concordance_row_count": len(concordance),
            "conflict_report": "external/growatt-firmware/reports/ZABA22/focused/ZABA22_register_conflicts.md",
            "conflict_report_sha256": sha256(report / "ZABA22_register_conflicts.md"),
            "legacy_read_semantics": legacy_read_semantics,
            "legacy_memory_provider": legacy_memory_provider,
            "legacy_compound_provider": legacy_compound_provider,
            "legacy_transform_provider": legacy_transform_provider,
            "legacy_typed_concat_provider": legacy_typed_concat_provider,
            "legacy_typed_concat_semantics": legacy_typed_concat_semantics,
            "fc03_10000_provider": fc03_10000_provider,
            "linear_read_provider": linear_read_provider,
            "capture_conformance": capture_conformance,
        },
    )


def vpp_firmware_correlations(
    firmware_evidence: dict[str, Any],
    *,
    table: str,
    function_code: int,
    address: int,
) -> list[dict[str, Any]]:
    """Return address-specific ARM evidence without promoting source names.

    The VPP source rows and the firmware matrix answer different questions.
    Keep the join explicit in the generated spec so consumers can display the
    firmware route beside the documented name and still see that the name is
    source-derived.
    """

    projection = firmware_evidence.get("arm_modbus_reconstruction", {})
    vpp = projection.get("vpp", {}) if isinstance(projection, dict) else {}
    matrix = vpp.get("access_matrix", {}) if isinstance(vpp, dict) else {}
    matrix_rows = matrix.get("rows", []) if isinstance(matrix, dict) else []
    source_report = projection.get("source_reports", {}).get("vpp_access_matrix", {}) if isinstance(projection, dict) else {}
    matches = []
    for row in matrix_rows:
        if row.get("table") != table:
            continue
        # The generated matrix is keyed by table; retain the public function
        # code in the spec correlation even though the matrix omits it.
        if (3 if table == "holding" else 4) != function_code:
            continue
        if not int(row["address_start"]) <= address <= int(row["address_end"]):
            continue
        evidence_classes = list(row.get("evidence_classes", []))
        if "proven_direct_table_route" in evidence_classes:
            confidence = "high"
        elif "documented_address_unresolved_in_firmware" in evidence_classes:
            confidence = "unresolved"
        else:
            confidence = "medium"
        matches.append(
            {
                "kind": "zaba22_arm_modbus_correlation",
                "table": table,
                "function_code": function_code,
                "address_start": int(row["address_start"]),
                "address_end": int(row["address_end"]),
                "firmware_confidence": confidence,
                "firmware_read_status": list(row.get("firmware_read_status", [])),
                "firmware_write_status": row.get("firmware_write_status"),
                "firmware_routes": list(row.get("firmware_routes", [])),
                "evidence_classes": evidence_classes,
                "firmware_offset_formulas": list(row.get("firmware_offset_formulas", [])),
                "firmware_storage_pointer_symbol": row.get("firmware_storage_pointer_symbol"),
                "firmware_storage_pointer_target": row.get("firmware_storage_pointer_target"),
                "firmware_resolved_byte_formula": row.get("firmware_resolved_byte_formula"),
                "firmware_resolved_byte_range": row.get("firmware_resolved_byte_range"),
                "write_cases": row.get("write_cases", []),
                "source_report": source_report.get("path"),
                "source_report_sha256": source_report.get("sha256"),
                "semantic_name_confidence": "source_correlation_only",
            }
        )
    if not matches:
        # Keep an explicit negative evidence record for documented VPP rows
        # outside the scoped matrix (for example holding 32000..32099).
        matches.append(
            {
                "kind": "zaba22_arm_modbus_correlation",
                "table": table,
                "function_code": function_code,
                "address_start": address,
                "address_end": address,
                "firmware_confidence": "unresolved",
                "firmware_read_status": ["not_established_in_scoped_artifacts"],
                "firmware_write_status": "no_address_specific_case_recovered",
                "firmware_routes": [],
                "evidence_classes": ["documented_address_unresolved_in_firmware"],
                "firmware_offset_formulas": [],
                "firmware_storage_pointer_symbol": None,
                "firmware_storage_pointer_target": None,
                "firmware_resolved_byte_formula": None,
                "firmware_resolved_byte_range": None,
                "write_cases": [],
                "source_report": source_report.get("path"),
                "source_report_sha256": source_report.get("sha256"),
                "semantic_name_confidence": "source_correlation_only",
            }
        )
    return matches


def legacy_firmware_correlation(
    firmware_evidence: dict[str, Any],
    *,
    table: str,
    function_code: int,
    address: int,
    address_end: int,
) -> dict[str, Any]:
    """Join a legacy documentation row to the hash-pinned ARM provider join."""

    projection = firmware_evidence.get("arm_modbus_reconstruction", {})
    index = projection.get("legacy_register_join", {})
    index_rows = index.get("rows", []) if isinstance(index, dict) else []
    matches = [
        row
        for row in index_rows
        if row.get("table") == table
        and int(address) <= int(row["address"]) <= int(address_end)
    ]
    source_report = index.get("source_report") if isinstance(index, dict) else None
    source_report_sha256 = index.get("source_report_sha256") if isinstance(index, dict) else None
    matched_addresses = [int(row["address"]) for row in matches]
    evidence_classes = {
        str(row["evidence_class"])
        for row in matches
        if row.get("evidence_class")
    }
    if not matches:
        firmware_confidence = "unresolved"
        read_status = ["not_established_in_scoped_artifacts"]
    elif evidence_classes <= {
        "proven_explicit_provider_case",
        "proven_direct_table_route",
    }:
        firmware_confidence = "high_for_recovered_route"
        read_status = ["provider_or_direct_route"]
    elif any(str(item).startswith("proven_") for item in evidence_classes):
        firmware_confidence = "medium_for_provider_route"
        read_status = ["provider_route_with_storage_or_semantic_limit"]
    else:
        firmware_confidence = "unresolved"
        read_status = ["provider_route_not_established"]
    write_status = "not_established"
    return {
        "kind": "zaba22_arm_legacy_register_correlation",
        "table": table,
        "function_code": function_code,
        "address_start": int(address),
        "address_end": int(address_end),
        "expected_word_count": int(address_end) - int(address) + 1,
        "matched_word_count": len(matches),
        "matched_addresses": matched_addresses,
        "firmware_confidence": firmware_confidence,
        "firmware_read_status": read_status,
        "firmware_write_status": write_status,
        "evidence_classes": sorted(evidence_classes),
        "firmware_routes": sorted(
            {row["firmware_route"] for row in matches if row.get("firmware_route")}
        ),
        "firmware_offset_formulas": sorted(
            {
                row["firmware_offset_formula"]
                for row in matches
                if row.get("firmware_offset_formula")
            }
        ),
        "firmware_storage_symbols": sorted(
            {
                row["firmware_storage_symbol"]
                for row in matches
                if row.get("firmware_storage_symbol")
            }
        ),
        "capture_confidences": sorted(
            {row["capture_confidence"] for row in matches if row.get("capture_confidence")}
        ),
        "capture_observation_count": sum(
            int(row.get("capture_observation_count", 0)) for row in matches
        ),
        "source_report": source_report,
        "source_report_sha256": source_report_sha256,
        "semantic_name_confidence": "source_correlation_only",
    }


def add_vpp_to_consolidated(
    path: Path,
    source_artifact: str,
    rows: list[dict[str, Any]],
    firmware_evidence: dict[str, Any],
) -> None:
    candidate = load(path)
    candidate["source_documents"] = [
        item for item in candidate.get("source_documents", []) if item.get("document_id") != "vendor_growatt_vpp_v201"
    ]
    candidate["family_metadata"] = [
        item for item in candidate.get("family_metadata", []) if item.get("id") != "min_tl_xh_vpp"
    ]
    candidate["applicability"] = [
        item for item in candidate["applicability"] if item.get("declaration_id") != "vpp-v201-min-tl-xh"
    ]
    candidate["applicability_paths"] = [
        item for item in candidate["applicability_paths"] if item.get("declaration_id") != "vpp-v201-min-tl-xh"
    ]
    candidate["source_native_blocks"] = [
        item for item in candidate["source_native_blocks"] if not item.get("source_block_id", "").startswith("v124-vpp-v201-")
    ]
    candidate["blocks"] = [
        item for item in candidate["blocks"] if not item.get("consolidated_block_id", "").startswith("cb-vpp-v201-")
    ]
    candidate["registers"] = [
        item for item in candidate["registers"] if not item.get("register_id", "").startswith("growatt_vpp_v201:")
    ]
    candidate.setdefault("source_documents", []).append(
        {
            "document_id": "vendor_growatt_vpp_v201",
            "revision": "V2.01",
            "source_claim_artifact": source_artifact,
            "source_status": "normalized_rows_with_static_firmware_correlation",
        }
    )
    candidate.setdefault("family_metadata", []).append(
        {
            "id": "min_tl_xh_vpp",
            "name": "MIN/TL-XH/XH2 VPP V2.01",
            "models": ["MIN 2.5-6KTL-XH", "MIN TL-XH", "MIN TL-XH2", "TL-XH"],
            "protocol_group": "VPP V2.01",
            "notes": "VPP source rows are retained separately from legacy V1.24 blocks; XH/XH2 profile alternatives remain in evidence.",
        }
    )
    declaration_id = "vpp-v201-min-tl-xh"
    if not any(item.get("declaration_id") == declaration_id for item in candidate["applicability"]):
        candidate["applicability"].append(
            {
                "declaration_id": declaration_id,
                "family_id": "min_tl_xh_vpp",
                "family_label": "MIN/TL-XH/XH2 VPP V2.01",
                "page": None,
                "ranges": [],
                "raw_text": "Growatt VPP Protocol V2.01 rows correlated with ZABA22 firmware; model-specific alternatives remain separate evidence.",
                "source_scope": "vpp_v201",
            }
        )
    groups: dict[tuple[str, int, int], list[dict[str, Any]]] = {}
    for row in rows:
        start = row["address"]
        if row["table"] == "holding":
            block_range = (30000, 30499) if start < 30500 else (30500, 30999) if start < 32000 else (32000, 32099)
        elif start < 31300:
            block_range = (31000, 31299)
        elif start < 31400:
            block_range = (31300, 31399)
        elif start < 31500:
            block_range = (31400, 31499)
        else:
            block_range = (31500, 31599)
        groups.setdefault((row["table"], *block_range), []).append(row)
    declaration = next(item for item in candidate["applicability"] if item["declaration_id"] == declaration_id)
    for (table, start, end), group in sorted(groups.items()):
        block_suffix = f"{table}-{start}-{end}"
        block_id = f"cb-vpp-v201-{block_suffix}"
        native_id = f"v124-vpp-v201-{block_suffix}"
        if any(item.get("consolidated_block_id") == block_id for item in candidate["blocks"]):
            continue
        function_code = 3 if table == "holding" else 4
        declaration["ranges"].append({"start": start, "end": end, "table": table, "function_code": function_code})
        path_item = {
            "consolidated_block_id": block_id,
            "declaration_id": declaration_id,
            "declared_end": end,
            "declared_start": start,
            "family_id": "min_tl_xh_vpp",
            "family_label": "MIN/TL-XH/XH2 VPP V2.01",
            "function_code": function_code,
            "qualifier": None,
            "source_block_id": native_id,
            "source_scope": "vpp_v201",
            "table": table,
        }
        candidate["applicability_paths"].append(path_item)
        registers = []
        claim_refs = []
        for row in group:
            register_id = source_row_id(row)
            claim_refs.append(register_id)
            scale, unit = normalized_unit(row["unit_raw"])
            signed = str(row["data_type"] or "").upper().startswith("INT")
            encoding = "reserved/raw register" if row["data_type"] in {"-", None} else row["data_type"]
            if scale not in {None, 1.0}:
                encoding = f"{encoding} / {int(round(1 / scale)) if scale < 1 else scale}"
            divisor = 1 / scale if scale not in {None, 0, 1.0} else None
            registers.append(
                {
                    "register_id": register_id,
                    "consolidated_block_id": block_id,
                    "table": table,
                    "function_code": row["function_code"],
                    "address": row["address"],
                    "address_end": row["address_end"],
                    "applicability_paths": [{"source_scope": "vpp_v201", "declared_start": start, "declared_end": end, "qualifier": None}],
                    "conflict_refs": [],
                    "other_evidence": vpp_firmware_correlations(
                        firmware_evidence,
                        table=table,
                        function_code=row["function_code"],
                        address=row["address"],
                    ),
                    "consolidated": {
                        "access": access(row["access"]),
                        "description": row["name"],
                        "divisor": divisor,
                        "multiplier": scale,
                        "name": row["name"],
                        "range_raw": row["range_notes"],
                        "scale": scale,
                        "semantic_key": f"vpp_v201.{table}.{row['address']}",
                        "signed": signed,
                        "unit": unit,
                    },
                    "current_canonical": [
                        {
                            "access": access(row["access"]),
                            "description": row["name"],
                            "divisor": divisor,
                            "family": "min_tl_xh_vpp",
                            "multiplier": scale,
                            "name": row["name"],
                            "physical_id": f"min_tl_xh_vpp:{table}:{row['address']}",
                            "quantity": f"vpp_v201.{table}.{row['address']}",
                            "raw_type": encoding,
                            "resolution_confidence": "medium",
                            "resolution_status": "source_only",
                            "scale": scale,
                            "signed": signed,
                            "source_provenance": ["vendor_vpp_v201"],
                            "unit": unit,
                            "write_policy": "conditional" if access(row["access"]) == "read_write" else "read_only",
                        }
                    ],
                    "status": "SOURCE_ONLY",
                    "ha_readiness": "NOT_READY",
                    "vendor": {
                        "claim_id": register_id,
                        "source_row_id": str(row["source_row"]),
                        "address_raw": str(row["address"]),
                        "variable_raw": row["name"],
                        "description_raw": row["name"],
                        "value_raw": row["access"],
                        "unit_raw": row["unit_raw"],
                        "page": None,
                        "page_end": None,
                    },
                }
            )
        candidate["source_native_blocks"].append(
            {
                "source_block_id": native_id,
                "table": table,
                "function_code": function_code,
                "address_start": start,
                "address_end": end,
                "page_start": None,
                "page_end": None,
                "vendor_heading_raw": f"Growatt VPP V2.01 {table} registers {start}-{end}",
                "vendor_group_label_raw": "VPP V2.01",
                "normalized_role": "vpp_registers",
                "role_status": "source_only",
                "rows": claim_refs,
                "source_document_id": "vendor_growatt_vpp_v201",
                "source_artifact": source_artifact,
                "reviewed_evidence_claims": [],
                "address_bounds_status": "complete_for_extracted_rows",
            }
        )
        candidate["blocks"].append(
            {
                "consolidated_block_id": block_id,
                "table": table,
                "function_code": function_code,
                "address_start": start,
                "address_end": end,
                "register_ids": [item["register_id"] for item in registers],
                "applicability_paths": [path_item],
                "equivalence": "VPP_SOURCE_ONLY",
            }
        )
        candidate["registers"].extend(registers)
    for register in candidate["registers"]:
        address = register.get("address")
        if address is None or int(address) >= 30000:
            continue
        address_end = register.get("address_end")
        if address_end is None:
            address_end = address
        register["other_evidence"] = [
            item
            for item in register.get("other_evidence", [])
            if item.get("kind") != "zaba22_arm_legacy_register_correlation"
        ]
        register.setdefault("other_evidence", []).append(
            legacy_firmware_correlation(
                firmware_evidence,
                table=register["table"],
                function_code=int(register["function_code"]),
                address=int(address),
                address_end=int(address_end),
            )
        )
    path.write_text(json.dumps(candidate, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--modbus-root", type=Path, default=DEFAULT_MODBUS)
    parser.add_argument("--firmware-root", type=Path, default=DEFAULT_FIRMWARE)
    parser.add_argument("--no-consolidated", action="store_true")
    args = parser.parse_args()
    vpp_csv = args.modbus_root / "Protocols/growatt_vpp_protocol_v2.01_registers.csv"
    vpp_delta_csv = args.modbus_root / "Protocols/growatt_vpp_protocol_v2.03_delta.csv"
    rows = valid_vpp_rows(vpp_csv)
    delta_rows = valid_vpp_rows(vpp_delta_csv)
    vpp_source = ROOT / "sources/vendor/growatt-vpp-v2.01-registers.json"
    write_vpp_source(vpp_source, vpp_csv, rows)
    vpp_delta_source = ROOT / "sources/vendor/growatt-vpp-v2.03-delta.json"
    write_vpp_source(
        vpp_delta_source,
        vpp_delta_csv,
        delta_rows,
        source_id="vendor_growatt_vpp_v203_delta",
        title="Growatt VPP communication protocol V2.03 changed and added register rows",
        revision="V2.03",
        scope="MIN 2500-6000TL-XH/XH2/XHE/XA, DTC 5100; overlay only",
        source_pdf=ROOT / "tmp/VPP_Protocol_V2.03.pdf",
    )
    write_modbus_snapshot(
        ROOT / "sources/external/growatt-modbus-tcp-registers.snapshot.json",
        args.modbus_root,
        rows,
        delta_rows,
        args.firmware_root,
    )
    firmware_evidence_path = ROOT / "sources/evidence/zaba22-firmware-register-correlation.json"
    write_firmware_evidence(firmware_evidence_path, args.firmware_root)
    if not args.no_consolidated:
        add_vpp_to_consolidated(
            BLOCK_SOURCE,
            "sources/vendor/growatt-vpp-v2.01-registers.json",
            rows,
            load(firmware_evidence_path),
        )
    print(f"Imported {len(rows)} V2.01 rows, {len(delta_rows)} V2.03 delta rows and ZABA22 firmware evidence")


if __name__ == "__main__":
    main()
