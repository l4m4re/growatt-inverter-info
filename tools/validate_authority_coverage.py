#!/usr/bin/env python3
"""Validate the generated PIPELINE-5A authority coverage inventory."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

try:
    from tools.build_authority_coverage import ORIGIN_CATEGORIES, OUTPUT_PATH, build
except ModuleNotFoundError:
    from build_authority_coverage import ORIGIN_CATEGORIES, OUTPUT_PATH, build


def validate(path: Path = OUTPUT_PATH) -> list[str]:
    expected = build()
    if not path.is_file():
        return [f"coverage artifact is missing: {path}"]
    actual = json.loads(path.read_text(encoding="utf-8"))
    errors: list[str] = []
    if actual != expected:
        errors.append("coverage artifact is stale or non-deterministic")
    canonical_count = expected["counts"]["canonical_records"]
    records = actual.get("records", [])
    if len(records) != canonical_count:
        errors.append(f"inventoried {len(records)} records, expected {canonical_count}")
    physical_ids = [record.get("physical_id") for record in records]
    if len(set(physical_ids)) != len(physical_ids):
        errors.append("duplicate canonical physical IDs in inventory")
    for record in records:
        if not isinstance(record.get("migration_class"), str) or not record["migration_class"]:
            errors.append(f"record has no migration class: {record.get('physical_id')}")
        if not set(record.get("missing_declarative_properties", [])) <= set(actual["authority_origin_metrics"]["by_property"]):
            errors.append(f"record has an unknown property name: {record.get('physical_id')}")
    for property_name, detail in actual["authority_origin_metrics"]["by_property"].items():
        for classification in detail["current_origin_counts"]:
            if classification not in ORIGIN_CATEGORIES:
                errors.append(f"{property_name} uses unknown origin category {classification}")
    if actual["declarative_coverage"]["physical_targets"] != 18:
        errors.append("the PIPELINE-4A diagnostic layer no longer reports 18 physical targets")
    if actual["authority_origin_metrics"]["unknown_origin_property_cells"] < 0:
        errors.append("unknown origin count is invalid")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=OUTPUT_PATH)
    args = parser.parse_args()
    errors = validate(args.input)
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print("valid: canonical authority coverage is current and complete")


if __name__ == "__main__":
    main()
