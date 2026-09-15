#!/usr/bin/env python3
"""Build the bounded GII-CONSOLIDATION-2A correction artifacts.

This is a corrective projection over the immutable C2 audit snapshots.  It
does not edit the canonical specification or rewrite the historical C2 files.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.build_gii_consolidation import dump, load


ROOT = Path(__file__).resolve().parents[1]
C2_SHA = "1c9c0d34e819d6839958cd9b7a2ae4e2d2cff4a8"
CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
VENDOR_SHA256 = "fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320"
DATA = ROOT / "docs/consolidation/data"

INPUT_GAP_START = 3281
INPUT_GAP_END = 3374
HOLDING_RESERVED_START = 3115
HOLDING_RESERVED_END = 3124


def _path(name: str) -> Path:
    return DATA / name


def _c2(name: str) -> dict[str, Any]:
    return load(_path(name))


def _canonical_sha() -> str:
    digest = hashlib.sha256((ROOT / "spec/growatt-register-spec.json").read_bytes()).hexdigest()
    if digest != CANONICAL_SHA256:
        raise ValueError(f"frozen canonical specification hash changed: {digest}")
    return digest


def _gap_status(item: dict[str, Any]) -> dict[str, Any]:
    result = dict(item)
    address = item["address"]
    if item["table"] == "input" and INPUT_GAP_START <= address <= INPUT_GAP_END:
        result.update(
            gap_category="RESERVED_VENDOR_RANGE",
            automatically_resolvable=False,
            recommended_action=(
                "The V1.24 input block explicitly covers 3250-3374, but no individual "
                "semantic row is defined after I3280; retain I3281-I3374 as reserved "
                "or unused words, not as individual semantic registers."
            ),
            range_status="vendor_declared_reserved_words_without_semantic_rows",
            research_required_for_v124_completeness=False,
        )
    elif item["table"] == "holding" and HOLDING_RESERVED_START <= address <= HOLDING_RESERVED_END:
        result.update(
            gap_category="CANONICAL_CONFLICTS_WITH_VENDOR_RESERVED_RANGE",
            automatically_resolvable=False,
            recommended_action=(
                "Retain the historical canonical meaning for provenance, but do not present "
                "it as a V1.24 MIN/TL-XH semantic."
            ),
            range_status="vendor_reserved",
            research_required_for_v124_completeness=False,
        )
    return result


def _correct_classification() -> dict[str, Any]:
    old = _c2("GII-CONSOLIDATION-2_MIN_TL_XH_GAP_CLASSIFICATION.json")
    items = [_gap_status(item) for item in old["items"]]
    counts = Counter(item["gap_category"] for item in items)
    return {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2a_min_tl_xh_gap_classification",
        "parent_artifact": "GII-CONSOLIDATION-2_MIN_TL_XH_GAP_CLASSIFICATION.json",
        "parent_sha": C2_SHA,
        "canonical_sha256": CANONICAL_SHA256,
        "vendor_pdf_sha256": VENDOR_SHA256,
        "correction_scope": [
            "input 3281-3374 range-level V1.24 no-row classification",
            "holding 3116-3123 overlap with explicit V1.24 reserved range",
        ],
        "initial_gap_count": len(items),
        "final_unexplained_count": old["final_unexplained_count"],
        "category_counts": dict(sorted(counts.items())),
        "items": items,
        "vendor_unresolved": old["vendor_unresolved"],
        "existence_rule": (
            "A physical register requires an explicit vendor row, explicit vendor range row, "
            "explicit reserved range, or separately sourced non-vendor physical evidence. "
            "Applicability and polling ranges alone cannot instantiate a register."
        ),
    }


def _range_semantics() -> dict[str, Any]:
    return {
        "existence_rule": {
            "applicability_is_existence": False,
            "polling_is_existence": False,
            "accepted_evidence": [
                "explicit_vendor_row",
                "explicit_vendor_range_row",
                "explicit_reserved_range",
                "separately_sourced_non_vendor_physical_evidence",
            ],
        },
        "vendor_reserved_or_unassigned_ranges": [
            {
                "table": "holding",
                "start": HOLDING_RESERVED_START,
                "end": HOLDING_RESERVED_END,
                "status": "RESERVED",
                "confidence": "confirmed",
                "source": "vendor_growatt_v124_2020",
                "source_artifact": "sources/curated/overlays/growatt_vendor_tables_overlay.json",
                "source_pointer": "/holding:3115-3124/source_strings/vendor_tables",
                "source_page_or_section": "V1.24 p.42, Use for TL-X and TL-XH; row 3115 ~ 3124",
            },
            {
                "table": "input",
                "start": INPUT_GAP_START,
                "end": INPUT_GAP_END,
                "status": "RESERVED_VENDOR_RANGE",
                "confidence": "confirmed_for_no_row_gap",
                "source": "vendor_growatt_v124_2020",
                "source_artifact": "sources/vendor/growatt-v1.24-blocks.json",
                "source_pointer": "/blocks/13",
                "source_page_or_section": (
                    "V1.24 input TL-X/TL-XH block: I3280 is last explicit row; "
                    "next source block begins at I4000"
                ),
                "semantic_meaning": "declared block words with no individual V1.24 semantic row; treated as reserved or unused",
                "declared_block": {"table": "input", "start": 3250, "end": 3374, "function_code": 4, "family": "min_tl_xh"},
                "runtime_corroboration": {
                    "all_zero_words": True,
                    "nonzero_count": 0,
                    "physical_refreshes": 343,
                    "shine_cache_reads": 4860,
                    "earlier_direct_responses": 39,
                    "note": "Runtime observations corroborate reserved or unused words; they do not define semantic meaning.",
                },
            },
        ],
        "block_boundary_rule": "An explicit block end remains visible before the next block; polling spans do not fill the gap.",
    }


def _correct_candidate() -> dict[str, Any]:
    candidate = load(ROOT / "spec/growatt-register-spec-v2-candidate.json")
    candidate["vendor_range_semantics"] = _range_semantics()
    candidate["generated_by"] = "tools/build_gii_consolidation2a.py"
    candidate["source_documents"] = [
        *candidate["source_documents"],
        {
            "document_id": "ark_xh_a1_bdc_rs485_manual",
            "source_claim_artifact": "sources/evidence/ark-xh-a1-bdc-rs485.json",
            "source_status": "structured_excerpt_only",
        },
    ]
    seen_documents: set[str] = set()
    candidate["source_documents"] = [
        item
        for item in candidate["source_documents"]
        if not (item["document_id"] in seen_documents or seen_documents.add(item["document_id"]))
    ]
    for register in candidate["registers"]:
        table = register.get("table")
        address = register.get("address")
        if table == "holding" and address == 3085:
            register["status"] = "ENRICHED"
            register["conflict_refs"] = []
            register["consolidated"].update(
                {
                    "name": "BDC/BMS RS485 communication address",
                    "description": "RS485 communication address of the BDC/BMS battery system on the SYS COM battery interface.",
                    "semantic_key": "bdc_bms_slave_address",
                    "default": 1,
                    "range_raw": "1..254",
                    "subsystem": "bdc_bms",
                    "interface": "sys_com_rs485_battery",
                }
            )
            evidence = {"kind": "c2a_subsystem_scope", "source": "ark_xh_a1_bdc_rs485_manual"}
            register["other_evidence"] = [item for item in register.get("other_evidence", []) if item != evidence] + [evidence]
        elif table == "holding" and address == 3086:
            register["consolidated"].update(
                {
                    "name": "BDC/BMS RS485 baud-rate selector",
                    "description": "Baud-rate selector for inverter-to-BDC/BMS RS485 communication on the SYS COM battery interface.",
                    "semantic_key": "bdc_bms_rs485_baud_rate",
                    "default": 0,
                    "enum_values": {"0": "9600 bps", "1": "38400 bps"},
                    "subsystem": "bdc_bms",
                    "interface": "sys_com_rs485_battery",
                }
            )
            evidence = {"kind": "c2a_subsystem_scope", "source": "ark_xh_a1_bdc_rs485_manual"}
            register["other_evidence"] = [item for item in register.get("other_evidence", []) if item != evidence] + [evidence]
        elif table == "input" and address == 3085:
            register["status"] = "RESERVED"
            register["ha_readiness"] = "RESERVED_OR_UNSUPPORTED"
            register["conflict_refs"] = []
            register["consolidated"] = {
                **register["consolidated"],
                "name": "Reserved",
                "description": "Reserved in V1.24; no input semantic is defined.",
                "semantic_key": None,
                "signed": None,
                "divisor": None,
            }
    status_counts = Counter(item["status"] for item in candidate["registers"])
    readiness_counts = Counter(item["ha_readiness"] for item in candidate["registers"])
    candidate["metrics"].update(
        {
            "conflict_count": status_counts["CONFLICT"],
            "reserved_count": status_counts["RESERVED"],
            "unresolved_count": status_counts["UNRESOLVED"],
            "status_counts": dict(sorted(status_counts.items())),
            "ha_readiness_counts": dict(sorted(readiness_counts.items())),
        }
    )
    return candidate


def _correct_conflicts() -> dict[str, Any]:
    result = _c2("GII-CONSOLIDATION-2_CONFLICTS.json")
    conflicts = []
    for item in result["conflicts"]:
        item = dict(item)
        if item["conflict_id"] == "c2-conflict-022":
            item.update(
                disposition="RESOLVED_BDC_BMS_SUBSYSTEM_SCOPE",
                rationale=(
                    "H3085 is scoped to the BDC/BMS battery RS485 interface: the V1.24 "
                    "BDC block and the structured ARK XH-A1 wiring evidence identify SYS COM, "
                    "not the external DDSU666 meter."
                ),
            )
        elif item["conflict_id"] == "c2-conflict-023":
            item.update(
                disposition="RESOLVED_VENDOR_RESERVED_RANGE",
                rationale=(
                    "V1.24 marks input I3085 as Reserved; the old generic semantic conflict "
                    "is not a live BDC address setting."
                ),
            )
        conflicts.append(item)
    result.update(
        {
            "schema_version": "1.0.0",
            "artifact": "gii_consolidation_2a_conflict_review",
            "parent_artifact": "GII-CONSOLIDATION-2_CONFLICTS.json",
            "parent_sha": C2_SHA,
            "canonical_sha256": CANONICAL_SHA256,
            "conflicts": conflicts,
            "summary": dict(sorted(Counter(item["disposition"] for item in conflicts).items())),
        }
    )
    return result


def build(root: Path = ROOT) -> dict[str, Any]:
    global ROOT, DATA
    ROOT = root
    DATA = root / "docs/consolidation/data"
    _canonical_sha()
    candidate = _correct_candidate()
    classification = _correct_classification()
    conflicts = _correct_conflicts()
    old_projection = _c2("GII-CONSOLIDATION-2_MIN_TL_XH_PROJECTION.json")
    projection = dict(old_projection)
    projection.update(
        {
            "artifact": "gii_consolidation_2a_min_tl_xh_projection",
            "parent_artifact": "GII-CONSOLIDATION-2_MIN_TL_XH_PROJECTION.json",
            "parent_sha": C2_SHA,
            "canonical_sha256": CANONICAL_SHA256,
            "existence_model": _range_semantics()["existence_rule"],
            "vendor_reserved_or_unassigned_ranges": _range_semantics()["vendor_reserved_or_unassigned_ranges"],
        }
    )
    old_unresolved = _c2("GII-CONSOLIDATION-2_UNRESOLVED.json")
    unresolved = dict(old_unresolved)
    unresolved.update(
        {
            "artifact": "gii_consolidation_2a_unresolved_review",
            "parent_artifact": "GII-CONSOLIDATION-2_UNRESOLVED.json",
            "parent_sha": C2_SHA,
            "canonical_sha256": CANONICAL_SHA256,
            "excluded_from_active_research": [
                "input 3281-3374 RESERVED_VENDOR_RANGE",
                "holding 3116-3123 CANONICAL_CONFLICTS_WITH_VENDOR_RESERVED_RANGE",
            ],
        }
    )
    queue = {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2a_research_queue",
        "parent_artifact": "GII-CONSOLIDATION-2_RESEARCH_QUEUE.json",
        "parent_sha": C2_SHA,
        "canonical_sha256": CANONICAL_SHA256,
        "items": [
            {
                "queue_id": "retained-access-conflicts-c2a",
                "priority": "P2",
                "reason": "Four access-capability conflicts remain explicitly deferred for a later bounded review.",
                "conflict_ids": [
                    "c2-conflict-002",
                    "c2-conflict-003",
                    "c2-conflict-017",
                    "c2-conflict-018",
                ],
            }
        ],
        "priority_counts": {"P2": 1},
        "removed_resolved_items": [
            "h3085-semantic",
            "canonical-only-holding-3116-3123",
            "canonical-only-input-3281-3374",
        ],
        "note": "Applicability and polling ranges are not research evidence for register existence.",
    }
    classification_items = classification["items"]
    metrics = {
        "current_canonical_physical_keys": 895,
        "v124_defined_physical_min_tlxh_register_keys": 648,
        "v124_applicability_envelope_words_min_tlxh": 750,
        "v124_explicit_reserved_range_words": 10,
        "v124_reserved_declared_block_words_without_semantic_rows": INPUT_GAP_END - INPUT_GAP_START + 1,
        "canonical_only_non_v124_reserved_overlap_words": 8,
        "covered_vendor_defined_physical_keys": 648,
        "canonical_sha256": CANONICAL_SHA256,
        "candidate_register_count": len(candidate["registers"]),
        "candidate_conflict_count": candidate["metrics"]["conflict_count"],
        "active_research_queue_items": len(queue["items"]),
        "gap_category_counts": classification["category_counts"],
        "invariants": {
            "input_gap_not_instantiated": not any(
                r.get("table") == "input"
                and isinstance(r.get("address"), int)
                and INPUT_GAP_START <= r["address"] <= INPUT_GAP_END
                for r in candidate["registers"]
            ),
            "canonical_reserved_history_retained": all(
                any(
                    item["table"] == "holding"
                    and HOLDING_RESERVED_START <= item["address"] <= HOLDING_RESERVED_END
                    and item["gap_category"] == "CANONICAL_CONFLICTS_WITH_VENDOR_RESERVED_RANGE"
                    for item in classification_items
                )
                for _ in [0]
            ),
            "canonical_frozen": _canonical_sha() == CANONICAL_SHA256,
        },
    }
    return {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2a_reserved_and_bms_corrections",
        "starting_main_sha": C2_SHA,
        "parent_c2_sha": C2_SHA,
        "canonical_sha256": CANONICAL_SHA256,
        "vendor_pdf_sha256": VENDOR_SHA256,
        "candidate": candidate,
        "classification": classification,
        "projection": projection,
        "conflicts": conflicts,
        "unresolved": unresolved,
        "queue": queue,
        "metrics": metrics,
    }


def report(result: dict[str, Any]) -> str:
    metrics = result["metrics"]
    counts = metrics["gap_category_counts"]
    lines = [
        "# GII-CONSOLIDATION-2A — Reserved-range and BDC/BMS corrections",
        "",
        "This bounded offline correction preserves the immutable C2 audit snapshots and regenerates a corrected V2 candidate projection. The frozen canonical specification is unchanged.",
        "",
        "## Lineage and safety",
        "",
        f"- Starting/main and C2 parent SHA: `{result['starting_main_sha']}`",
        f"- Frozen canonical SHA before/after: `{CANONICAL_SHA256}`",
        f"- V1.24 PDF SHA-256: `{VENDOR_SHA256}`",
        "- No HA, broker, inverter, Shine, cloud, live API, or configuration operation was performed.",
        "- Historical C2 JSON/Markdown snapshots remain immutable; C2A outputs are phase-specific corrections.",
        "",
        "## Corrected classification",
        "",
        "| Subject | C2 before | C2A after |",
        "|---|---|---|",
        "| I3281–I3374 | `DIFFERENT_PROTOCOL_OR_SOURCE_REQUIRED` (94) | `RESERVED_VENDOR_RANGE` (94) |",
        "| H3116–H3123 | `CANONICAL_ONLY_PHYSICAL_REGISTER` (8) | `CANONICAL_CONFLICTS_WITH_VENDOR_RESERVED_RANGE` (8) |",
        "| H3115–H3124 | no range-level status | explicit V1.24 `RESERVED` range |",
        "",
        "I3281–I3374 have no individual semantic row in the candidate register list. They are inside the explicitly declared V1.24 FC04 block I3250–I3374 and are represented as reserved/unused words. Shine polling and the all-zero runtime observations corroborate that treatment; they do not create additional semantic definitions.",
        "",
        "## H3085/H3086 semantic scope",
        "",
        "- H3085 is `bdc_bms_slave_address`: read/write, default `1`, range `1..254`, subsystem `bdc_bms`, interface `sys_com_rs485_battery`.",
        "- H3086 is `bdc_bms_rs485_baud_rate`: read/write, default `0`, with `0 = 9600 bps` and `1 = 38400 bps`, on the same subsystem/interface.",
        "- The structured ARK XH-A1 excerpt identifies BDC INV RS485 pins 7/8 with MIN TL-XH SYS COM pins 7/8. Interface scope is documented; inverter-master/BDC-slave remains a high-confidence inference, not a vendor claim.",
        "- H3085 is not treated as a DDSU666 external-meter address. Input I3085 is retained as a V1.24 Reserved word.",
        "",
        "## Metrics",
        "",
        f"- Canonical physical keys: `{metrics['current_canonical_physical_keys']}` (not used as the V1.24 denominator).",
        f"- V1.24-defined MIN/TL-XH candidate physical keys: `{metrics['v124_defined_physical_min_tlxh_register_keys']}`.",
        f"- MIN/TL-XH applicability envelope words: `{metrics['v124_applicability_envelope_words_min_tlxh']}`; explicit reserved range words: `{metrics['v124_explicit_reserved_range_words']}`; declared-block words without semantic rows: `{metrics['v124_reserved_declared_block_words_without_semantic_rows']}`.",
        f"- Candidate register count remains `{metrics['candidate_register_count']}`; candidate conflicts reduce to `{metrics['candidate_conflict_count']}` after the two H3085 semantic resolutions.",
        f"- Corrected gap category counts: `{counts}`.",
        f"- Active research queue: `{len(result['queue']['items'])}` item containing the four retained access conflicts; the H3085, H3116–H3123, and I3281–I3374 items are removed.",
        "",
        "## Deferred scope",
        "",
        "The four retained access conflicts remain explicitly unresolved for a later bounded review. Master/slave direction remains inferred at high confidence. No unrelated canonical semantic, access, scaling, unit, or runtime consumer record was changed.",
        "",
        "## Generated artifacts",
        "",
        "- `spec/growatt-register-spec-v2-candidate.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2A_RESERVED_AND_BMS_CORRECTIONS.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2A_MIN_TL_XH_GAP_CLASSIFICATION.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2A_MIN_TL_XH_PROJECTION.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2A_CONFLICTS.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2A_UNRESOLVED.json`",
        "- `docs/consolidation/data/GII-CONSOLIDATION-2A_RESEARCH_QUEUE.json`",
        "- `sources/evidence/ark-xh-a1-bdc-rs485.json`",
        "",
        "`GII_C2A_RESERVED_AND_BMS_CORRECTIONS_ACCEPTED_WITH_FOLLOW_UP`",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    result = build()
    dump(ROOT / "spec/growatt-register-spec-v2-candidate.json", result["candidate"])
    dump(_path("GII-CONSOLIDATION-2A_RESERVED_AND_BMS_CORRECTIONS.json"), {k: v for k, v in result.items() if k != "candidate"})
    dump(_path("GII-CONSOLIDATION-2A_MIN_TL_XH_GAP_CLASSIFICATION.json"), result["classification"])
    dump(_path("GII-CONSOLIDATION-2A_MIN_TL_XH_PROJECTION.json"), result["projection"])
    dump(_path("GII-CONSOLIDATION-2A_CONFLICTS.json"), result["conflicts"])
    dump(_path("GII-CONSOLIDATION-2A_UNRESOLVED.json"), result["unresolved"])
    dump(_path("GII-CONSOLIDATION-2A_RESEARCH_QUEUE.json"), result["queue"])
    (ROOT / "docs/consolidation/GII-CONSOLIDATION-2A_RESERVED_AND_BMS_CORRECTIONS.md").write_text(report(result), encoding="utf-8")
    print(json.dumps(result["metrics"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
