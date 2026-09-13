#!/usr/bin/env python3
"""Validate public-safe Growatt vendor source-claim artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


def validate(path: Path, schema_path: Path) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    schema = json.loads(schema_path.read_text(encoding="utf-8"))
    errors = sorted(Draft202012Validator(schema).iter_errors(payload), key=lambda error: list(error.path))
    messages = [f"{'.'.join(str(part) for part in error.path)}: {error.message}" for error in errors]
    claims = payload.get("claims", [])
    claim_ids = [claim.get("claim_id") for claim in claims]
    duplicate_ids = sorted({claim_id for claim_id in claim_ids if claim_ids.count(claim_id) > 1})
    document = payload.get("document", {})
    cross_reference_errors: list[str] = []
    fragment_ids: set[str] = set()
    for claim in claims:
        if claim.get("document_id") != document.get("document_id"):
            cross_reference_errors.append(f"{claim.get('claim_id')}: document_id mismatch")
        if claim.get("document_sha256", "").lower() != document.get("document_sha256", "").lower():
            cross_reference_errors.append(f"{claim.get('claim_id')}: document_sha256 mismatch")
        for fragment in claim.get("source_fragments", []):
            fragment_ids.add(fragment.get("fragment_id"))
    for claim in claims:
        for reference in claim.get("continuation_refs", []):
            if reference not in fragment_ids:
                cross_reference_errors.append(f"{claim.get('claim_id')}: unresolved continuation {reference}")
    all_errors = messages + [f"duplicate claim_id: {claim_id}" for claim_id in duplicate_ids] + cross_reference_errors
    return {
        "path": str(path),
        "valid": not all_errors,
        "claim_count": len(claims),
        "unique_claim_ids": len(set(claim_ids)),
        "duplicate_claim_ids": duplicate_ids,
        "errors": all_errors,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims", type=Path, action="append", required=True)
    parser.add_argument("--schema", type=Path, default=Path("sources/claims/vendor/schema.json"))
    args = parser.parse_args()
    results = [validate(path, args.schema) for path in args.claims]
    print(json.dumps({"valid": all(result["valid"] for result in results), "files": results}, indent=2))
    if not all(result["valid"] for result in results):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
