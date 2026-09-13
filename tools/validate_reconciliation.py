#!/usr/bin/env python3
"""Validate declarative reconciliation and candidate invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
STATUSES = {"resolved", "provisionally_resolved", "unresolved", "not_applicable", "reserved", "scope_specific"}


def read(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def ranges(value: Any) -> list[tuple[int, int]]:
    found: list[tuple[int, int]] = []
    if isinstance(value, dict):
        bits = value.get("bits")
        if isinstance(bits, list) and len(bits) == 2 and all(isinstance(item, int) for item in bits): found.append((bits[0], bits[1]))
        for child in value.values(): found.extend(ranges(child))
    elif isinstance(value, list):
        for child in value: found.extend(ranges(child))
    return found


def validate_ranges(value: Any, prefix: str) -> list[str]:
    errors: list[str] = []
    found = ranges(value)
    for index, (low, high) in enumerate(found):
        if low < 0 or high < low or high > 15:
            errors.append(f"{prefix}: impossible packed range {low}..{high}")
        for other_low, other_high in found[index + 1:]:
            if low <= other_high and other_low <= high:
                errors.append(f"{prefix}: overlapping packed ranges {low}..{high} and {other_low}..{other_high}")
    return errors


def require_claims(
    support: list[str], prefixes: tuple[str, ...], prefix: str, property_name: str
) -> list[str]:
    if any(claim_id.startswith(candidate) for claim_id in support for candidate in prefixes):
        return []
    return [f"{prefix}: {property_name} lacks required claim-level support"]


def validate() -> list[str]:
    errors: list[str] = []
    claims = {item["claim_id"]: item for item in read("sources/claims/generic-claims.json")["claims"]}
    data = read("reconciliation/min_tl_xh.json")
    ids: set[str] = set()
    logical_objects: set[str] = {
        item["target"]["logical_object"]
        for item in data["decisions"]
        if item["target"].get("namespace") == "LOGICAL" and item["target"].get("logical_object")
    }
    for index, item in enumerate(data["decisions"]):
        prefix = f"decisions[{index}]"
        decision_id = item.get("decision_id")
        if not isinstance(decision_id, str): errors.append(f"{prefix}: missing decision_id")
        if decision_id in ids: errors.append(f"{prefix}: duplicate decision_id {decision_id}")
        ids.add(decision_id)
        target = item.get("target", {})
        namespace = target.get("namespace")
        if namespace == "MODBUS" and (target.get("table") not in {"holding", "input"} or not isinstance(target.get("address"), int)): errors.append(f"{prefix}: invalid MODBUS target")
        if namespace in {"LOGICAL", "GROWATT_FC0x20"} and not target.get("logical_object"): errors.append(f"{prefix}: logical target needs logical_object")
        status = item.get("decision", {}).get("status")
        if status not in STATUSES: errors.append(f"{prefix}: invalid decision status {status}")
        if not item.get("support") and status in {"resolved", "provisionally_resolved", "scope_specific"}: errors.append(f"{prefix}: resolved decision without support")
        for claim_id in [*item.get("support", []), *(rejection["claim_id"] for rejection in item.get("conflicts", []))]:
            if claim_id not in claims: errors.append(f"{prefix}: dangling claim reference {claim_id}")
            elif any(token in claims[claim_id]["provenance"].get("source_artifact", "") for token in ("spec/", "knowledge/compatibility/", "compatibility/")):
                errors.append(f"{prefix}: canonical/compatibility artifact used as evidence")
        scope = item.get("scope", {})
        if scope.get("family") != "min_tl_xh" or not scope.get("applicability"): errors.append(f"{prefix}: invalid scope")
        errors.extend(validate_ranges(item.get("decision", {}).get("value"), prefix))
        value_text = json.dumps(item.get("decision", {}).get("value", {}), ensure_ascii=False)
        if "encoding_template" in value_text:
            template_names = set(re.findall(r"xh_schedule_(?:start_control|end)_v124", value_text))
            if not template_names.issubset(logical_objects | {"xh_schedule_start_control_v124", "xh_schedule_end_v124"}):
                errors.append(f"{prefix}: dangling template reference")
        for rejection in item.get("conflicts", []):
            if not rejection.get("reason"): errors.append(f"{prefix}: rejection without reason")
        address = target.get("address")
        value = item.get("decision", {}).get("value", {})
        if address == 3000 and target.get("table") == "input" and "fields" in value:
            errors.extend(require_claims(item.get("support", []), ("vendor_growatt_v124_2020:assertion:vendor_growatt_v124_2020:input:p069-070:i3000:visual-review:enum",), prefix, "I3000 packed enum"))
        if address in {3036, 3037} and target.get("table") == "holding" and value.get("unit") == "%":
            errors.extend(require_claims(item.get("support", []), ("min_semantic_review:holding:", "openinverter_gateway:devices:GrowattTLXH:holding_registers:"), prefix, f"H{address} percentage interpretation"))
        if address == 3082 and target.get("table") == "holding" and value.get("unit") == "%":
            errors.extend(require_claims(item.get("support", []), ("min_semantic_review:holding:3082:",), prefix, "H3082 ratio-to-percentage normalization"))
        if address == 3166 and target.get("table") == "input" and "fields" in value:
            errors.extend(require_claims(item.get("support", []), ("vendor_growatt_v124_2020:assertion:vendor_growatt_v124_2020:input:p078:i3166:visual-review:enum",), prefix, "I3166 packed enum"))
        if address == 3000 and target.get("table") == "input":
            fields = {field.get("name"): field for field in value.get("fields", [])}
            if fields.get("mode", {}).get("bits") != [8, 15] or fields.get("status", {}).get("bits") != [0, 7]:
                errors.append(f"{prefix}: I3000 mode/status byte assignment is invalid")
            if set(fields.get("mode", {}).get("enum", {})) != {str(number) for number in range(9)}:
                errors.append(f"{prefix}: I3000 mode enum is incomplete or has extra values")
            if set(fields.get("status", {}).get("enum", {})) != {"0", "1", "3", "4"}:
                errors.append(f"{prefix}: I3000 status enum is incomplete or has extra values")
        if address == 3166 and target.get("table") == "input":
            fields = {field.get("name"): field for field in value.get("fields", [])}
            if fields.get("mode", {}).get("bits") != [8, 15] or fields.get("status", {}).get("bits") != [0, 7]:
                errors.append(f"{prefix}: I3166 mode/status byte assignment is invalid")
        if target.get("logical_object") == "xh_schedule_start_control_v124":
            fields = {field.get("name"): field for field in value.get("fields", [])}
            expected = {"minute": [0, 7], "hour": [8, 12], "priority": [13, 14], "enable": [15, 15]}
            if {name: field.get("bits") for name, field in fields.items()} != expected:
                errors.append(f"{prefix}: XH start/control codec is incomplete or misplaced")
    candidate = read("reconciliation/resolved-assertions.json")
    if candidate.get("canonical_status") != "shadow_only_not_canonical": errors.append("candidate is not marked shadow-only")
    if len(candidate.get("decisions", [])) != len(data["decisions"]): errors.append("candidate/decision count mismatch")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    errors = validate()
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("valid: reconciliation decisions and shadow candidate")


if __name__ == "__main__":
    main()
