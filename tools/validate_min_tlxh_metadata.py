#!/usr/bin/env python3
"""Check obvious metadata contradictions in the canonical MIN/TL-XH view."""

# ruff: noqa: T201

import json
import re
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
SPEC_PATH = REPO / "spec" / "growatt-register-spec.json"

PRIMARY_RANGES = {
    "holding": ((3000, 3124),),
    "input": ((3000, 3374),),
}


def in_scope(record: dict[str, Any]) -> bool:
    return record["family"] == "min_tl_xh" and any(
        start <= record["address"] <= end
        for start, end in PRIMARY_RANGES[record["table"]]
    )


def normalized_unit(unit: str | None) -> str | None:
    """Return a base engineering unit while accepting source scale notation."""
    if not unit:
        return None
    value = unit.replace("℃", "°C").strip()
    match = re.fullmatch(r"(?:\d+(?:[.,]\d+)?\s*)?(V|A|W|kW|VA|var|Wh|kWh|kvarh|Hz|°C|Ah|pf|%)", value)
    return match.group(1) if match else value


def finding(record: dict[str, Any], kind: str, detail: str, severity: str) -> dict[str, Any]:
    return {
        "physical_id": record["physical_id"],
        "kind": kind,
        "detail": detail,
        "severity": severity,
    }


def check(spec: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    records = [record for record in spec["registers"] if in_scope(record)]
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    info: list[dict[str, Any]] = []
    seen: set[str] = set()

    for record in records:
        physical_id = record["physical_id"]
        if physical_id in seen:
            errors.append(finding(record, "duplicate_physical_identity", "physical_id occurs more than once", "error"))
        seen.add(physical_id)

        normalized = record["normalized"]
        name = (normalized.get("name") or "").lower()
        raw_type = normalized.get("raw_type", "").lower()
        raw_unit = normalized.get("unit")
        unit = normalized_unit(raw_unit)
        if raw_unit and unit == raw_unit and any(token in raw_unit for token in (":", "[", "]", "Not detected", "Detection")):
            warnings.append(finding(record, "range_or_enum_in_unit", f"unit contains range/enum text: {raw_unit}", "warning"))

        expected: set[str] | None = None
        if "voltage" in name:
            expected = {"V"}
        elif "current" in name:
            expected = {"A"}
        elif "power" in name and "factor" not in name:
            expected = {"W", "kW", "VA", "var", "%"}
        elif "energy" in name:
            expected = {"Wh", "kWh", "kvarh"}
        elif "frequency" in name and not any(token in name for token in ("delay", "slope")):
            expected = {"Hz"}
        elif "temperature" in name:
            expected = {"°C"}
        elif any(token in name for token in ("soc", "soh", "percentage")):
            expected = {"%"}
        if expected and unit is not None and unit not in expected:
            errors.append(finding(record, "semantic_unit_contradiction", f"{normalized.get('name')} has unit {raw_unit!r}; expected one of {sorted(expected)}", "error"))

        datatype_expected: set[str] | None = None
        if "voltage" in raw_type:
            datatype_expected = {"V"}
        elif "current" in raw_type:
            datatype_expected = {"A"}
        elif "temperature" in raw_type:
            datatype_expected = {"°C"}
        elif "percentage" in raw_type:
            datatype_expected = {"%"}
        if datatype_expected and unit is not None and unit not in datatype_expected:
            errors.append(finding(record, "datatype_unit_contradiction", f"{normalized.get('raw_type')} has unit {raw_unit!r}; expected one of {sorted(datatype_expected)}", "error"))

        if "factor" in name and unit not in (None, "pf"):
            errors.append(finding(record, "semantic_unit_contradiction", f"power-factor field has unit {raw_unit!r}", "error"))
        if normalized.get("raw_type", "").startswith("packed") and unit is not None:
            errors.append(finding(record, "packed_field_unit", f"packed field has engineering unit {raw_unit!r}", "error"))
        if record.get("bitfields") and unit is not None and unit not in {"%"}:
            warnings.append(finding(record, "bitfield_unit", f"bitfield has unit {raw_unit!r}", "warning"))

        if record.get("component_role") and record["length_words"] != 1:
            errors.append(finding(record, "component_length", "logical component must have length_words=1", "error"))
        if record["length_words"] > 1 and not record.get("logical_field_id"):
            errors.append(finding(record, "unrepresented_multiword", "multiword physical record has no logical field", "error"))

    fields = {field["id"]: field for field in spec["logical_fields"]}
    scoped_ids = {record["physical_id"] for record in records}
    for field in spec["logical_fields"]:
        physical = field["physical_registers"]
        if len(physical) < 2:
            continue
        if field.get("length_words") != len(physical):
            errors.append({"logical_field": field["id"], "kind": "logical_length", "detail": "length_words must equal physical-register count", "severity": "error"})
        addresses = [item["address"] for item in physical]
        if addresses != list(range(addresses[0], addresses[-1] + 1)):
            errors.append({"logical_field": field["id"], "kind": "logical_membership", "detail": "logical field members are not contiguous", "severity": "error"})
        for item in physical:
            if item["physical_id"] in scoped_ids:
                record = next(record for record in records if record["physical_id"] == item["physical_id"])
                if record.get("component_of") != field["id"]:
                    errors.append(finding(record, "logical_membership", "component_of does not match logical field", "error"))

    by_family_address: dict[tuple[str, int], set[str]] = {}
    for record in records:
        by_family_address.setdefault((record["family"], record["address"]), set()).add(record["table"])
    overlaps = [
        (family, address)
        for (family, address), tables in by_family_address.items()
        if tables == {"holding", "input"}
    ]
    if overlaps:
        info.append({"kind": "holding_input_overlap", "detail": f"{len(overlaps)} valid address overlaps remain namespace-separated", "severity": "info"})
    return {"errors": errors, "warnings": warnings, "info": info, "logical_fields": list(fields)}


def main() -> None:
    result = check(json.loads(SPEC_PATH.read_text(encoding="utf-8")))
    print(json.dumps({key: value for key, value in result.items() if key != "logical_fields"}, indent=2))
    if result["errors"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
