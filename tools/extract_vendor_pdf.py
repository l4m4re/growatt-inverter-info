#!/usr/bin/env python3
"""Extract layout-preserving Growatt vendor PDF source claims.

This tool deliberately stops at source claims.  It does not assign canonical
semantic names, decode registers, or reconcile documents.  The vendor PDF is
read with Poppler's embedded-text/layout extractor; page continuations and
ambiguous addresses are retained as evidence instead of being guessed away.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


SCHEMA_VERSION = "1.0.0"
SOURCE_KIND = "vendor_pdf_extraction"
PAGE_RE = re.compile(r"^\s*(\d+)\s*/\s*(\d+)\s*$")
REVISION_RE = re.compile(r"\bV\d+(?:\.\d+)+\b", re.IGNORECASE)
DATE_RE = re.compile(r"\b\d{4}[-/.]\d{1,2}[-/.]\d{1,2}\b")
ROW_RE = re.compile(
    r"^(?P<indent>\s{0,14})(?P<address>(?:\d[^\s]*|[…\.]{2,})+)"
    r"(?:\s+(?P<body>.*)|\s*$)$"
)
SIMPLE_SINGLE_RE = re.compile(r"^\d+\.?$")
SIMPLE_RANGE_RE = re.compile(r"^(\d+)\s*[~\-]\s*(\d+)$")
ALGEBRAIC_RE = re.compile(r"[+*()]|\bN\b", re.IGNORECASE)
MALFORMED_RANGE_RE = re.compile(r"^\d+\s*-\s*\d+(?:\s+\d+)?$")

TABLE_PATTERNS = {
    "holding": re.compile(r"\b4\.1\s+Holding\b|\bHolding\s+Reg\b", re.IGNORECASE),
    "input": re.compile(r"\b4\.2\s+Input\b|\bInput\s+Reg\b", re.IGNORECASE),
}
TABLE_END_RE = re.compile(r"^\s*5\s+Set\s+address\b", re.IGNORECASE)
SECTION_RE = re.compile(
    r"(?:first|second|third|fourth|fifth|sixth|six|seventh|eighth|ninth|tenth)\s+group|"
    r"\b(?:BDC|BMS|UPS)\s+(?:information|infomation)|"
    r"\bUS\s+Machine\s+type\s+Time\s+Set\b|"
    r"\bUse\s+for\s+TL-X\b|"
    r"\bBDC\s+information\b",
    re.IGNORECASE,
)
FOOTER_RE = re.compile(
    r"Growatt\s+(?:New Energy|NEW ENERGY)|^\s*#?28\s+Guangming|"
    r"P\.C\.\s*\d+|www\.|info@|Tel:",
    re.IGNORECASE,
)


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def run_text_command(args: list[str]) -> str:
    result = subprocess.run(args, check=True, capture_output=True, text=True)
    return result.stdout


def pdfinfo(path: Path) -> dict[str, str]:
    result = run_text_command(["pdfinfo", str(path)])
    info: dict[str, str] = {}
    for line in result.splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            info[key.strip()] = value.strip()
    return info


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def page_text(path: Path) -> list[str]:
    output = run_text_command(["pdftotext", "-layout", "-enc", "UTF-8", str(path), "-"])
    return [page for page in output.split("\f") if page.strip()]


def document_id(revision: str | None, digest: str) -> str:
    prefix = (revision or "unknown").lower().replace(".", "_")
    return f"vendor_{prefix}_{digest[:8]}"


def metadata_from_pages(path: Path, pages: list[str], digest: str, info: dict[str, str]) -> dict[str, Any]:
    first_pages = "\n".join(pages[:3])
    title = next(
        (
            collapse(line)
            for line in first_pages.splitlines()
            if "Growatt" in line and "Protocol" in line and len(collapse(line)) > 15
        ),
        path.stem,
    )
    revision_match = REVISION_RE.search(first_pages)
    revision = revision_match.group(0).upper() if revision_match else None
    dates = []
    for value in DATE_RE.findall(first_pages):
        normalized = value.replace("/", "-").replace(".", "-")
        if normalized not in dates:
            dates.append(normalized)

    scope_lines: list[str] = []
    for line in first_pages.splitlines():
        normalized = collapse(line)
        if "register range" in normalized.lower() or "type)" in normalized.lower():
            if normalized and normalized not in scope_lines:
                scope_lines.append(normalized)
    if not scope_lines:
        scope_lines = ["unknown_vendor_scope"]

    language = "English"
    if re.search(r"[\u3400-\u9fff]", first_pages):
        language = "English with Chinese text/footer"

    return {
        "document_id": document_id(revision, digest),
        "filename": path.name,
        "title": title,
        "declared_revision": revision,
        "declared_dates": dates,
        "pdf_metadata_date": info.get("CreationDate"),
        "document_sha256": digest,
        "page_count": int(info.get("Pages", len(pages))),
        "language": language,
        "apparent_family_scope": scope_lines,
        "source_origin": "local user-retained/vendor workspace PDF; original URL not assumed",
    }


def is_footer(line: str) -> bool:
    return bool(FOOTER_RE.search(line))


def table_from_line(line: str) -> str | None:
    for table, pattern in TABLE_PATTERNS.items():
        if pattern.search(line):
            return table
    return None


def is_heading(line: str) -> bool:
    normalized = collapse(line)
    return bool(normalized and len(normalized) <= 100 and SECTION_RE.search(normalized))


def row_match(line: str, indent_max: int = 14) -> re.Match[str] | None:
    if len(line) - len(line.lstrip()) > indent_max:
        return None
    return ROW_RE.match(line)


def parse_address(raw: str) -> tuple[int | None, int | None, str, str | None]:
    value = collapse(raw).rstrip(".")
    if SIMPLE_SINGLE_RE.fullmatch(value):
        return int(value.rstrip(".")), None, "parsed", None
    if match := SIMPLE_RANGE_RE.fullmatch(value):
        start, end = int(match.group(1)), int(match.group(2))
        if end >= start:
            return start, end, "parsed", None
        return None, None, "ambiguous", "suspicious_layout_address"
    if ALGEBRAIC_RE.search(value):
        return None, None, "ambiguous", "algebraic_address_expression"
    if MALFORMED_RANGE_RE.fullmatch(value) or re.search(r"\d+\s+-\s+\d+", value):
        return None, None, "ambiguous", "suspicious_layout_address"
    return None, None, "unparsed", "unparsed_address"


def header_positions(line: str) -> dict[str, int]:
    positions: dict[str, int] = {}
    for key, patterns in {
        "variable": ("Variable Name", "Variable"),
        "description": ("Description",),
        "access": ("Write",),
        "value": ("Value",),
        "unit": ("Unit",),
        "initial": ("Initial",),
        "note": ("Note",),
    }.items():
        for pattern in patterns:
            position = line.lower().find(pattern.lower())
            if position >= 0:
                positions[key] = position
                break
    return positions


def sliced_columns(line: str, positions: dict[str, int]) -> dict[str, str | None]:
    if not positions:
        return {key: None for key in ("variable", "description", "access", "value", "unit", "initial", "note")}
    ordered = sorted((position, key) for key, position in positions.items())
    columns: dict[str, str | None] = {}
    for index, (start, key) in enumerate(ordered):
        end = ordered[index + 1][0] if index + 1 < len(ordered) else None
        columns[key] = line[start:end].strip() or None
    for key in ("variable", "description", "access", "value", "unit", "initial", "note"):
        columns.setdefault(key, None)
    # Layout extraction can leave the tail of a wrapped description in front
    # of the access token (for example ``r    W`` at H107).  Repair only an
    # isolated Modbus access token; arbitrary input-column text remains raw.
    access = columns.get("access")
    if access:
        # A clipped leading character is a recurring layout artifact in the
        # vendor table: ``/W`` and ``/R`` are the visible tail of R/W and W/R.
        clipped = re.match(r"^\s*/([WR])(?:\s|$)", access.upper())
        if clipped:
            columns["access"] = f"{'R' if clipped.group(1) == 'W' else 'W'}/{clipped.group(1)}"
            return columns
        matches = re.findall(r"(?<![A-Za-z/])(?:R/W|W/R|R|W)(?![A-Za-z/])", access.upper())
        if matches:
            columns["access"] = matches[-1]
    return columns


def claim_from_row(row: dict[str, Any], metadata: dict[str, Any]) -> dict[str, Any]:
    fragments = row["fragments"]
    first = fragments[0]
    raw_address = row["raw_address_expression"]
    address, address_end, address_status, address_diagnostic = parse_address(raw_address)
    columns = row["columns"]
    raw_text = "\n".join(line for fragment in fragments for line in fragment["lines"])
    status = "continued" if len(fragments) > 1 else "complete"
    diagnostics: list[str] = []
    if address_diagnostic:
        diagnostics.append(address_diagnostic)
    if len(fragments) > 1:
        diagnostics.append("page_spanning_continuation")
    if not columns.get("variable"):
        diagnostics.append("blank_variable")
    if columns.get("variable") and re.search(r"[A-Za-z]{3,}\s+[A-Za-z]{1,}", columns["variable"]):
        diagnostics.append("internal_split_word_candidate")
    if re.search(r"\b\d+\s*[:：]", raw_text):
        diagnostics.append("enum_or_bitfield_candidate")

    claim_id = f"{metadata['document_id']}:{row['table']}:p{row['page']:03d}:row-{row['source_row_id']}"
    continuation_refs = [
        f"{claim_id}:fragment-p{fragment['page']:03d}"
        for fragment in fragments[1:]
    ]
    source_fragments = [
        {
            "fragment_id": f"{claim_id}:fragment-p{fragment['page']:03d}",
            "page": fragment["page"],
            "lines": fragment["lines"],
            "text": "\n".join(fragment["lines"]),
        }
        for fragment in fragments
    ]
    claim: dict[str, Any] = {
        "claim_id": claim_id,
        "document_id": metadata["document_id"],
        "document_revision": metadata["declared_revision"],
        "document_sha256": metadata["document_sha256"],
        "source_kind": SOURCE_KIND,
        "page": row["page"],
        "page_end": fragments[-1]["page"],
        "section_id": row["section_id"],
        "section_title": row["section_title"],
        "family_scope": metadata["apparent_family_scope"],
        "register_table": row["table"],
        "source_row_id": row["source_row_id"],
        "raw_address_expression": raw_address,
        "parsed_address": address,
        "parsed_address_end": address_end,
        "raw_variable": columns.get("variable"),
        "reconstructed_variable": None,
        "raw_description": columns.get("description"),
        "raw_value_text": columns.get("value"),
        "raw_unit_text": columns.get("unit"),
        "raw_access_text": columns.get("access"),
        "raw_initial_text": columns.get("initial"),
        "raw_note": columns.get("note"),
        "raw_row_text": raw_text,
        "reconstructed_row_text": collapse(raw_text),
        "extraction_method": "pdftotext-layout-embedded-text",
        "extraction_confidence": "medium" if diagnostics else "high",
        "source_status": status if address_status == "parsed" else f"{status}_{address_status}",
        "continuation_refs": continuation_refs,
        "source_fragments": source_fragments,
        "diagnostics": sorted(set(diagnostics)),
    }
    return claim


def load_review_claims(path: Path, metadata: dict[str, Any]) -> list[dict[str, Any]]:
    """Load explicitly reviewed, public-safe source transcriptions.

    Review files contain table transcription decisions that cannot be recovered
    reliably from a flattened PDF text stream.  They never contain canonical
    semantics; the original page fragments and review note remain mandatory.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    review_paths = [path]
    review_paths.extend(path.parent / include for include in payload.get("include_files", []))
    claims: list[dict[str, Any]] = []
    for review_path in review_paths:
        review = json.loads(review_path.read_text(encoding="utf-8"))
        if review["document_id"] != metadata["document_id"]:
            raise ValueError(f"review document mismatch in {review_path}")
        if review["document_sha256"].lower() != metadata["document_sha256"].lower():
            raise ValueError(f"review hash mismatch in {review_path}")
        for item in review.get("claims", []):
            exclude_from_duplicate = review.get("exclude_from_duplicate", False)
            claim_id = item["claim_id"]
            fragments = [
                {
                    "fragment_id": f"{claim_id}:fragment-p{fragment['page']:03d}",
                    "page": fragment["page"],
                    "lines": fragment["lines"],
                    "text": "\n".join(fragment["lines"]),
                }
                for fragment in item["source_fragments"]
            ]
            continuation_refs = [
                f"{claim_id}:fragment-p{fragment['page']:03d}"
                for fragment in fragments[1:]
            ]
            claim = {
                "claim_id": claim_id,
                "document_id": metadata["document_id"],
                "document_revision": metadata["declared_revision"],
                "document_sha256": metadata["document_sha256"],
                "source_kind": "manual_original_document_verified",
                "page": item["page"],
                "page_end": fragments[-1]["page"],
                "section_id": item["section_id"],
                "section_title": item["section_title"],
                "family_scope": item.get("family_scope", metadata["apparent_family_scope"]),
                "register_table": item["register_table"],
                "source_row_id": item["source_row_id"],
                "raw_address_expression": item["raw_address_expression"],
                "parsed_address": item.get("parsed_address"),
                "parsed_address_end": item.get("parsed_address_end"),
                "raw_variable": item.get("raw_variable"),
                "reconstructed_variable": item.get("reconstructed_variable"),
                "raw_description": item.get("raw_description"),
                "raw_value_text": item.get("raw_value_text"),
                "raw_unit_text": item.get("raw_unit_text"),
                "raw_access_text": item.get("raw_access_text"),
                "raw_initial_text": item.get("raw_initial_text"),
                "raw_note": item.get("raw_note"),
                "raw_row_text": "\n".join(
                    line for fragment in fragments for line in fragment["lines"]
                ),
                "reconstructed_row_text": item["reconstructed_row_text"],
                "extraction_method": "native_text+agent_visual_review",
                "extraction_confidence": item.get("extraction_confidence", "high"),
                "source_status": "manually_reviewed",
                "continuation_refs": continuation_refs,
                "source_fragments": fragments,
                "diagnostics": sorted(set(item.get("diagnostics", []))),
                "review_note": item["review_note"],
                "exclude_from_duplicate": exclude_from_duplicate,
            }
            claims.append(claim)
    return claims


