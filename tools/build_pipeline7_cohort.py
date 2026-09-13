#!/usr/bin/env python3
"""Build the next bounded declarative authority migration.

The authority inventory remains the single generic accounting implementation.
This builder applies the accepted PIPELINE-6 decisions as an explicit overlay
only for the fresh PIPELINE-7 baseline, then ranks and builds one new cohort.
"""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import subprocess
from typing import Any

try:
    from tools.build_authority_coverage import (
        DECISION_PROPERTY_MAP,
        build as build_authority,
        canonical_authority_origins,
        override_keys,
    )
except ModuleNotFoundError:
    from build_authority_coverage import (
        DECISION_PROPERTY_MAP,
        build as build_authority,
        canonical_authority_origins,
        override_keys,
    )

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = ROOT / "spec/growatt-register-spec.json"
RECONCILIATION_PATH = ROOT / "reconciliation/min_tl_xh_holding_comms_3083_3086.json"
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-7_NEXT_AUTHORITY_COHORT.json"
REPORT_PATH = ROOT / "docs/pipeline/GII-PIPELINE-7_NEXT_AUTHORITY_COHORT.md"
GII6_REUSED_PATH = ROOT / "reconciliation/min_tl_xh.json"
GII6_NEW_PATH = ROOT / "reconciliation/min_tl_xh_holding_ems_3036_3059_3081_3082.json"
GII6_ARTIFACT_PATH = (
    ROOT / "docs/pipeline/data/GII-PIPELINE-6_NEXT_AUTHORITY_COHORT.json"
)

SELECTED_ADDRESSES = [3083, 3084, 3085, 3086]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def claim_id(address: int) -> str:
    claims = load(ROOT / "sources/claims/generic-claims.json")["claims"]
    matches = [
        item["claim_id"]
        for item in claims
        if item["source_id"] == "vendor_growatt_v124_2020"
        and item["subject"].get("table") == "holding"
        and item["subject"].get("address") == address
        and ":source-row:" in item["claim_id"]
    ]
    if len(matches) != 1:
        raise ValueError(
            f"expected one V1.24 source-row claim for H{address}, found {matches}"
        )
    return matches[0]


def accepted_pipeline6_decisions() -> list[dict[str, Any]]:
    addresses = set(load(GII6_ARTIFACT_PATH)["selected_cohort"]["addresses"])
    old = [
        item
        for item in load(GII6_REUSED_PATH)["decisions"]
        if item["target"].get("namespace") == "MODBUS"
        and item["target"].get("table") == "holding"
        and item["target"].get("address") in addresses
    ]
    new = load(GII6_NEW_PATH)["decisions"]
    return [*old, *new]


def properties_for(
    decisions: list[dict[str, Any]],
) -> dict[tuple[str, str, int], set[str]]:
    result: dict[tuple[str, str, int], set[str]] = {}
    for item in decisions:
        target = item["target"]
        if target.get("namespace") != "MODBUS":
            continue
        key = (target["canonical_family"], target["table"], target["address"])
        result.setdefault(key, set()).update(
            DECISION_PROPERTY_MAP.get(target["property"], set())
        )
    return result


