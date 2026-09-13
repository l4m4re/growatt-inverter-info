#!/usr/bin/env python3
"""Compare independent vendor claim artifacts without resolving conflicts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def norm(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip().lower()


def signature(claim: dict[str, Any]) -> tuple[str, int | None]:
    return (claim["register_table"], claim.get("parsed_address"))


def compare(paths: list[Path]) -> dict[str, Any]:
    docs = [json.loads(path.read_text(encoding="utf-8")) for path in paths]
    indexed: dict[tuple[str, int | None], list[tuple[str, dict[str, Any]]]] = {}
    for payload in docs:
        doc_id = payload["document"]["document_id"]
        for claim in payload["claims"]:
            indexed.setdefault(signature(claim), []).append((doc_id, claim))
    rows: list[dict[str, Any]] = []
    for key, entries in sorted(indexed.items(), key=lambda item: (item[0][0], item[0][1] is None, item[0][1] or -1)):
        if len({doc_id for doc_id, _ in entries}) < 2:
            continue
        texts = {norm(" ".join(str(claim.get(field) or "") for field in ("raw_variable", "raw_description", "raw_value_text", "raw_unit_text", "raw_access_text"))) for _, claim in entries}
        if len(texts) == 1:
            classification = "identical_claim"
        elif all(norm(claim.get("raw_unit_text")) == norm(entries[0][1].get("raw_unit_text")) and norm(claim.get("raw_access_text")) == norm(entries[0][1].get("raw_access_text")) for _, claim in entries):
            classification = "wording_or_layout_difference"
        else:
            classification = "apparent_unresolved_difference"
        scopes = {doc_id: claim.get("family_scope", []) for doc_id, claim in entries}
        rows.append({"register_table": key[0], "parsed_address": key[1], "family_scopes": scopes, "classification": classification, "documents": [doc_id for doc_id, _ in entries], "claims": [claim["claim_id"] for _, claim in entries]})
    return {"documents": [payload["document"] for payload in docs], "overlap_count": len(rows), "comparisons": rows, "note": "Classification is descriptive only; no document is selected as canonical."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--claims", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = compare(args.claims)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps({"output": str(args.output), "overlap_count": result["overlap_count"]}, indent=2))


if __name__ == "__main__":
    main()
