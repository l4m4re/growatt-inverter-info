#!/usr/bin/env python3
"""Build the review-resolved current GII-CONSOLIDATION-2B state.

This is an additive current-state correction over the accepted C2A output.
Historical C2/C2A artifacts and the frozen canonical specification are not
rewritten.
"""

from __future__ import annotations

from collections import Counter
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from tools.build_gii_consolidation import access_capabilities, dump, load


ROOT = Path(__file__).resolve().parents[1]
CANONICAL_SHA256 = "e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405"
C2A_CANDIDATE = ROOT / "spec/growatt-register-spec-v2-candidate.json"
C2A_CONFLICTS = ROOT / "docs/consolidation/data/GII-CONSOLIDATION-2A_CONFLICTS.json"
DATA = ROOT / "docs/consolidation/data"
REPORT_PATH = ROOT / "docs/consolidation/GII-CONSOLIDATION-2B_ACCESS_AND_RESERVED_FINALIZATION.md"
BASELINE_COMMIT = "5024fa4bc12000474b376eec48e90277a8b04cd4"

REVIEWED_ACCESS = {
    122: {
        "reviewed_access_raw": "R/W",
        "resolution": "reviewed_vendor_correction",
        "basis": "manual_source_review",
    },
    123: {
        "reviewed_access_raw": "R/W",
        "resolution": "reviewed_vendor_correction",
        "basis": "manual_source_review",
    },
    1002: {
        "reviewed_access_raw": "R/W",
        "resolution": "reviewed_vendor_access",
        "basis": "manual_source_review",
    },
    1003: {
        "reviewed_access_raw": "W",
        "resolution": "reviewed_write_marker_plus_read_evidence",
        "basis": "manual_source_review",
    },
}

