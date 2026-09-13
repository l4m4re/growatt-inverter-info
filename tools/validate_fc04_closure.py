#!/usr/bin/env python3
"""Validate the bounded PIPELINE-5C closure inventory offline."""

from __future__ import annotations

import argparse
import json
import re

try:
    from tools.build_fc04_closure import END, FAMILY, OUTPUT_PATH, RECONCILIATION_PATH, START, build
    from tools.build_fc04_migration import CLAIMS_PATH
except ModuleNotFoundError:
    from build_fc04_closure import END, FAMILY, OUTPUT_PATH, RECONCILIATION_PATH, START, build
    from build_fc04_migration import CLAIMS_PATH


def validate() -> list[str]:
    expected = build()
    errors: list[str] = []
    for path, data in ((OUTPUT_PATH, expected[0]), (RECONCILIATION_PATH, expected[1])):
        if not path.is_file() or json.loads(path.read_text(encoding="utf-8")) != data:
            errors.append(f"stale or missing artifact: {path}")
    if errors:
        return errors
    inventory, reconciliation = expected
    targets = inventory["targets"]
    if inventory["original_unresolved_count"] != 129 or len(targets) != 129:
        errors.append("closure inventory does not cover exactly the 129 5B unresolved targets")
    if [target["address"] for target in targets] != sorted(target["address"] for target in targets):
        errors.append("closure targets are not deterministic/ordered")
    if len(reconciliation["decisions"]) != 129:
        errors.append("closure reconciliation does not contain one decision per target")
    claim_ids = {claim["claim_id"] for claim in json.loads(CLAIMS_PATH.read_text(encoding="utf-8"))["claims"]}
    if any(claim_id not in claim_ids for target in targets for claim_id in target["source_claims"]):
        errors.append("closure target references an unknown source claim")
    if any(target["experiment"]["performed"] for target in targets) and not inventory["safety"]["shine_bound_only"]:
        errors.append("active experiment is not marked Shine-bound only")
    if inventory["safety"] != {"shine_bound_only": True, "local_ground_truth_modified": False, "intentional_inverter_writes": False, "counters_injected": False, "identity_injected": False}:
        errors.append("safety boundary changed")
    if re.search(r"wc7c6o|access[_ -]?token|session[_ -]?cookie", json.dumps(inventory), re.I):
        errors.append("possible secret material in closure inventory")
    physical_ids = {f"{FAMILY}:input:{address}" for address in range(START, END + 1)}
    if not set(target["physical_id"] for target in targets) <= physical_ids:
        errors.append("target outside cohort")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.parse_args()
    errors = validate()
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("valid: 5C closure inventory and reconciliation pass offline checks")


if __name__ == "__main__":
    main()
