#!/usr/bin/env python3
"""Validate generic claim identity and provenance invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
VALID_NAMESPACES = {"MODBUS", "GROWATT_FC0x20", "LOGICAL", "IMPLEMENTATION"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def pointer_exists(value: Any, pointer: str) -> bool:
    if pointer == "/":
        return True
    current = value
    for token in pointer.lstrip("/").split("/"):
        token = token.replace("~1", "/").replace("~0", "~")
        try:
            current = current[int(token)] if isinstance(current, list) else current[token]
        except (KeyError, IndexError, TypeError, ValueError):
            return False
    return True


def validate(path: Path) -> list[str]:
    data = load(path)
    errors: list[str] = []
    if data.get("schema_version") != "1.0.0": errors.append("schema_version must be 1.0.0")
    if data.get("artifact") != "growatt_generic_source_claims": errors.append("wrong artifact")
    registry_path = ROOT / "sources/claims/source-registry.json"
    registry = load(registry_path)
    sources = {entry["source_id"] for entry in registry["sources"]}
    ids: set[str] = set()
    for index, item in enumerate(data.get("claims", [])):
        prefix = f"claims[{index}]"
        claim_id = item.get("claim_id")
        if not isinstance(claim_id, str) or not claim_id: errors.append(f"{prefix}: missing claim_id")
        elif claim_id in ids: errors.append(f"{prefix}: duplicate claim_id {claim_id}")
        else: ids.add(claim_id)
        source_id = item.get("source_id")
        if source_id not in sources: errors.append(f"{prefix}: unknown source_id {source_id}")
        sub = item.get("subject", {})
        namespace = sub.get("namespace")
        if namespace not in VALID_NAMESPACES: errors.append(f"{prefix}: invalid subject namespace {namespace}")
        if namespace == "MODBUS":
            if sub.get("table") not in {"holding", "input"}: errors.append(f"{prefix}: MODBUS subject needs holding/input")
            if not isinstance(sub.get("address"), int): errors.append(f"{prefix}: MODBUS subject needs address")
            if sub.get("address_end") is not None and sub["address_end"] < sub["address"]: errors.append(f"{prefix}: reversed address range")
        elif namespace in {"LOGICAL", "IMPLEMENTATION", "GROWATT_FC0x20"} and not sub.get("logical_object"):
            errors.append(f"{prefix}: {namespace} subject needs logical_object")
        assertion = item.get("assertion", {})
        if not isinstance(assertion.get("kind"), str) or not assertion["kind"]: errors.append(f"{prefix}: missing assertion kind")
        if "value" not in assertion: errors.append(f"{prefix}: missing assertion value")
        provenance = item.get("provenance", {})
        if not provenance.get("source_artifact"): errors.append(f"{prefix}: missing source_artifact")
        artifact = ROOT / provenance.get("source_artifact", "")
        if not artifact.is_file(): errors.append(f"{prefix}: missing provenance artifact {provenance.get('source_artifact')}")
        pointer = provenance.get("json_pointer")
        if pointer is not None and artifact.is_file():
            try:
                if not pointer_exists(load(artifact), pointer): errors.append(f"{prefix}: dangling json_pointer {pointer}")
            except json.JSONDecodeError: errors.append(f"{prefix}: provenance artifact is not JSON")
        claim_scope = item.get("scope", {})
        if "family" not in claim_scope or "applicability" not in claim_scope: errors.append(f"{prefix}: incomplete scope")
        evidence = item.get("evidence", {})
        if not all(evidence.get(key) for key in ("method", "confidence", "status")): errors.append(f"{prefix}: incomplete evidence")
        bit_range = assertion.get("bit_range")
        if isinstance(bit_range, str) and ".." in bit_range:
            try:
                low, high = (int(value) for value in bit_range.split("..", 1))
                if low < 0 or high < low or high > 15: errors.append(f"{prefix}: impossible bit range {bit_range}")
            except ValueError: errors.append(f"{prefix}: invalid bit range {bit_range}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", nargs="?", default="sources/claims/generic-claims.json")
    args = parser.parse_args()
    errors = validate(ROOT / args.path)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    data = load(ROOT / args.path)
    print(f"valid: {len(data['claims'])} claims")


if __name__ == "__main__":
    main()