CONFLICT_RESOLUTIONS = {
    122: "RESOLVED_VENDOR_RW_REVIEW_CORRECTION",
    123: "RESOLVED_VENDOR_RW_REVIEW_CORRECTION",
    1002: "RESOLVED_VENDOR_ACCESS_REVIEW",
    1003: "RESOLVED_VENDOR_WRITE_CAPABILITY_PLUS_READ_EVIDENCE",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def baseline_candidate(root: Path) -> tuple[dict[str, Any], str]:
    """Read the accepted C2A candidate without depending on the output file."""
    payload = subprocess.check_output(
        [
            "git",
            "-C",
            str(root),
            "show",
            f"{BASELINE_COMMIT}:spec/growatt-register-spec-v2-candidate.json",
        ]
    )
    return json.loads(payload), hashlib.sha256(payload).hexdigest()


def current_capabilities(access: str | None) -> dict[str, bool | None]:
    """Represent current access without treating ``write`` as write-only."""
    return access_capabilities(access)


def register_for(candidate: dict[str, Any], address: int) -> dict[str, Any]:
    return next(
        item
        for item in candidate["registers"]
        if item.get("table") == "holding" and item.get("address") == address
    )


def apply_access_review(candidate: dict[str, Any]) -> None:
    for register in candidate["registers"]:
        address = register.get("address")
        if register.get("table") == "holding" and address in {*range(1003, 1013), 124}:
            access = register.get("consolidated", {}).get("access")
            register["consolidated_access_capabilities"] = current_capabilities(access)

    for address, review in REVIEWED_ACCESS.items():
        register = register_for(candidate, address)
        old_refs = list(register.get("conflict_refs", []))
        register["reviewed_correction"] = {
            **review,
            "status": "resolved",
            "historical_extraction_superseded": address in {122, 123},
            "historical_conflict_refs": old_refs,
            "consolidated_access": "read_write",
        }
        register["consolidated"]["access"] = "read_write"
        register["consolidated_access_capabilities"] = {
            "readable": True,
            "writable": True,
        }
        register["conflict_refs"] = []
        register["status"] = "ENRICHED"

    candidate["access_normalization"] = {
        "context": "V1.24 holding-register write-capability column",
        "markers": {
            "R/W": {"readable": True, "writable": True},
            "R": {"readable": True, "writable": False},
            "W": {"readable": None, "writable": True},
        },
        "rule": "W is a writable marker, not proof of write-only access; readability requires independent evidence.",
    }


def apply_reserved_review(candidate: dict[str, Any]) -> None:
    for item in candidate["vendor_range_semantics"]["vendor_reserved_or_unassigned_ranges"]:
        if item["table"] == "holding" and item["start"] == 3115 and item["end"] == 3124:
            item["status"] = "RESERVED"
            item["reservation_basis"] = ["vendor_explicit_reserved"]
        elif item["table"] == "input" and item["start"] == 3281 and item["end"] == 3374:
            item["historical_status"] = item.get("status")
            item["status"] = "RESERVED"
            item["range_status"] = "RESERVED"
            item["reservation_basis"] = [
                "vendor_specified_range",
                "no_individual_semantic_rows",
                "stock_shine_reads_range",
                "runtime_all_zero",
            ]


def update_metrics(candidate: dict[str, Any]) -> None:
    status_counts = Counter(item["status"] for item in candidate["registers"])
    readiness_counts = Counter(item["ha_readiness"] for item in candidate["registers"])
    candidate["metrics"].update(
        {
            "conflict_count": status_counts["CONFLICT"],
            "reserved_count": status_counts["RESERVED"],
            "status_counts": dict(sorted(status_counts.items())),
            "ha_readiness_counts": dict(sorted(readiness_counts.items())),
            "active_research_queue_items": 0,
        }
    )


def current_conflicts(parent_sha: str) -> dict[str, Any]:
    parent = load(C2A_CONFLICTS)
    conflicts: list[dict[str, Any]] = []
    for original in parent["conflicts"]:
        item = dict(original)
        register = item["original_conflict"].get("register")
        if register in CONFLICT_RESOLUTIONS and item["disposition"] == "RETAINED_ACCESS_CONFLICT_REVIEW":
            item["disposition"] = CONFLICT_RESOLUTIONS[register]
            item["resolution_basis"] = "review_resolved_current_consolidation"
            item["rationale"] = {
                122: "Manual review confirms the V1.24 cell is R/W; the historical extracted R is superseded only in current state.",
                123: "Manual review confirms the V1.24 cell is R/W; the historical extracted R is superseded only in current state.",
                1002: "Manual review confirms the V1.24 row is R/W and enriches the canonical read capability.",
                1003: "V1.24 W is a writable marker; existing read evidence makes the current capability read/write.",
            }[register]
        conflicts.append(item)
    return {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2b_current_conflict_review",
        "parent_artifact": "GII-CONSOLIDATION-2A_CONFLICTS.json",
        "parent_sha": parent_sha,
        "historical_conflicts_preserved": True,
        "total": len(conflicts),
        "conflicts": conflicts,
        "summary": dict(sorted(Counter(item["disposition"] for item in conflicts).items())),
        "retained_access_conflicts": sum(
            item["disposition"] == "RETAINED_ACCESS_CONFLICT_REVIEW" for item in conflicts
        ),
    }


def build(root: Path = ROOT) -> dict[str, Any]:
    candidate, parent_sha = baseline_candidate(root)
    conflict_parent_sha = sha256(C2A_CONFLICTS)
    canonical_sha = sha256(root / "spec/growatt-register-spec.json")
    if canonical_sha != CANONICAL_SHA256:
        raise ValueError(f"frozen canonical specification hash changed: {canonical_sha}")

    apply_access_review(candidate)
    apply_reserved_review(candidate)
    update_metrics(candidate)
    candidate["generated_by"] = "tools/build_gii_consolidation2b.py"
    candidate["parent_artifact"] = "spec/growatt-register-spec-v2-candidate.json (C2A state)"
    candidate["parent_sha256"] = parent_sha
    candidate["review_scope"] = [
        "H122/H123 reviewed vendor R/W correction",
        "H1002 reviewed vendor access enrichment",
        "H1003 reviewed W marker plus read evidence",
        "I3281-I3374 reviewed RESERVED classification",
    ]

    conflicts = current_conflicts(conflict_parent_sha)
    queue = {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2b_current_research_queue",
        "parent_artifact": "GII-CONSOLIDATION-2A_RESEARCH_QUEUE.json",
        "parent_sha": sha256(DATA / "GII-CONSOLIDATION-2A_RESEARCH_QUEUE.json"),
        "active_items": [],
        "resolved_items": [
            "H122 access conflict",
            "H123 access conflict",
            "H1002 access conflict",
            "H1003 access conflict",
        ],
        "active_count": 0,
        "note": "The four access conflicts are resolved by review in the current consolidated state; historical queue artifacts remain unchanged.",
    }
    result = {
        "schema_version": "1.0.0",
        "artifact": "gii_consolidation_2b_access_and_reserved_finalization",
        "parent_candidate_sha256": parent_sha,
        "canonical_sha256": canonical_sha,
        "historical_artifacts_unchanged": [
            "GII-CONSOLIDATION-2_CONFLICTS.json",
            "GII-CONSOLIDATION-2A_CONFLICTS.json",
            "GII-CONSOLIDATION-2A_RESEARCH_QUEUE.json",
            "PIPELINE-6..11 artifacts",
        ],
        "candidate": candidate,
        "conflicts": conflicts,
        "research_queue": queue,
        "resolved_access": {
            "before_retained_access_conflicts": 4,
            "after_retained_access_conflicts": conflicts["retained_access_conflicts"],
            "registers": [122, 123, 1002, 1003],
        },
        "reserved_ranges": [
            {
                "table": "holding",
                "start": 3115,
                "end": 3124,
                "status": "RESERVED",
                "reservation_basis": ["vendor_explicit_reserved"],
            },
            {
                "table": "input",
                "start": 3281,
                "end": 3374,
                "status": "RESERVED",
                "reservation_basis": [
                    "vendor_specified_range",
                    "no_individual_semantic_rows",
                    "stock_shine_reads_range",
                    "runtime_all_zero",
                ],
            },
        ],
        "metrics": {
            "candidate_register_count": len(candidate["registers"]),
            "candidate_conflict_count": candidate["metrics"]["conflict_count"],
            "active_research_queue_count": queue["active_count"],
        },
    }
    return result


def report(result: dict[str, Any]) -> str:
    return f"""# GII-CONSOLIDATION-2B — Review-resolved access and reserved-state finalization

This additive current-state correction records reviewed conclusions without
rewriting historical C2/C2A artifacts or the frozen canonical specification.

## Current resolutions

| Register | Current result | Resolution |
|---|---|---|
| H122 | `read_write` | reviewed vendor correction; current reviewed raw access `R/W` |
| H123 | `read_write` | reviewed vendor correction; current reviewed raw access `R/W` |
| H1002 | `read_write` | reviewed vendor access enriches canonical read evidence |
| H1003 | `read_write` | `W` means writable marker; existing read evidence is retained |

The historical extracted H122/H123 value `R` remains in the historical source
claim. The current candidate carries the reviewed correction explicitly and
does not silently rewrite that provenance.

## Reserved ranges

| Range | Current status | Basis |
|---|---|---|
| H3115–H3124 | `RESERVED` | explicit vendor reserved rows |
| I3281–I3374 | `RESERVED` | vendor range, no semantic rows, Shine reads range, repeated all-zero observations |

I3250–I3280 remains outside the reserved tail and is not changed. The current
candidate does not instantiate individual semantic registers for I3281–I3374.

## Counts and lineage

- Retained access conflicts: `4` before → `{result['resolved_access']['after_retained_access_conflicts']}` after.
- Active current research queue: `{result['metrics']['active_research_queue_count']}`.
- Candidate register count: `{result['metrics']['candidate_register_count']}`.
- Parent C2A candidate SHA-256: `{result['parent_candidate_sha256']}`.
- Frozen canonical SHA-256: `{result['canonical_sha256']}` (unchanged).
- Historical C2/C2A and PIPELINE-6..11 artifacts remain unchanged.
- No HA, broker, inverter, Shine, cloud, or live operation was performed.

## Access normalization

In the V1.24 holding-register write-capability column, `R/W` means readable
and writable, `R` means readable and not writable, and `W` means writable with
readability unspecified. `W` is never treated as proof of write-only access.

## Generated current artifacts

- `spec/growatt-register-spec-v2-candidate.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2B_ACCESS_AND_RESERVED_FINALIZATION.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2B_CONFLICTS.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2B_RESEARCH_QUEUE.json`

`GII_C2B_REVIEW_RESOLVED_FINALIZATION_ACCEPTED`
"""


def main() -> None:
    result = build()
    dump(C2A_CANDIDATE, result["candidate"])
    dump(DATA / "GII-CONSOLIDATION-2B_ACCESS_AND_RESERVED_FINALIZATION.json", {key: value for key, value in result.items() if key != "candidate"})
    dump(DATA / "GII-CONSOLIDATION-2B_CONFLICTS.json", result["conflicts"])
    dump(DATA / "GII-CONSOLIDATION-2B_RESEARCH_QUEUE.json", result["research_queue"])
    REPORT_PATH.write_text(report(result) + "\n", encoding="utf-8")
    print(json.dumps(result["metrics"], indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