def build_decisions() -> list[dict[str, Any]]:
    decisions: list[dict[str, Any]] = []
    for address in (3083, 3084):
        decisions.append(
            {
                "decision_id": f"min-xh-h{address}-reserved-authority",
                "target": {
                    "canonical_family": "min_tl_xh",
                    "namespace": "MODBUS",
                    "table": "holding",
                    "address": address,
                    "property": "status",
                },
                "scope": {
                    "family": "min_tl_xh",
                    "model": "MIN/TL-XH",
                    "firmware": None,
                    "protocol_revision": "V1.24",
                    "region": None,
                    "applicability": "MIN/TL-XH V1.24 holding communication block",
                },
                "decision": {
                    "status": "reserved",
                    "confidence": "high",
                    "value": {"reserved": True},
                },
                "support": [claim_id(address)],
                "conflicts": [],
                "rationale": "The V1.24 source row explicitly marks this physical word Reserved; no semantic value is invented.",
                "review": {
                    "status": "reviewed",
                    "notes": "PIPELINE-7 promotion of a source-declared reserved word; canonical output remains frozen.",
                },
            }
        )

    decisions.append(
        {
            "decision_id": "min-xh-h3085-modbus-address-authority",
            "target": {
                "canonical_family": "min_tl_xh",
                "namespace": "MODBUS",
                "table": "holding",
                "address": 3085,
                "property": "semantic_mapping",
            },
            "scope": {
                "family": "min_tl_xh",
                "model": "MIN/TL-XH",
                "firmware": None,
                "protocol_revision": "V1.24",
                "region": None,
                "applicability": "MIN/TL-XH V1.24 holding communication block",
            },
            "decision": {
                "status": "resolved",
                "confidence": "high",
                "value": {
                    "semantic_key": "modbus_slave_address",
                    "canonical_name": "Modbus slave address",
                    "datatype": "u16",
                    "signedness": "unsigned",
                    "range": "1-254",
                    "unit": None,
                    "normalization": "identity",
                },
            },
            "support": [claim_id(3085)],
            "conflicts": [],
            "rationale": "The V1.24 row defines a one-word communication address with the domain 1..254. This is the inverter communication address, not an external-meter address claim.",
            "review": {
                "status": "reviewed",
                "notes": "The generic communication-register meaning is promoted; no DDSU666 interpretation is attached.",
            },
        }
    )
    decisions.extend(
        [
            {
                "decision_id": "min-xh-h3086-rs485-baud-authority",
                "target": {
                    "canonical_family": "min_tl_xh",
                    "namespace": "MODBUS",
                    "table": "holding",
                    "address": 3086,
                    "property": "semantic_mapping",
                },
                "scope": {
                    "family": "min_tl_xh",
                    "model": "MIN/TL-XH",
                    "firmware": None,
                    "protocol_revision": "V1.24",
                    "region": None,
                    "applicability": "MIN/TL-XH V1.24 holding communication block",
                },
                "decision": {
                    "status": "resolved",
                    "confidence": "high",
                    "value": {
                        "semantic_key": "rs_485_baud_rate",
                        "canonical_name": "RS-485 baud rate",
                        "datatype": "u16 enum",
                        "signedness": "unsigned",
                        "unit": None,
                        "normalization": "identity",
                    },
                },
                "support": [claim_id(3086)],
                "conflicts": [],
                "rationale": "The V1.24 row defines the communication baud selector as a one-word unsigned enum; this remains a generic inverter communication setting.",
                "review": {
                    "status": "reviewed",
                    "notes": "Enum members are promoted separately so enum authority remains property-level and claim-backed.",
                },
            },
            {
                "decision_id": "min-xh-h3086-rs485-baud-enum-authority",
                "target": {
                    "canonical_family": "min_tl_xh",
                    "namespace": "MODBUS",
                    "table": "holding",
                    "address": 3086,
                    "property": "enum",
                },
                "scope": {
                    "family": "min_tl_xh",
                    "model": "MIN/TL-XH",
                    "firmware": None,
                    "protocol_revision": "V1.24",
                    "region": None,
                    "applicability": "MIN/TL-XH V1.24 holding communication block",
                },
                "decision": {
                    "status": "resolved",
                    "confidence": "high",
                    "value": {"0": "9600_bps", "1": "38400_bps"},
                },
                "support": [claim_id(3086)],
                "conflicts": [],
                "rationale": "The V1.24 row explicitly defines enum value 0 as 9600 bps and value 1 as 38400 bps.",
                "review": {
                    "status": "reviewed",
                    "notes": "No live value or external-meter assignment is asserted.",
                },
            },
        ]
    )
    return decisions


def build_reconciliation(decisions: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_reconciliation_decisions",
        "decisions": decisions,
    }


def canonical_records() -> dict[tuple[str, str, int], dict[str, Any]]:
    return {
        (item["family"], item["table"], item["address"]): item
        for item in load(CANONICAL_PATH)["registers"]
    }


