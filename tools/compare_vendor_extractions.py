#!/usr/bin/env python3
"""Compare the historical flat V1.24 derivative with source claims."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def normalized(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def old_rows(payload: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for table in ("holding", "input"):
        for row in payload.get(table, []):
            expression = str(row.get("register", "")).strip()
            match = re.fullmatch(r"(\d+)\s*", expression)
            if match:
                rows.append({"table": table, "address": int(match.group(1)), "row": row})
            else:
                rows.append({"table": table, "address": None, "row": row})
    return rows


def claim_text(claim: dict[str, Any]) -> str:
    return normalized(" ".join(
        str(claim.get(key) or "")
        for key in ("raw_variable", "raw_description", "raw_value_text", "raw_unit_text", "raw_access_text", "raw_note")
    ))


def compare(old: dict[str, Any], new: dict[str, Any]) -> dict[str, Any]:
    indexed: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for claim in new.get("claims", []):
        address = claim.get("parsed_address")
        if address is not None:
            indexed.setdefault((claim["register_table"], address), []).append(claim)
    differences: list[dict[str, Any]] = []
    counts: dict[str, int] = {}
    for item in old_rows(old):
        key = (item["table"], item["address"]) if item["address"] is not None else None
        matches = indexed.get(key, []) if key else []
        old_text = claim_text(item["row"])
        if not matches:
            kind = "old_content_missing" if key else "old_row_ambiguous"
            detail = "No uniquely parsed new claim for the historical row."
        else:
            new_texts = {claim_text(claim) for claim in matches}
            if old_text in new_texts:
                kind = "same"
                detail = "Normalized source fields agree."
            elif any(normalized(item["row"].get("variable")) in normalized(claim.get("reconstructed_variable") or claim.get("raw_variable")) for claim in matches):
                kind = "reconstructed_word_split"
                detail = "The new claim preserves a source split and a reviewed/reconstructed form."
            elif any(len(claim.get("source_fragments", [])) > 1 for claim in matches):
                kind = "new_continuation_recovered"
                detail = "The new claim retains page-spanning source fragments."
            else:
                kind = "content_changed_or_layout_shift"
                detail = "Source text differs; this is not classified as a semantic correction."
        counts[kind] = counts.get(kind, 0) + 1
        differences.append({"table": item["table"], "old_register": item["row"].get("register"), "classification": kind, "detail": detail})
    return {
        "old_artifact": "sources/vendor/growatt-v1.24-tables.json",
        "new_document_id": new.get("document", {}).get("document_id"),
        "old_rows": len(old_rows(old)),
        "new_claims": len(new.get("claims", [])),
        "classification_counts": dict(sorted(counts.items())),
        "differences": differences,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--old", type=Path, required=True)
    parser.add_argument("--new", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--markdown", type=Path)
    args = parser.parse_args()
    result = compare(json.loads(args.old.read_text(encoding="utf-8")), json.loads(args.new.read_text(encoding="utf-8")))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if args.markdown:
        lines = ["# Historical vendor derivative comparison", "", f"* Old rows: `{result['old_rows']}`", f"* New claims: `{result['new_claims']}`", "", "## Classifications", ""]
        lines.extend(f"* `{key}`: {value}" for key, value in result["classification_counts"].items())
        args.markdown.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "classification_counts": result["classification_counts"]}, indent=2))


if __name__ == "__main__":
    main()
