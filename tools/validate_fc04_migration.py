#!/usr/bin/env python3
"""Validate the offline, bounded PIPELINE-5B FC04 migration artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

try:
    from tools.build_fc04_migration import (
        CLAIMS_PATH,
        END,
        FAMILY,
        RECONCILIATION_PATH,
        SHADOW_PATH,
        START,
        build_all,
    )
except ModuleNotFoundError:
    from build_fc04_migration import (
        CLAIMS_PATH,
        END,
        FAMILY,
        RECONCILIATION_PATH,
        SHADOW_PATH,
        START,
        build_all,
    )


def validate() -> list[str]:
    errors: list[str] = []
    expected = build_all()
    paths = (CLAIMS_PATH, RECONCILIATION_PATH, SHADOW_PATH)
    for path, data in zip(paths, expected):
        if not path.is_file():
            errors.append(f"missing artifact: {path}")
        elif json.loads(path.read_text(encoding="utf-8")) != data:
            errors.append(f"stale or non-deterministic artifact: {path}")
    if errors:
        return errors

    claims, reconciliation, shadow = expected
    claim_ids = [item["claim_id"] for item in claims["claims"]]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("claim IDs are not unique")
    source_ids = {item["source_id"] for item in claims["sources"]}
    if any(item["source_id"] not in source_ids for item in claims["claims"]):
        errors.append("claim references unknown source")
    if any("wc7c6o" in json.dumps(item, ensure_ascii=False) for item in claims["claims"]):
        errors.append("secret/token material found in claims")
    vendor_addresses = {
        item["subject"]["address"]
        for item in claims["claims"]
        if item["source_id"] == "vendor_v124_fc04"
        and item["subject"].get("table") == "input"
        and START <= item["subject"]["address"] <= END
    }
    if vendor_addresses != set(range(START, END + 1)):
        errors.append("vendor claims do not cover every FC04 physical address")
    physical = [item for item in reconciliation["decisions"] if item["target"].get("namespace") == "MODBUS"]
    addresses = [item["target"].get("address") for item in physical]
    if addresses != list(range(START, END + 1)):
        errors.append("reconciliation does not contain exactly one ordered physical decision per address")
    if shadow["parity"]["physical_identity"] != 250 or shadow["parity"]["source_shape"] != 250:
        errors.append("physical parity gate failed")
    forbidden = re.compile(r"(api[_ -]?key|access[_ -]?token|session[_ -]?cookie|password)\s*[:=]", re.I)
    for path in paths:
        if forbidden.search(path.read_text(encoding="utf-8")):
            errors.append(f"possible secret field in {path}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="kept for symmetry with the builder")
    parser.parse_args()
    errors = validate()
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("valid: bounded FC04 claims, reconciliation, parity, and public-safety checks pass")


if __name__ == "__main__":
    main()