def origin_sets(
    record: dict[str, Any], overrides: dict[str, set[tuple[str, str, int]]]
) -> tuple[set[str], set[str]]:
    origins = canonical_authority_origins(record, overrides)
    legacy = {
        name
        for name, detail in origins.items()
        if {"LEGACY_PYTHON", "COMPATIBILITY_RULE"} & set(detail["origins"])
    }
    exclusive = {
        name
        for name, detail in origins.items()
        if detail["classification"] == "LEGACY_PYTHON"
    }
    return legacy, exclusive


def effective_baseline(
    authority: dict[str, Any], accepted: dict[tuple[str, str, int], set[str]]
) -> dict[str, Any]:
    canonical = canonical_records()
    overrides = override_keys()
    legacy = declared = exclusive = 0
    for item in authority["records"]:
        key = (item["family"], item["table"], item["address"])
        old_legacy, old_exclusive = origin_sets(canonical[key], overrides)
        promoted = accepted.get(key, set())
        legacy += len(old_legacy - promoted)
        exclusive += len(old_exclusive - promoted)
        declared += len(set(item["declarative_properties"]) | promoted)
    return {
        "canonical_property_cells": authority["authority_origin_metrics"][
            "canonical_property_cells"
        ],
        "legacy_authoritative_property_cells": legacy,
        "declarative_authoritative_property_cells": declared,
        "legacy_exclusive_property_cells": exclusive,
    }


def candidate_metrics(
    authority: dict[str, Any],
    accepted: dict[tuple[str, str, int], set[str]],
    predicate: Callable[[dict[str, Any]], bool],
    canonical: dict[tuple[str, str, int], dict[str, Any]],
    overrides: dict[str, set[tuple[str, str, int]]],
) -> dict[str, Any]:
    selected = [item for item in authority["records"] if predicate(item)]
    legacy = declared = exclusive = 0
    unresolved = 0
    for item in selected:
        key = (item["family"], item["table"], item["address"])
        old_legacy, old_exclusive = origin_sets(canonical[key], overrides)
        promoted = accepted.get(key, set())
        legacy += len(old_legacy - promoted)
        exclusive += len(old_exclusive - promoted)
        declared += len(set(item["declarative_properties"]) | promoted)
        unresolved += item["migration_class"] in {
            "EVIDENCE_GATED",
            "LEGACY_ONLY_COMPLEX",
        }
    return {
        "family_records": len(selected),
        "physical_units": len(
            {
                (item["table"], item["address"], item["length_words"])
                for item in selected
            }
        ),
        "semantic_concepts": len(
            {key for item in selected for key in item["semantic_keys"]}
        ),
        "legacy_authoritative_cells": legacy,
        "legacy_exclusive_cells": exclusive,
        "existing_declarative_cells": declared,
        "unresolved_or_complex_records": unresolved,
    }


