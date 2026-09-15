#!/usr/bin/env python3
"""Build the block-oriented GII-CONSOLIDATION-1 candidate.

The input vendor claim artifact is the machine-readable result of the
layout-preserving V1.24 PDF extraction.  The PDF is still required here: its
hash and headings are checked independently so a flattened row export cannot
silently become the structural authority.

This tool creates review artifacts only.  It never edits the canonical
``spec/growatt-register-spec.json``.
"""

from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import subprocess
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CLAIMS_PATH = ROOT / "sources/claims/vendor/vendor_growatt_v124_2020.json"
CANONICAL_PATH = ROOT / "spec/growatt-register-spec.json"
MANIFEST_PATH = ROOT / "sources/manifest.json"
EXPECTED_PDF_SHA256 = "fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320"
EXPECTED_CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"

TABLE_BY_HEADING = {
    "4.1 holding reg": "holding",
    "4.2 input reg": "input",
}
HEADING_RE = re.compile(
    r"(?:first|second|third|fourth|fifth|sixth|six|seventh|eighth|ninth|tenth)\s+group|"
    r"\b(?:BDC|BMS|UPS)\s+(?:information|infomation)|"
    r"\bUS\s+Machine\s+type\s+Time\s+Set\b|"
    r"\bUse\s+for\s+TL-X\s+and\s+TL-XH\b",
    re.IGNORECASE,
)
ORDINAL_ONLY_RE = re.compile(
    r"^(?:first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth)\s+group$",
    re.IGNORECASE,
)
RESERVED_RE = re.compile(r"\breserv(?:e|ed|es|ing|ed)\b|\breversed\b", re.IGNORECASE)


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def dump(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sha256sum(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def collapse(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_") or "unknown"


def pdf_structure(pdf_path: Path) -> dict[str, Any]:
    """Read page headings from the original PDF with embedded layout text."""
    digest = sha256sum(pdf_path)
    if digest.lower() != EXPECTED_PDF_SHA256:
        raise ValueError(f"V1.24 PDF SHA-256 mismatch: expected {EXPECTED_PDF_SHA256}, got {digest}")
    result = subprocess.run(
        ["pdftotext", "-layout", "-enc", "UTF-8", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    current_table: str | None = None
    headings: list[dict[str, Any]] = []
    for page_number, page in enumerate(result.stdout.split("\f"), start=1):
        for line in page.splitlines():
            text = line.strip()
            normalized = collapse(text).lower()
            if normalized in TABLE_BY_HEADING:
                current_table = TABLE_BY_HEADING[normalized]
                continue
            if current_table and HEADING_RE.search(text) and len(collapse(text)) <= 100:
                headings.append(
                    {
                        "table": current_table,
                        "page": page_number,
                        "raw": text,
                        "normalized": collapse(text),
                        "section_id": slug(text),
                    }
                )
    return {
        "pdf_sha256": digest,
        "pages": len(result.stdout.split("\f")) - 1,
        "text_extractor": "pdftotext -layout -enc UTF-8",
        "headings": headings,
    }


def raw_bounds(expression: str) -> tuple[int | None, int | None]:
    numbers = [int(value) for value in re.findall(r"\d+", expression)]
    if not numbers:
        return None, None
    if re.search(r"\d+\s*[~-]\s*\d+", expression):
        return numbers[0], numbers[1]
    return numbers[0], None


def access_kind(raw: str | None) -> str | None:
    """Normalize only an exact access token; never search arbitrary row text."""
    if raw is None:
        return None
    token = re.sub(r"\s+", "", raw.strip().upper())
    if token in {"R", "READ"}:
        return "read"
    if token in {"W", "WRITE"}:
        return "write"
    if token in {"R/W", "W/R", "RW", "WR", "READ/WRITE", "WRITE/READ"}:
        return "read_write"
    return None


def access_capabilities(raw: str | None) -> dict[str, bool | None]:
    """Interpret the V1.24 write-column marker without making W write-only."""
    token = access_kind(raw)
    if token == "write":
        return {"readable": None, "writable": True}
    if token == "read":
        return {"readable": True, "writable": False}
    if token == "read_write":
        return {"readable": True, "writable": True}
    return {"readable": None, "writable": None}


def overlaps(start: int | None, end: int | None, other_start: int, other_end: int) -> bool:
    if start is None:
        return False
    return not (end or start) < other_start and not start > other_end


def role_for_heading(heading: str) -> tuple[str | None, str]:
    normalized = collapse(heading).lower()
    if ORDINAL_ONLY_RE.fullmatch(normalized):
        return None, "unresolved_ordinal_label"
    if "six group for storage power" in normalized:
        return "storage_power_settings", "vendor_supported"
    if "ninth group for storage power" in normalized:
        return "storage_power_telemetry", "vendor_supported"
    if "ninth group reserved for storage power" in normalized:
        return "storage_power_telemetry_reserved", "vendor_supported"
    if "ups information" in normalized:
        return "ups_information", "vendor_supported"
    if "bms information" in normalized or "bms infomation" in normalized:
        return "bms_information", "vendor_supported"
    if "bdc information" in normalized:
        return "bdc_information", "vendor_supported"
    if "us machine type time set" in normalized:
        return "time_set", "vendor_supported"
    if "use for tl-x" in normalized:
        return "tl_x_tl_xh_registers", "vendor_supported"
    return None, "unresolved"


def source_blocks(claims_doc: dict[str, Any], pdf: dict[str, Any]) -> list[dict[str, Any]]:
    # Manual review claims are parallel evidence for an extracted row, not a
    # second source-native occurrence.  Keep them linked below without adding
    # them to block membership or register counts.
    claims = [
        claim
        for claim in claims_doc["claims"]
        if claim.get("source_kind") == "vendor_pdf_extraction"
        and not claim.get("exclude_from_duplicate", False)
    ]
    grouped: dict[tuple[str, str, str], list[dict[str, Any]]] = defaultdict(list)
    for claim in claims:
        grouped[
            (
                claim["register_table"],
                claim["section_id"],
                claim["section_title"],
            )
        ].append(claim)

    headings_by_slug: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for heading in pdf["headings"]:
        headings_by_slug[(heading["table"], heading["section_id"])].append(heading)

    blocks: list[dict[str, Any]] = []
    for index, ((table, section_id, section_title), rows) in enumerate(
        sorted(grouped.items(), key=lambda item: (item[0][0], min(x["page"] for x in item[1]), item[0][1])),
        start=1,
    ):
        starts: list[int] = []
        ends: list[int] = []
        raw_starts: list[int] = []
        pages = [row["page"] for row in rows]
        page_ends = [row["page_end"] for row in rows]
        for row in rows:
            if row.get("parsed_address") is not None:
                starts.append(row["parsed_address"])
                ends.append(row.get("parsed_address_end") or row["parsed_address"])
            raw_start, raw_end = raw_bounds(row["raw_address_expression"])
            if raw_start is not None:
                raw_starts.append(raw_start)
                if raw_end is not None:
                    ends.append(raw_end)
        first_address, _ = raw_bounds(rows[0]["raw_address_expression"])
        address_start = first_address if first_address is not None else (starts[0] if starts else None)
        address_end = max(ends) if ends else None
        raw_heading = (
            headings_by_slug.get((table, slug(section_title)), [{}])[0].get("raw")
            or section_title
        )
        role, role_status = role_for_heading(raw_heading)
        block_id = f"v124-{table}-p{min(pages):03d}-{slug(section_id)}-block-{index:02d}"
        manual_reviews = [
            claim["claim_id"]
            for claim in claims_doc["claims"]
            if claim.get("exclude_from_duplicate", False)
            and claim["register_table"] == table
            and any(
                claim.get("parsed_address") is not None
                and row.get("parsed_address") == claim["parsed_address"]
                for row in rows
            )
        ]
        blocks.append(
            {
                "source_block_id": block_id,
                "source": "vendor_growatt_v124_2020",
                "table": table,
                "function_code": 3 if table == "holding" else 4,
                "page_start": min(pages),
                "page_end": max(page_ends),
                "address_start": address_start,
                "address_end": address_end,
                "address_bounds_status": (
                    "partial_due_to_algebraic_or_unparsed_rows"
                    if any(row.get("parsed_address") is None for row in rows)
                    else "complete_for_extracted_rows"
                ),
                "vendor_heading_raw": raw_heading,
                "vendor_group_label_raw": raw_heading if "group" in raw_heading.lower() else None,
                "normalized_role": role,
                "role_status": role_status,
                "rows": [row["claim_id"] for row in sorted(rows, key=lambda x: (x["page"], x["source_row_id"]))],
                "source_row_ids": [row["source_row_id"] for row in sorted(rows, key=lambda x: (x["page"], x["source_row_id"]))],
                "reviewed_evidence_claims": sorted(manual_reviews),
            }
        )
    return blocks


def applicability_paths(
    blocks: list[dict[str, Any]], declarations: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    paths: list[dict[str, Any]] = []
    for block in blocks:
        for declaration in declarations:
            for declared_range in declaration.get("ranges", []):
                if declared_range["table"] != block["table"]:
                    continue
                if not overlaps(
                    block["address_start"],
                    block["address_end"],
                    declared_range["start"],
                    declared_range["end"],
                ):
                    continue
                paths.append(
                    {
                        "consolidated_block_id": block["source_block_id"].replace("v124-", "cb-", 1),
                        "source_block_id": block["source_block_id"],
                        "declaration_id": declaration["declaration_id"],
                        "family_id": declaration["family_id"],
                        "source_scope": declaration["source_scope"],
                        "family_label": declaration["family_label"],
                        "qualifier": declared_range.get("qualifier"),
                        "function_code": declared_range["function_code"],
                        "table": declared_range["table"],
                        "declared_start": declared_range["start"],
                        "declared_end": declared_range["end"],
                    }
                )
    return sorted(
        paths,
        key=lambda item: (
            item["consolidated_block_id"],
            item["source_scope"],
            item["declared_start"],
            item["qualifier"] or "",
        ),
    )


def compact_canonical(record: dict[str, Any]) -> dict[str, Any]:
    normalized = record.get("normalized") or {}
    semantic = record.get("semantic_identity") or {}
    return {
        "physical_id": record.get("physical_id"),
        "family": record.get("family"),
        "name": normalized.get("name"),
        "description": normalized.get("description"),
        "raw_type": normalized.get("raw_type"),
        "signed": normalized.get("signed"),
        "divisor": normalized.get("divisor"),
        "multiplier": normalized.get("multiplier"),
        "scale": normalized.get("scale"),
        "unit": normalized.get("unit"),
        "access": access_kind(normalized.get("access")) or normalized.get("access"),
        "quantity": semantic.get("quantity"),
        "resolution_status": (record.get("resolution") or {}).get("status"),
        "resolution_confidence": (record.get("resolution") or {}).get("confidence"),
        "write_policy": record.get("write_policy"),
        "source_provenance": sorted(record.get("source_provenance") or []),
    }


def canonical_index(canonical: dict[str, Any]) -> dict[tuple[str, int], list[dict[str, Any]]]:
    index: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    for record in canonical["registers"]:
        if isinstance(record.get("address"), int) and record.get("table") in {"holding", "input"}:
            index[(record["table"], record["address"])].append(record)
    for records in index.values():
        records.sort(key=lambda record: (record.get("family") != "min_tl_xh", record.get("physical_id", "")))
    return index


def canonical_conflicts(
    vendor: dict[str, Any], matches: list[dict[str, Any]], block_id: str
) -> list[dict[str, Any]]:
    conflicts: list[dict[str, Any]] = []
    raw_access = vendor.get("raw_access_text")
    normalized_vendor_access = access_kind(raw_access)
    canonical_capabilities = [
        access_capabilities((match.get("normalized") or {}).get("access"))
        for match in matches
        if access_kind((match.get("normalized") or {}).get("access"))
    ]
    vendor_capabilities = access_capabilities(raw_access)
    access_mismatch = any(
        vendor_capabilities[key] is not None
        and all(capability[key] is not None and capability[key] != vendor_capabilities[key] for capability in canonical_capabilities)
        for key in ("readable", "writable")
    )
    if normalized_vendor_access and canonical_capabilities and access_mismatch:
        conflicts.append(
            {
                "block": block_id,
                "register": vendor.get("parsed_address"),
                "property": "access",
                "source_a": {"source": "vendor_v124", "value": raw_access},
                "source_b": {
                    "source": "current_canonical",
                    "value": sorted(
                        {
                            access_kind((match.get("normalized") or {}).get("access"))
                            for match in matches
                        }
                    ),
                },
                "vendor_capabilities": vendor_capabilities,
                "canonical_capabilities": canonical_capabilities,
                "evidence_quality": "source_access_dimensions_require_review",
                "recommended_status": "CONFLICT",
                "blocks_read_decoding": False,
                "blocks_safe_writing": True,
                "next_evidence": "inspect original row and family-specific access claims",
            }
        )
    canonical_quantities = {
        (match.get("semantic_identity") or {}).get("quantity")
        for match in matches
        if (match.get("semantic_identity") or {}).get("quantity")
    }
    if vendor.get("parsed_address") == 3085:
        conflicts.append(
            {
                "block": block_id,
                "register": 3085,
                "property": "semantic_identity",
                "source_a": {
                    "source": "vendor_v124",
                    "value": "ComAddress / Communication addr",
                },
                "source_b": {
                    "source": "current_canonical",
                    "value": sorted(canonical_quantities) or ["control.modbus_slave_address"],
                },
                "evidence_quality": "canonical_interpretation; external_meter_scope_unresolved",
                "recommended_status": "CONFLICT_REVIEW_CANDIDATE",
                "blocks_read_decoding": False,
                "blocks_safe_writing": True,
                "next_evidence": "independent device/protocol evidence; do not infer DDSU666 settings",
            }
        )
    return conflicts


def make_register(
    claim: dict[str, Any],
    block: dict[str, Any],
    matches: list[dict[str, Any]],
    paths: list[dict[str, Any]],
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    address = claim.get("parsed_address")
    physical_key = f"{block['source_block_id']}:{claim['source_row_id']}"
    compact_matches = [compact_canonical(record) for record in matches]
    chosen = compact_matches[0] if compact_matches else {}
    provenance_sources = sorted(
        {
            source
            for record in matches
            for source in record.get("source_provenance", [])
        }
    )
    conflicts = canonical_conflicts(claim, matches, block["source_block_id"])
    text = " ".join(
        value or ""
        for value in (
            claim.get("raw_variable"),
            claim.get("raw_description"),
            claim.get("raw_note"),
        )
    )
    if conflicts:
        status = "CONFLICT"
    elif address is None or not matches:
        status = "UNRESOLVED"
    elif RESERVED_RE.search(text):
        status = "RESERVED"
    elif any(path.get("qualifier") for path in paths):
        status = "QUALIFIED"
    elif chosen.get("name") or chosen.get("quantity"):
        status = "ENRICHED"
    else:
        status = "CONFIRMED"

    vendor_access = access_kind(claim.get("raw_access_text"))
    canonical_access = chosen.get("access")
    if address is None:
        ha_readiness = "NEEDS_METADATA"
    elif status == "RESERVED":
        ha_readiness = "RESERVED_OR_UNSUPPORTED"
    elif canonical_access in {"read", "read_write"} and (chosen.get("raw_type") or chosen.get("quantity")):
        ha_readiness = "READY_READ"
    elif canonical_access == "write" and (claim.get("raw_value_text") or chosen.get("name")):
        ha_readiness = "READY_WRITE_DOCUMENTED"
    else:
        ha_readiness = "NEEDS_METADATA"

    selected = {
        "name": chosen.get("name") or claim.get("raw_variable"),
        "description": chosen.get("description") or claim.get("raw_description"),
        "access": canonical_access or vendor_access,
        "unit": chosen.get("unit"),
        "signed": chosen.get("signed"),
        "scale": chosen.get("scale"),
        "divisor": chosen.get("divisor"),
        "multiplier": chosen.get("multiplier"),
        "semantic_key": chosen.get("quantity"),
        "range_raw": claim.get("raw_value_text"),
    }
    register = {
        "register_id": physical_key,
        "consolidated_block_id": block["source_block_id"].replace("v124-", "cb-", 1),
        "table": claim["register_table"],
        "function_code": 3 if claim["register_table"] == "holding" else 4,
        "address": address,
        "address_end": claim.get("parsed_address_end"),
        "vendor": {
            "claim_id": claim["claim_id"],
            "source_row_id": claim["source_row_id"],
            "page": claim["page"],
            "page_end": claim["page_end"],
            "variable_raw": claim.get("raw_variable"),
            "description_raw": claim.get("raw_description"),
            "access_raw": claim.get("raw_access_text"),
            "access_capabilities": access_capabilities(claim.get("raw_access_text")),
            "value_raw": claim.get("raw_value_text"),
            "unit_raw": claim.get("raw_unit_text"),
            "initial_raw": claim.get("raw_initial_text"),
            "note_raw": claim.get("raw_note"),
            "address_raw": claim.get("raw_address_expression"),
        },
        "current_canonical": compact_matches,
        "other_evidence": [
            {
                "source": source,
                "kind": "current_canonical_source_provenance",
            }
            for source in provenance_sources
        ],
        "consolidated": selected,
        "property_provenance": {
            "identity": ["vendor_v124"],
            "name": ["current_canonical"] if chosen.get("name") else ["vendor_v124"],
            "description": ["current_canonical"] if chosen.get("description") else ["vendor_v124"],
            "access": ["current_canonical"] if canonical_access else ["vendor_v124"],
            "decode_metadata": ["current_canonical"] if chosen.get("raw_type") else ["unresolved"],
        },
        "status": status,
        "ha_readiness": ha_readiness,
        "conflict_refs": [f"{block['source_block_id']}:{address}:{item['property']}" for item in conflicts],
        "applicability_paths": [
            {
                "source_scope": path["source_scope"],
                "qualifier": path["qualifier"],
                "declared_start": path["declared_start"],
                "declared_end": path["declared_end"],
            }
            for path in paths
            if address is None
            or overlaps(address, claim.get("parsed_address_end"), path["declared_start"], path["declared_end"])
        ],
    }
    unresolved: list[dict[str, Any]] = []
    if status == "UNRESOLVED":
        gap_type = "ambiguous_source_address" if address is None else "no_canonical_match"
        unresolved.append(
            {
                "register": address,
                "block": block["source_block_id"],
                "gap_type": gap_type,
                "source_claim": claim["claim_id"],
                "detail": claim.get("raw_address_expression"),
                "suggested_next_evidence": "original PDF visual review or family-specific source",
            }
        )
    return register, conflicts, unresolved


def compare_min_projection(
    registers: list[dict[str, Any]], canonical: dict[str, Any], paths: list[dict[str, Any]]
) -> dict[str, Any]:
    min_paths = [path for path in paths if path["source_scope"] == "min_tl_xh"]
    min_block_ids = {
        path["source_block_id"].replace("v124-", "cb-", 1) for path in min_paths
    }
    def register_keys(register: dict[str, Any]) -> set[tuple[str, int]]:
        address = register.get("address")
        if address is None:
            return set()
        end = register.get("address_end") or address
        return {(register["table"], item) for item in range(address, end + 1)}

    def is_in_min_path(register: dict[str, Any]) -> bool:
        return (
            register.get("consolidated_block_id") in min_block_ids
            and register.get("address") is not None
            and any(
            path["table"] == register["table"]
            and overlaps(
                register["address"],
                register.get("address_end"),
                path["declared_start"],
                path["declared_end"],
            )
            for path in min_paths
        )
        )

    candidate_keys = {
        key
        for register in registers
        if is_in_min_path(register)
        for key in register_keys(register)
    }
    canonical_keys = {
        (record["table"], record["address"])
        for record in canonical["registers"]
        if record.get("family") == "min_tl_xh" and isinstance(record.get("address"), int)
    }
    candidate_registers = {
        key: register
        for register in registers
        if is_in_min_path(register)
        for key in register_keys(register)
    }
    match = candidate_keys & canonical_keys
    category_counts = {
        "MATCH": len(match),
        "ENRICHED": sum(
            register["status"] == "ENRICHED" for register in candidate_registers.values()
        ),
        "CONFLICT": sum(
            register["status"] == "CONFLICT" for register in candidate_registers.values()
        ),
        "MISSING_IN_CANDIDATE": len(canonical_keys - candidate_keys),
        "NEW_FROM_VENDOR": len(candidate_keys - canonical_keys),
        "REPRESENTATION_ONLY": 0,
    }
    return {
        "candidate_physical_keys": len(candidate_keys),
        "canonical_min_tl_xh_keys": len(canonical_keys),
        "match": len(match),
        "new_from_vendor": len(candidate_keys - canonical_keys),
        "missing_in_candidate": len(canonical_keys - candidate_keys),
        "representation_only": 0,
        "category_counts": category_counts,
        "representation_only_definition": (
            "No separate representation-only category exists in this candidate; "
            "the value is zero until a reviewed non-physical representation is modeled."
        ),
    }


def build(pdf_path: Path) -> dict[str, Any]:
    claims_doc = load(CLAIMS_PATH)
    canonical = load(CANONICAL_PATH)
    actual_canonical_sha = sha256sum(CANONICAL_PATH)
    if actual_canonical_sha != EXPECTED_CANONICAL_SHA256:
        raise ValueError(
            f"canonical spec changed: expected {EXPECTED_CANONICAL_SHA256}, got {actual_canonical_sha}"
        )
    if claims_doc["document"]["document_sha256"].lower() != EXPECTED_PDF_SHA256:
        raise ValueError("V1.24 claims do not identify the expected original PDF")
    pdf = pdf_structure(pdf_path)
    blocks = source_blocks(claims_doc, pdf)
    declarations = claims_doc["document"].get("applicability_declarations", [])
    paths = applicability_paths(blocks, declarations)
    index = canonical_index(canonical)
    claims_by_id = {claim["claim_id"]: claim for claim in claims_doc["claims"]}
    all_registers: list[dict[str, Any]] = []
    conflicts: list[dict[str, Any]] = []
    unresolved: list[dict[str, Any]] = []
    consolidated_blocks: list[dict[str, Any]] = []
    for block in blocks:
        block_paths = [path for path in paths if path["source_block_id"] == block["source_block_id"]]
        block_registers: list[str] = []
        for claim_id in block["rows"]:
            claim = claims_by_id[claim_id]
            address = claim.get("parsed_address")
            matches = index.get((claim["register_table"], address), []) if address is not None else []
            register, register_conflicts, register_unresolved = make_register(
                claim, block, matches, block_paths
            )
            all_registers.append(register)
            block_registers.append(register["register_id"])
            conflicts.extend(register_conflicts)
            unresolved.extend(register_unresolved)
        consolidated_blocks.append(
            {
                "consolidated_block_id": block["source_block_id"].replace("v124-", "cb-", 1),
                "table": block["table"],
                "function_code": block["function_code"],
                "address_start": block["address_start"],
                "address_end": block["address_end"],
                "source_blocks": [block["source_block_id"]],
                "applicability_paths": block_paths,
                "applies_to": sorted({path["source_scope"] for path in block_paths}),
                "vendor_context": {
                    "headings_raw": [block["vendor_heading_raw"]],
                    "group_labels_raw": [block["vendor_group_label_raw"]]
                    if block["vendor_group_label_raw"]
                    else [],
                },
                "equivalence": "IDENTICAL",
                "register_ids": block_registers,
                "source_row_count": len(block["rows"]),
                "reviewed_evidence_claims": block["reviewed_evidence_claims"],
            }
        )

    all_registers.sort(key=lambda item: (item["table"], item["address"] is None, item["address"] or -1, item["register_id"]))
    conflict_unique: dict[str, dict[str, Any]] = {}
    for item in conflicts:
        key = f"{item['block']}:{item['register']}:{item['property']}:{item['recommended_status']}"
        conflict_unique[key] = item
    conflicts = [conflict_unique[key] for key in sorted(conflict_unique)]
    unresolved.sort(key=lambda item: (item["block"], item["register"] is None, item["register"] or -1, item["gap_type"]))

    status_counts = Counter(register["status"] for register in all_registers)
    readiness_counts = Counter(register["ha_readiness"] for register in all_registers)
    role_counts = Counter(
        "functional" if block["role_status"] == "vendor_supported" else "vague_or_ordinal"
        for block in blocks
    )
    metrics = {
        "source_native_blocks_discovered": len(blocks),
        "source_native_blocks_with_explicit_functional_heading": role_counts["functional"],
        "source_native_blocks_with_vague_or_ordinal_heading": role_counts["vague_or_ordinal"],
        "consolidated_blocks": len(consolidated_blocks),
        "identical_block_merges": 0,
        "semantic_equivalent_merges": 0,
        "family_variants": 0,
        "block_conflicts": 0,
        "total_consolidated_registers": len(all_registers),
        "status_counts": dict(sorted(status_counts.items())),
        "ha_readiness_counts": dict(sorted(readiness_counts.items())),
        "conflict_count": len(conflicts),
        "unresolved_count": len(unresolved),
        "reserved_count": status_counts["RESERVED"],
        "unsupported_count": 0,
    }
    candidate = {
        "schema_version": "2.0.0-candidate",
        "artifact": "growatt_consolidated_register_spec_candidate",
        "generated_by": "tools/build_gii_consolidation.py",
        "source_documents": [
            {
                "document_id": claims_doc["document"]["document_id"],
                "revision": claims_doc["document"]["declared_revision"],
                "sha256": claims_doc["document"]["document_sha256"],
                "source_claim_artifact": "sources/claims/vendor/vendor_growatt_v124_2020.json",
            }
        ],
        "canonical_comparison": {
            "path": "spec/growatt-register-spec.json",
            "sha256": actual_canonical_sha,
            "frozen": True,
        },
        "blocks": consolidated_blocks,
        "source_native_blocks": blocks,
        "applicability": declarations,
        "applicability_paths": paths,
        "overrides": [],
        "registers": all_registers,
        "metrics": metrics,
        "normalization_policy": {
            "raw_vendor_values_preserved": True,
            "access_normalization": "exact-token-only",
            "evidence_strength_unchanged_by_normalization": True,
        },
        "review_scope": "offline V1.24 source and repository evidence only; no live/cloud/HA/broker changes",
    }
    projection = {
        "schema_version": "1.0.0",
        "artifact": "generated_min_tl_xh_projection",
        "generated_by": "tools/build_gii_consolidation.py",
        "source_candidate": "spec/growatt-register-spec-v2-candidate.json",
        "family": "min_tl_xh",
        "applicability_paths": [path for path in paths if path["source_scope"] == "min_tl_xh"],
        "blocks": [
            {
                "consolidated_block_id": block["consolidated_block_id"],
                "covered_ranges": [
                    {
                        "table": path["table"],
                        "start": path["declared_start"],
                        "end": path["declared_end"],
                        "qualifier": path["qualifier"],
                    }
                    for path in paths
                    if path["source_block_id"] in block["source_blocks"]
                    and path["source_scope"] == "min_tl_xh"
                ],
                "register_ids": [
                    register["register_id"]
                    for register in all_registers
                    if register["consolidated_block_id"] == block["consolidated_block_id"]
                    and register["address"] is not None
                    and any(
                        path["source_block_id"] in block["source_blocks"]
                        and path["table"] == register["table"]
                        and path["source_scope"] == "min_tl_xh"
                        and overlaps(
                            register["address"],
                            register.get("address_end"),
                            path["declared_start"],
                            path["declared_end"],
                        )
                        for path in paths
                    )
                ],
            }
            for block in consolidated_blocks
            if any(path["source_block_id"] in block["source_blocks"] and path["source_scope"] == "min_tl_xh" for path in paths)
        ],
        "comparison_with_current_canonical": compare_min_projection(all_registers, canonical, paths),
    }
    return {
        "candidate": candidate,
        "projection": projection,
        "blocks": {
            "schema_version": "1.0.0",
            "artifact": "growatt_v124_source_native_block_inventory",
            "generated_by": "tools/build_gii_consolidation.py",
            "source_pdf": {
                "document_id": claims_doc["document"]["document_id"],
                "filename": claims_doc["document"]["filename"],
                "sha256": pdf["pdf_sha256"],
                "pages": pdf["pages"],
                "extraction": pdf["text_extractor"],
            },
            "blocks": blocks,
            "applicability_paths": paths,
            "metrics": metrics,
        },
        "matrix": {
            "schema_version": "1.0.0",
            "artifact": "gii_consolidation_register_matrix",
            "generated_by": "tools/build_gii_consolidation.py",
            "canonical_sha256": actual_canonical_sha,
            "registers": all_registers,
        },
        "conflicts": {
            "schema_version": "1.0.0",
            "artifact": "gii_consolidation_conflicts",
            "generated_by": "tools/build_gii_consolidation.py",
            "canonical_sha256": actual_canonical_sha,
            "conflicts": conflicts,
        },
        "unresolved": {
            "schema_version": "1.0.0",
            "artifact": "gii_consolidation_unresolved",
            "generated_by": "tools/build_gii_consolidation.py",
            "unresolved": unresolved,
        },
    }


def render_report(result: dict[str, Any]) -> str:
    blocks = result["blocks"]["blocks"]
    metrics = result["candidate"]["metrics"]
    comparison = result["projection"]["comparison_with_current_canonical"]
    status_counts = metrics["status_counts"]
    lines = [
        "# GII-CONSOLIDATION-1 — Vendor-native V1.24 register blocks",
        "",
        "## Goal",
        "",
        "This is an offline, block-oriented candidate for the future Growatt register specification. It keeps the V1.24 vendor structure primary, uses existing repository evidence for enrichment and challenge, and leaves the canonical specification frozen.",
        "",
        "## Starting repository state",
        "",
        "- Starting merged-main: `fe63d223d83dbadd4be6448802d42b5f9302c64f` (PIPELINE-11 merge).",
        f"- V1.24 PDF SHA-256: `{EXPECTED_PDF_SHA256}`; 85 pages; embedded `pdftotext -layout` extraction.",
        f"- Frozen canonical spec SHA-256: `{EXPECTED_CANONICAL_SHA256}`.",
        "- No live, cloud, Home Assistant, broker or inverter activity was performed.",
        "",
        "### Reproducible extraction command",
        "",
        "```text",
        "python3 tools/extract_vendor_pdf.py --pdf ../Homeassistant-Growatt-Local-Modbus/doc/Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf --expected-sha256 fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320 --document-id vendor_growatt_v124_2020 --profile sources/vendor/profiles/vendor_growatt_v124_2020.json --review sources/claims/vendor/reviews/vendor_growatt_v124_2020.json --output sources/claims/vendor/vendor_growatt_v124_2020.json",
        "python3 tools/build_gii_consolidation.py --pdf ../Homeassistant-Growatt-Local-Modbus/doc/Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf",
        "```",
        "",
        "The extraction environment used `pdftotext`/`pdfinfo` 25.03.0 and Python 3.14.5. The original PDF is not copied into this repository; only its filename, hash and derived claims are published.",
        "",
        "## Growatt V1.24 source-native block structure",
        "",
        "The source-native inventory is derived from the original PDF’s layout-preserving claim extraction. Manual visual-review claims are retained as evidence references and are not counted as a second occurrence.",
        "",
        "| Source-native block | FC/table | Range | Vendor heading(s) | Families/scopes | Rows | Role status |",
        "|---|---:|---:|---|---|---:|---|",
    ]
    for block in blocks:
        paths = [p for p in result["blocks"]["applicability_paths"] if p["source_block_id"] == block["source_block_id"]]
        families = ", ".join(sorted({p["source_scope"] for p in paths})) or "—"
        bounds = f"{block['address_start']}–{block['address_end']}"
        lines.append(
            f"| `{block['source_block_id']}` | FC{block['function_code']} / {block['table']} | {bounds} | {block['vendor_heading_raw']} | {families} | {len(block['rows'])} | `{block['role_status']}` |"
        )
    lines.extend(
        [
            "",
            "Functional headings: **%d**; vague/ordinal headings: **%d**. The latter remain `unresolved_ordinal_label` and are not promoted to vendor-authored semantics." % (
                metrics["source_native_blocks_with_explicit_functional_heading"],
                metrics["source_native_blocks_with_vague_or_ordinal_heading"],
            ),
            "",
            "## Consolidated block model",
            "",
            f"The candidate contains **{metrics['consolidated_blocks']}** consolidated blocks. Each currently maps one V1.24 source-native structural block; shared family use is represented through applicability paths rather than copied family register tables. No cross-source block merge was forced because the available source-native occurrences were not independently proven identical beyond their preserved structure.",
            "",
            "## Family/model applicability",
            "",
            "All seven V1.24 instruction-block declarations are retained, including MIN/TL-XH, TL3/MAX scopes, MOD TL3-XH and MIX/SPA/SPH storage scopes. The complete raw declaration text is in `spec/growatt-register-spec-v2-candidate.json`; block paths retain declaration ID, function/table, range and qualifiers.",
            "",
            "## Register consolidation results",
            "",
            f"The matrix contains **{metrics['total_consolidated_registers']}** vendor row definitions. Vendor raw fields and canonical comparison fields are kept separate; selected descriptions and decode metadata are enrichment, not new evidence.",
            "",
            "| Register status | Count |",
            "|---|---:|",
        ]
    )
    for key in ("CONFIRMED", "ENRICHED", "QUALIFIED", "CONFLICT", "UNRESOLVED", "RESERVED"):
        lines.append(f"| {key.title()} | {status_counts.get(key, 0)} |")
    lines.extend(
        [
            "",
            "### H107 access normalization",
            "",
            "H107 is represented with vendor raw access `W` and normalized access derived from the exact token only. The previous layout-leak form `r    W` is not accepted as a raw access value by the extractor. The regression is generic: access extraction never searches or copies arbitrary neighboring row text.",
            "",
            "## Description enrichment and decode metadata",
            "",
            "Existing canonical, runtime, external implementation and accepted evidence records are included as compact side-by-side comparison entries in the register matrix. A missing decode property remains visible as `NEEDS_METADATA`; normalization such as `1S` to `s` is not performed as evidence creation in this candidate.",
            "",
            "## Write metadata and HA-readiness",
            "",
            "Vendor access and write safety remain separate. A documented writable row is not marked live-write-verified. The current candidate reports:",
            "",
            f"- `READY_READ`: {metrics['ha_readiness_counts'].get('READY_READ', 0)}",
            f"- `READY_WRITE_DOCUMENTED`: {metrics['ha_readiness_counts'].get('READY_WRITE_DOCUMENTED', 0)}",
            f"- `READY_WRITE_VERIFIED`: {metrics['ha_readiness_counts'].get('READY_WRITE_VERIFIED', 0)}",
            f"- `NEEDS_METADATA`: {metrics['ha_readiness_counts'].get('NEEDS_METADATA', 0)}",
            f"- `RESERVED_OR_UNSUPPORTED`: {metrics['ha_readiness_counts'].get('RESERVED_OR_UNSUPPORTED', 0)}",
            "",
            "## MIN/TL-XH generated projection",
            "",
            "The projection is generated from consolidated blocks plus V1.24 applicability paths. It is not hand-maintained and retains qualifiers such as the TL-XH/TL-XH US distinctions.",
            "",
            f"- Candidate physical keys: **{comparison['candidate_physical_keys']}**",
            f"- Current canonical MIN/TL-XH keys: **{comparison['canonical_min_tl_xh_keys']}**",
            f"- Matching keys: **{comparison['match']}**",
            f"- New from vendor: **{comparison['new_from_vendor']}**",
            f"- Missing in candidate: **{comparison['missing_in_candidate']}**",
            "",
            "Comparison category summary:",
            "",
            *(f"- `{key}`: {value}" for key, value in comparison["category_counts"].items()),
            f"- `REPRESENTATION_ONLY` definition: {comparison['representation_only_definition']}",
            "",
            "## Conflicts",
            "",
            f"There are **{metrics['conflict_count']}** explicit comparison conflicts/review candidates. They are listed in `docs/consolidation/data/GII-CONSOLIDATION-1_CONFLICTS.json`; H3085 remains explicitly flagged as a semantic review candidate and is not silently treated as an external-meter setting.",
            "",
            "## Unresolved evidence gaps",
            "",
            f"There are **{metrics['unresolved_count']}** unresolved rows, including ambiguous/unparsed source addresses and rows without a current canonical match. They are listed in `docs/consolidation/data/GII-CONSOLIDATION-1_UNRESOLVED.json` rather than being invented or discarded.",
            "",
            "## Safety / canonical freeze",
            "",
            "`spec/growatt-register-spec.json` was not modified. The candidate is `spec/growatt-register-spec-v2-candidate.json`; no Home Assistant consumer changes are included. Generated artifacts are deterministic and can be regenerated with `tools/build_gii_consolidation.py` using the original local PDF.",
            "",
            "## Generated artifacts",
            "",
            "- `sources/vendor/growatt-v1.24-blocks.json`",
            "- `docs/consolidation/data/GII-CONSOLIDATION-1_BLOCK_INVENTORY.json`",
            "- `docs/consolidation/data/GII-CONSOLIDATION-1_REGISTER_MATRIX.json`",
            "- `docs/consolidation/data/GII-CONSOLIDATION-1_CONFLICTS.json`",
            "- `docs/consolidation/data/GII-CONSOLIDATION-1_UNRESOLVED.json`",
            "- `docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json`",
            "- `spec/growatt-register-spec-v2-candidate.json`",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, default=ROOT)
    args = parser.parse_args()
    result = build(args.pdf)
    output_root = args.output_root
    dump(output_root / "sources/vendor/growatt-v1.24-blocks.json", result["blocks"])
    dump(output_root / "docs/consolidation/data/GII-CONSOLIDATION-1_REGISTER_MATRIX.json", result["matrix"])
    dump(output_root / "docs/consolidation/data/GII-CONSOLIDATION-1_BLOCK_INVENTORY.json", result["blocks"])
    dump(output_root / "docs/consolidation/data/GII-CONSOLIDATION-1_CONFLICTS.json", result["conflicts"])
    dump(output_root / "docs/consolidation/data/GII-CONSOLIDATION-1_UNRESOLVED.json", result["unresolved"])
    dump(output_root / "spec/growatt-register-spec-v2-candidate.json", result["candidate"])
    dump(output_root / "docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json", result["projection"])
    (output_root / "docs/consolidation/GII-CONSOLIDATION-1_VENDOR_BLOCKS.md").write_text(
        render_report(result), encoding="utf-8"
    )


if __name__ == "__main__":
    main()