def extract_document(
    path: Path,
    expected_sha256: str | None = None,
    document_id_override: str | None = None,
    review_path: Path | None = None,
    family_scope_override: list[str] | None = None,
    profile_path: Path | None = None,
) -> dict[str, Any]:
    digest = sha256sum(path)
    if expected_sha256 and digest.lower() != expected_sha256.lower():
        raise ValueError(
            f"SHA-256 mismatch for {path}: expected {expected_sha256}, got {digest}"
        )
    info = pdfinfo(path)
    pages = page_text(path)
    metadata = metadata_from_pages(path, pages, digest, info)
    profile: dict[str, Any] = {}
    if profile_path:
        profile = json.loads(profile_path.read_text(encoding="utf-8"))
        if profile.get("document_id") != (document_id_override or metadata["document_id"]):
            raise ValueError(f"profile document mismatch in {profile_path}")
        if review_path is None and profile.get("manual_review_file"):
            review_path = Path(profile["manual_review_file"])
    if document_id_override:
        metadata["document_id"] = document_id_override
    if family_scope_override:
        metadata["apparent_family_scope"] = family_scope_override
    elif profile.get("apparent_family_scope"):
        metadata["apparent_family_scope"] = profile["apparent_family_scope"]
    if profile.get("applicability_declarations"):
        metadata["applicability_declarations"] = profile["applicability_declarations"]
    claims: list[dict[str, Any]] = []
    diagnostics: list[dict[str, Any]] = []
    current_table: str | None = None
    current_section_id = "unknown_section"
    current_section_title = "Unknown section"
    current_header: dict[str, int] = {}
    current_row: dict[str, Any] | None = None

    def flush() -> None:
        nonlocal current_row
        if current_row is None:
            return
        claim = claim_from_row(current_row, metadata)
        claims.append(claim)
        for kind in claim["diagnostics"]:
            diagnostics.append({"kind": kind, "claim_id": claim["claim_id"]})
        current_row = None

    for page_index, page in enumerate(pages, start=1):
        page_number_match = next((PAGE_RE.match(line) for line in page.splitlines() if PAGE_RE.match(line)), None)
        page_number = int(page_number_match.group(1)) if page_number_match else page_index
        lines = page.splitlines()
        for line in lines:
            if PAGE_RE.match(line) or is_footer(line):
                continue
            if TABLE_END_RE.match(line):
                flush()
                current_table = None
                continue
            detected_table = table_from_line(line)
            if detected_table:
                if detected_table != current_table:
                    flush()
                current_table = detected_table
                current_section_id = f"{detected_table}_register_table"
                current_section_title = f"{detected_table.title()} register table"
                continue
            if "Variable" in line and ("Description" in line or "Value" in line):
                current_header = header_positions(line)
                continue
            if current_table is None:
                continue
            if is_heading(line):
                flush()
                current_section_id = re.sub(r"[^a-z0-9]+", "_", collapse(line).lower()).strip("_") or "unknown_section"
                current_section_title = collapse(line)
                continue
            match = row_match(line, int(profile.get("row_indent_max", 14)))
            if match:
                address_candidate = collapse(match.group("address"))
                if (
                    current_row is not None
                    and re.fullmatch(r"\d+\s*-\s*\d+", current_row["raw_address_expression"])
                    and int(current_row["raw_address_expression"].split("-")[0])
                    and address_candidate.isdigit()
                    and int(current_row["raw_address_expression"].split("-")[0])
                    > int(address_candidate)
                ):
                    current_row["raw_address_expression"] += f" {address_candidate}"
                    current_row["fragments"][-1]["lines"].append(line)
                    continue
                flush()
                raw_address = address_candidate
                body = match.group("body") or ""
                current_row = {
                    "page": page_number,
                    "table": current_table,
                    "section_id": current_section_id,
                    "section_title": current_section_title,
                    "source_row_id": f"{page_number:03d}-{len(claims) + 1:04d}",
                    "raw_address_expression": raw_address,
                    "columns": sliced_columns(line, current_header),
                    "fragments": [{"page": page_number, "lines": [line]}],
                }
                continue
            if current_row is not None:
                if current_row["fragments"][-1]["page"] != page_number:
                    current_row["fragments"].append({"page": page_number, "lines": []})
                current_row["fragments"][-1]["lines"].append(line)
        if current_row is not None and current_row["fragments"][-1]["page"] != page_number:
            current_row["fragments"].append({"page": page_number, "lines": []})
    flush()

    reviewed_claims = load_review_claims(review_path, metadata) if review_path else []
    claims.extend(reviewed_claims)

    claims.sort(key=lambda claim: (claim["register_table"], claim["page"], claim["source_row_id"], claim["claim_id"]))
    diagnostic_counts: dict[str, int] = {}
    for item in diagnostics:
        diagnostic_counts[item["kind"]] = diagnostic_counts.get(item["kind"], 0) + 1
    numeric_groups: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for claim in claims:
        if claim["parsed_address"] is not None and not claim.get("exclude_from_duplicate", False):
            numeric_groups.setdefault((claim["register_table"], claim["parsed_address"]), []).append(claim)
    duplicate_groups = [
        group for group in numeric_groups.values()
        if len({(item["section_id"], item["page"]) for item in group}) > 1
    ]
    for group in duplicate_groups:
        for claim in group:
            if "duplicate_address_across_sections" not in claim["diagnostics"]:
                claim["diagnostics"].append("duplicate_address_across_sections")
                claim["diagnostics"].sort()
        diagnostic_counts["duplicate_address_across_sections"] = diagnostic_counts.get(
            "duplicate_address_across_sections", 0
        ) + len(group)

    return {
        "schema_version": SCHEMA_VERSION,
        "artifact": "growatt_vendor_source_claims",
        "document": metadata,
        "extraction": {
            "tool": "tools/extract_vendor_pdf.py",
            "tool_version": "1.0.0",
            "text_extractor": "pdftotext 25.x -layout -enc UTF-8",
            "strategy": "embedded text first; layout-preserving page parser; no OCR",
            "pages_processed": len(pages),
            "claims": len(claims),
            "continuation_fragments": sum(max(0, len(claim["source_fragments"]) - 1) for claim in claims),
            "ambiguous_address_claims": sum(claim["parsed_address"] is None for claim in claims),
            "source_rows_without_parsed_address": sum(claim["parsed_address"] is None for claim in claims),
            "manually_verified_claims": 0,
            "manually_verified_claims": len(reviewed_claims),
            "ocr_assisted_regions": 0,
            "diagnostic_counts": dict(sorted(diagnostic_counts.items())),
            "deterministic": True,
            "profile": profile.get("profile_id") if profile else None,
            "applicability_declarations": len(metadata.get("applicability_declarations", [])),
        },
        "claims": claims,
        "notes": [
            "Claims retain raw layout text; no canonical semantic interpretation is applied.",
            "A claim with multiple source_fragments is a logical row spanning pages.",
            "Ambiguous addresses are intentionally not coerced to a numeric register.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, action="append", required=True, help="Local vendor PDF; may be repeated")
    parser.add_argument("--expected-sha256", action="append", help="Expected SHA-256, in the same order as --pdf")
    parser.add_argument("--document-id", action="append", help="Stable document ID, in the same order as --pdf")
    parser.add_argument("--review", action="append", help="Reviewed-claim JSON, in the same order as --pdf")
    parser.add_argument("--family-scope", action="append", help="Document-level scope wording; may be repeated")
    parser.add_argument("--profile", action="append", help="Layout profile JSON, in the same order as --pdf")
    parser.add_argument("--output", type=Path, help="Output JSON for one PDF")
    parser.add_argument("--output-dir", type=Path, help="Output directory for multiple PDFs")
    args = parser.parse_args()
    if args.output and len(args.pdf) != 1:
        parser.error("--output is valid only with one --pdf")
    if args.expected_sha256 and len(args.expected_sha256) not in (1, len(args.pdf)):
        parser.error("provide one --expected-sha256 or one per --pdf")
    if args.document_id and len(args.document_id) not in (1, len(args.pdf)):
        parser.error("provide one --document-id or one per --pdf")
    if args.review and len(args.review) not in (1, len(args.pdf)):
        parser.error("provide one --review or one per --pdf")
    if args.profile and len(args.profile) not in (1, len(args.pdf)):
        parser.error("provide one --profile or one per --pdf")
    expected = args.expected_sha256 or []
    for index, pdf in enumerate(args.pdf):
        expected_hash = expected[0] if len(expected) == 1 else (expected[index] if expected else None)
        document_ids = args.document_id or []
        stable_id = document_ids[0] if len(document_ids) == 1 else (document_ids[index] if document_ids else None)
        reviews = args.review or []
        review = Path(reviews[0] if len(reviews) == 1 else reviews[index]) if reviews else None
        profiles = args.profile or []
        profile = Path(profiles[0] if len(profiles) == 1 else profiles[index]) if profiles else None
        payload = extract_document(pdf, expected_hash, stable_id, review, args.family_scope, profile)
        if args.output:
            output = args.output
        elif args.output_dir:
            output = args.output_dir / f"{payload['document']['document_id']}.json"
        else:
            output = Path(f"{payload['document']['document_id']}.json")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        print(json.dumps({"output": str(output), "document": payload["document"], "extraction": payload["extraction"]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