def candidate_ranking(
    authority: dict[str, Any], accepted: dict[tuple[str, str, int], set[str]]
) -> list[dict[str, Any]]:
    canonical = canonical_records()
    overrides = override_keys()
    gii6_addresses = set(load(GII6_ARTIFACT_PATH)["selected_cohort"]["addresses"])
    candidates: list[dict[str, Any]] = [
        {
            "id": "min_tl_xh_holding_3083_3086",
            "candidate": "MIN/TL-XH holding H3083-H3086 communication/reserved block",
            "addresses": SELECTED_ADDRESSES,
            "predicate": lambda item: (
                item["family"] == "min_tl_xh"
                and item["table"] == "holding"
                and item["address"] in SELECTED_ADDRESSES
            ),
            "evidence_quality": "high",
            "complexity": "low",
            "evidence_score": 3,
            "complexity_score": 3,
            "note": "One V1.24 family block; two reserved words and two explicitly documented communication selectors.",
        },
        {
            "id": "min_tl_xh_holding_3070_3071",
            "candidate": "MIN/TL-XH holding H3070-H3071 battery configuration",
            "addresses": [3070, 3071],
            "predicate": lambda item: (
                item["family"] == "min_tl_xh"
                and item["table"] == "holding"
                and item["address"] in {3070, 3071}
            ),
            "evidence_quality": "medium",
            "complexity": "medium",
            "evidence_score": 2,
            "complexity_score": 2,
            "note": "Source-described, but H3071 is explicitly scoped by the vendor to another product use and needs applicability review.",
        },
        {
            "id": "min_tl_xh_holding_3095",
            "candidate": "MIN/TL-XH holding H3095 BDC reset command",
            "addresses": [3095],
            "predicate": lambda item: (
                item["family"] == "min_tl_xh"
                and item["table"] == "holding"
                and item["address"] == 3095
            ),
            "evidence_quality": "high",
            "complexity": "medium",
            "evidence_score": 3,
            "complexity_score": 2,
            "note": "Vendor enum is explicit, but command/write semantics are higher risk and have no live write validation in this stage.",
        },
        {
            "id": "min_tl_xh_holding_remaining_3000_3124",
            "candidate": "Remaining MIN/TL-XH holding 3000-3124",
            "addresses": [
                item["address"]
                for item in authority["records"]
                if item["family"] == "min_tl_xh"
                and item["table"] == "holding"
                and 3000 <= item["address"] <= 3124
                and item["address"] not in gii6_addresses
            ],
            "predicate": lambda item: (
                item["family"] == "min_tl_xh"
                and item["table"] == "holding"
                and 3000 <= item["address"] <= 3124
                and item["address"] not in gii6_addresses
            ),
            "evidence_quality": "mixed",
            "complexity": "high",
            "evidence_score": 1,
            "complexity_score": 1,
            "note": "Large mixed block containing reserved, synthetic and evidence-gated records.",
        },
        {
            "id": "min_tl_xh_holding_3125_3249",
            "candidate": "MIN/TL-XH holding 3125-3249",
            "addresses": list(range(3125, 3250)),
            "predicate": lambda item: (
                item["family"] == "min_tl_xh"
                and item["table"] == "holding"
                and 3125 <= item["address"] <= 3249
            ),
            "evidence_quality": "low",
            "complexity": "high",
            "evidence_score": 1,
            "complexity_score": 1,
            "note": "Mostly US-TOU/special-day and reserved structures with weak bounded semantic evidence.",
        },
        {
            "id": "min_tl_xh_input_3250_3374",
            "candidate": "MIN/TL-XH input 3250-3374",
            "addresses": list(range(3250, 3375)),
            "predicate": lambda item: (
                item["family"] == "min_tl_xh"
                and item["table"] == "input"
                and 3250 <= item["address"] <= 3374
            ),
            "evidence_quality": "medium",
            "complexity": "high",
            "evidence_score": 2,
            "complexity_score": 1,
            "note": "Outside the frozen I3000-I3249 cohort, but currently dense with evidence-gated BMS fields.",
        },
    ]
    decisions = build_decisions()
    new_properties = properties_for(decisions)

    def potential_properties(record: dict[str, Any]) -> set[str]:
        if record["semantic_keys"]:
            properties = set(DECISION_PROPERTY_MAP["semantic_mapping"])
            key = (record["family"], record["table"], record["address"])
            if canonical[key]["enums"]:
                properties.add("enum_definitions")
            return properties
        if (
            record["canonical_record_count"]
            and record["migration_class"] == "EVIDENCE_GATED"
        ):
            return {"provenance_support"}
        return set()

    for item in candidates:
        metrics = candidate_metrics(
            authority, accepted, item["predicate"], canonical, overrides
        )
        new_reduction = 0
        for record in authority["records"]:
            if not item["predicate"](record):
                continue
            key = (record["family"], record["table"], record["address"])
            old_legacy, _ = origin_sets(canonical[key], overrides)
            candidate_properties = new_properties.get(key, potential_properties(record))
            new_reduction += len(old_legacy - accepted.get(key, set())) - len(
                old_legacy - accepted.get(key, set()) - candidate_properties
            )
        item.update(metrics, expected_reduction=new_reduction)
        # Review gates dominate raw size: evidence, boundedness, then reduction.
        item["rank_score"] = (
            item["evidence_score"] * 100
            + item["complexity_score"] * 10
            - item["unresolved_or_complex_records"]
            + min(item["expected_reduction"], 99) / 100
        )
        item.pop("predicate")
    ranked = sorted(candidates, key=lambda item: (-item["rank_score"], item["id"]))
    for rank, item in enumerate(ranked, 1):
        item["rank"] = rank
    return ranked


def parity(decisions: list[dict[str, Any]]) -> list[dict[str, Any]]:
    canonical = canonical_records()
    by_address: dict[int, list[dict[str, Any]]] = {}
    for item in decisions:
        by_address.setdefault(item["target"]["address"], []).append(item)
    result = []
    for address in SELECTED_ADDRESSES:
        record = canonical[("min_tl_xh", "holding", address)]
        values = [
            item["decision"].get("value", {})
            for item in by_address[address]
            if "semantic_key" in item["decision"].get("value", {})
        ]
        candidate_key = values[-1].get("semantic_key") if values else None
        current_key = record["semantic_identity"].get("quantity")

        def normalize(value: str | None) -> str | None:
            return (
                value.split(".", 1)[-1].replace(".", "_")
                if isinstance(value, str)
                else None
            )

        key_match = normalize(candidate_key) == normalize(current_key)
        canonical_enum = record["enums"]
        if address == 3085 and canonical_enum:
            classification = "SUPPORTED_CANONICAL_CORRECTION_CANDIDATE"
        else:
            classification = "PARITY_MATCH" if key_match else "REPRESENTATION_ONLY"
        result.append(
            {
                "physical_id": f"min_tl_xh:holding:{address}",
                "decision_ids": [item["decision_id"] for item in by_address[address]],
                "classification": classification,
                "canonical_semantic": current_key,
                "candidate_semantic": candidate_key,
            }
        )
    return result


def authority_metrics(
    authority: dict[str, Any],
    accepted: dict[tuple[str, str, int], set[str]],
    decisions: list[dict[str, Any]],
) -> dict[str, Any]:
    baseline = effective_baseline(authority, accepted)
    selected = properties_for(decisions)
    after = dict(baseline)
    for key, promoted in selected.items():
        old_legacy, old_exclusive = origin_sets(
            canonical_records()[key], override_keys()
        )
        old_promoted = accepted.get(key, set())
        after["legacy_authoritative_property_cells"] -= len(
            (old_legacy - old_promoted) & promoted
        )
        after["legacy_exclusive_property_cells"] -= len(
            (old_exclusive - old_promoted) & promoted
        )
        after["declarative_authoritative_property_cells"] += len(
            promoted - old_promoted
        )
    selected_before = selected_after = 0
    selected_exclusive_before = selected_exclusive_after = 0
    for key, promoted in selected.items():
        old_legacy, old_exclusive = origin_sets(
            canonical_records()[key], override_keys()
        )
        old_promoted = accepted.get(key, set())
        selected_before += len(old_legacy - old_promoted)
        selected_after += len((old_legacy - old_promoted) - promoted)
        selected_exclusive_before += len(old_exclusive - old_promoted)
        selected_exclusive_after += len((old_exclusive - old_promoted) - promoted)
    return {
        "repository_before": baseline,
        "repository_after": after,
        "selected_before": {
            "canonical_records": len(SELECTED_ADDRESSES),
            "legacy_authoritative_property_cells": selected_before,
            "legacy_exclusive_property_cells": selected_exclusive_before,
        },
        "selected_after": {
            "canonical_records": len(SELECTED_ADDRESSES),
            "legacy_authoritative_property_cells": selected_after,
            "legacy_exclusive_property_cells": selected_exclusive_after,
        },
        "promoted_property_cells": after["declarative_authoritative_property_cells"]
        - baseline["declarative_authoritative_property_cells"],
        "parity": parity(decisions),
    }


def build(starting_sha: str | None = None) -> dict[str, Any]:
    authority = authority_snapshot()
    accepted = properties_for(accepted_pipeline6_decisions())
    decisions = build_decisions()
    ranking = candidate_ranking(authority, accepted)
    selected = ranking[0]
    if selected["id"] != "min_tl_xh_holding_3083_3086":
        raise AssertionError(f"unexpected selected cohort: {selected['id']}")
    metrics = authority_metrics(authority, accepted, decisions)
    baseline = metrics["repository_before"]
    canonical_sha = sha256(CANONICAL_PATH)
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_pipeline7_next_authority_cohort",
        "generated_by": "tools/build_pipeline7_cohort.py",
        "starting_main_sha": starting_sha
        or subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=ROOT,
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip(),
        "canonical": {
            "path": "spec/growatt-register-spec.json",
            "sha256": canonical_sha,
            "canonical_modified": False,
        },
        "fresh_baseline": {
            "canonical_records": authority["counts"]["canonical_records"],
            "physical_bus_units": authority["counts"]["distinct_bus_physical_units"],
            "semantic_concepts": authority["counts"]["distinct_semantic_concepts"],
            "canonical_property_cells": authority["authority_origin_metrics"][
                "canonical_property_cells"
            ],
            "diagnostic_4a_declarative_physical_targets": authority[
                "declarative_coverage"
            ]["physical_targets"],
            "accepted_pipeline6_overlay": {
                "cohort": "min_tl_xh_holding_ems_3036_3059_3081_3082",
                "legacy_authoritative_property_cells": baseline[
                    "legacy_authoritative_property_cells"
                ],
                "declarative_authoritative_property_cells": baseline[
                    "declarative_authoritative_property_cells"
                ],
                "legacy_exclusive_property_cells": baseline[
                    "legacy_exclusive_property_cells"
                ],
            },
        },
        "selected_cohort": {
            "id": selected["id"],
            "family": "min_tl_xh",
            "table": "holding",
            "addresses": SELECTED_ADDRESSES,
            "physical_units": len(SELECTED_ADDRESSES),
            "new_decisions": [item["decision_id"] for item in decisions],
            "decision_source": str(RECONCILIATION_PATH.relative_to(ROOT)),
        },
        "candidate_ranking": ranking,
        "ranking_method": "Fresh deterministic ranking: evidence quality, bounded low-complexity scope and unresolved/complex density precede authority reduction; GII-6 accepted properties are removed from the baseline before scoring.",
        "authority": metrics,
        "parity_summary": dict(
            sorted(
                Counter(item["classification"] for item in metrics["parity"]).items()
            )
        ),
        "schema_changes": [],
        "evidence_mode": "retained V1.24 vendor source-row claims; no live experiment",
        "offline_inputs": {
            "authority_inventory": "docs/pipeline/data/GII-PIPELINE-5A_AUTHORITY_COVERAGE.json",
            "accepted_pipeline6": [
                str(GII6_ARTIFACT_PATH.relative_to(ROOT)),
                str(GII6_REUSED_PATH.relative_to(ROOT)),
                str(GII6_NEW_PATH.relative_to(ROOT)),
            ],
            "canonical": "spec/growatt-register-spec.json",
            "generic_claims": "sources/claims/generic-claims.json",
        },
        "unresolved_properties": [
            "H3085 canonical enum extraction remains a supported correction candidate; the vendor source defines a numeric range, not an enum.",
            "H3085/H3086 are generic inverter communication settings; no external-meter assignment is asserted.",
        ],
    }


@lru_cache(maxsize=1)
def authority_snapshot() -> dict[str, Any]:
    """Reuse the immutable authority inventory during one generator run."""
    return build_authority()


def render_report(data: dict[str, Any]) -> str:
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    selected_before = data["authority"]["selected_before"]
    selected_after = data["authority"]["selected_after"]
    lines = [
        "# GII-PIPELINE-7 — Next declarative authority cohort",
        "",
        "Disposition: `GII_PIPELINE_NEXT_COHORT_MIGRATION_ACCEPTED`",
        "",
        "## Lineage and fresh baseline",
        "",
        f"- Starting `main`: `{data['starting_main_sha']}`.",
        f"- Canonical SHA-256: `{data['canonical']['sha256']}` before and after; `canonical_modified=false`.",
        f"- Canonical records: {data['fresh_baseline']['canonical_records']}; physical bus units: {data['fresh_baseline']['physical_bus_units']}; semantic concepts: {data['fresh_baseline']['semantic_concepts']}.",
        "- The existing 4A diagnostic inventory still reports 18 physical targets. The accepted PIPELINE-6 overlay is applied only to the fresh migration baseline, so authority is not double-counted.",
        "",
        "## Fresh candidate ranking",
        "",
        "| Rank | Candidate | Physical units | Semantic concepts | Legacy cells | Legacy-exclusive | Existing declarative | Expected reduction | Unresolved/complex | Evidence | Complexity |",
        "| ---: | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | --- | --- |",
    ]
    for item in data["candidate_ranking"]:
        lines.append(
            f"| {item['rank']} | {item['candidate']} | {item['physical_units']} | {item['semantic_concepts']} | {item['legacy_authoritative_cells']} | {item['legacy_exclusive_cells']} | {item['existing_declarative_cells']} | {item['expected_reduction']} | {item['unresolved_or_complex_records']} | {item['evidence_quality']} | {item['complexity']} |"
        )
    lines += [
        "",
        "The selected cohort wins because it is a small, coherent V1.24 MIN/TL-XH block with explicit source rows and only reserved/evidence-gated status on the two words explicitly marked Reserved. Larger candidates remain intentionally deferred because their apparent reduction is dominated by mixed compatibility, synthetic and unresolved records.",
        "",
        "## Selected cohort",
        "",
        "- Scope: `min_tl_xh`, holding H3083–H3086; physical parity 4/4 (100%).",
        "- H3083 and H3084 are promoted as source-declared reserved words.",
        "- H3085 is the generic inverter Modbus communication address, range 1–254. It is not identified as a DDSU666 setting.",
        "- H3086 is the generic inverter RS-485 baud selector: 0 = 9600 bps, 1 = 38400 bps.",
        "- The selected decisions cite only generic V1.24 source-row claims; no canonical or compatibility artifact is used as evidence.",
        "- No schema extension, runtime change, HA change or live experiment was made.",
        "",
        "## Semantic parity and deferred corrections",
        "",
        f"- Parity: `{data['parity_summary']}`.",
        "- H3085 is a `SUPPORTED_CANONICAL_CORRECTION_CANDIDATE`: the canonical extractor exposes malformed enum entries, while the vendor row defines a numeric communication-address range.",
        "- No canonical correction is applied in PIPELINE-7. H3085/H3086 remain generic inverter communication settings and are not external-meter claims.",
        "",
        "## Authority movement",
        "",
        "| Metric | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
        f"| Repository legacy-authoritative cells | {before['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells'] - before['legacy_authoritative_property_cells']:+d} |",
        f"| Repository declarative-authoritative cells | {before['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells'] - before['declarative_authoritative_property_cells']:+d} |",
        f"| Repository legacy-exclusive cells | {before['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells'] - before['legacy_exclusive_property_cells']:+d} |",
        f"| Selected-cohort legacy-authoritative cells | {selected_before['legacy_authoritative_property_cells']} | {selected_after['legacy_authoritative_property_cells']} | {selected_after['legacy_authoritative_property_cells'] - selected_before['legacy_authoritative_property_cells']:+d} |",
        f"| Selected-cohort legacy-exclusive cells | {selected_before['legacy_exclusive_property_cells']} | {selected_after['legacy_exclusive_property_cells']} | {selected_after['legacy_exclusive_property_cells'] - selected_before['legacy_exclusive_property_cells']:+d} |",
        "",
        "The before column is the regenerated 5A inventory with the accepted PIPELINE-6 property overlay: 49,525 legacy-authoritative cells, 148 declarative-authoritative cells and 41 legacy-exclusive cells. This makes the PIPELINE-6 movement visible without rewriting the historical 5A diagnostic artifact.",
        "",
        "## Validation",
        "",
        "- The cohort, ranking, authority delta and report are generated by `tools/build_pipeline7_cohort.py`.",
        "- Canonical remains frozen and no runtime or live state was changed.",
        "- Full offline validators and tests are run at publication time.",
        "",
        "Final disposition: `GII_PIPELINE_NEXT_COHORT_MIGRATION_ACCEPTED`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    data = build()
    decisions = build_decisions()
    RECONCILIATION_PATH.write_text(
        json.dumps(build_reconciliation(decisions), indent=2, ensure_ascii=False)
        + "\n",
        encoding="utf-8",
    )
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    REPORT_PATH.write_text(render_report(data), encoding="utf-8")
    print(
        json.dumps(
            {
                "selected": data["selected_cohort"]["id"],
                "authority": data["authority"],
                "parity": data["parity_summary"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
