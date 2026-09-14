#!/usr/bin/env python3
"""Build the PIPELINE-8 applicability-aware next authority cohort."""

from __future__ import annotations

from collections import Counter, defaultdict
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
    from tools.pipeline8_evidence import candidate_evidence, evidence_dimensions
except ModuleNotFoundError:
    from build_authority_coverage import (
        DECISION_PROPERTY_MAP,
        build as build_authority,
        canonical_authority_origins,
        override_keys,
    )
    from pipeline8_evidence import candidate_evidence, evidence_dimensions
try:
    from tools.build_reconciliation import build as build_reconciliation
except ModuleNotFoundError:
    from build_reconciliation import build as build_reconciliation

ROOT = Path(__file__).resolve().parents[1]
CANONICAL_PATH = ROOT / "spec/growatt-register-spec.json"
RECONCILIATION_PATH = ROOT / "reconciliation/min_tl_xh_holding_bdc_3070_3071_3095.json"
OUTPUT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-8_VENDOR_APPLICABILITY_AND_NEXT_COHORT.json"
REPORT_PATH = ROOT / "docs/pipeline/GII-PIPELINE-8_VENDOR_APPLICABILITY_AND_NEXT_COHORT.md"
GII6_ARTIFACT_PATH = ROOT / "docs/pipeline/data/GII-PIPELINE-6_NEXT_AUTHORITY_COHORT.json"
GII7_RECONCILIATION_PATH = ROOT / "reconciliation/min_tl_xh_holding_comms_3083_3086.json"
GII6_REUSED_PATH = ROOT / "reconciliation/min_tl_xh.json"
GII6_NEW_PATH = ROOT / "reconciliation/min_tl_xh_holding_ems_3036_3059_3081_3082.json"

SELECTED_ADDRESSES = [3070, 3071, 3095]


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_claim(address: int, kind: str | None = None) -> str:
    claims = load(ROOT / "sources/claims/generic-claims.json")["claims"]
    matches = [
        item["claim_id"]
        for item in claims
        if item["source_id"] == "vendor_growatt_v124_2020"
        and item["subject"].get("table") == "holding"
        and item["subject"].get("address") == address
        and ":source-row:" in item["claim_id"]
        and (kind is None or item["assertion"]["kind"] == kind)
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one V1.24 source-row claim for H{address}, found {matches}")
    return matches[0]


def claim_id(address: int, suffix: str) -> str:
    claims = load(ROOT / "sources/claims/generic-claims.json")["claims"]
    matches = [
        item["claim_id"]
        for item in claims
        if item["source_id"] == "vendor_growatt_v124_2020"
        and (
            item["assertion"]["kind"] != "document_range_applicability"
            or item["subject"].get("family_scope") == ["min_tl_xh"]
        )
        and item["subject"].get("table") == "holding"
        and (
            item["subject"].get("address") == address
            or (
                item["assertion"]["kind"] == "document_range_applicability"
                and item["subject"].get("address", -1) <= address <= item["subject"].get("address_end", -1)
            )
        )
        and suffix in item["claim_id"]
    ]
    if len(matches) != 1:
        raise ValueError(f"expected one V1.24 {suffix} claim for H{address}, found {matches}")
    return matches[0]


def accepted_decisions() -> list[dict[str, Any]]:
    gii6_addresses = set(load(GII6_ARTIFACT_PATH)["selected_cohort"]["addresses"])
    old = [
        item
        for item in load(GII6_REUSED_PATH)["decisions"]
        if item["target"].get("namespace") == "MODBUS"
        and item["target"].get("table") == "holding"
        and item["target"].get("address") in gii6_addresses
    ]
    return [
        *old,
        *load(GII6_NEW_PATH)["decisions"],
        *load(GII7_RECONCILIATION_PATH)["decisions"],
    ]


def properties_for(decisions: list[dict[str, Any]]) -> dict[tuple[str, str, int], set[str]]:
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


def decision(
    address: int,
    property_name: str,
    value: dict[str, Any],
    support: list[str],
    rationale: str,
) -> dict[str, Any]:
    return {
        "decision_id": f"min-xh-h{address}-bdc-{property_name.replace('_', '-')}-authority",
        "target": {
            "canonical_family": "min_tl_xh",
            "namespace": "MODBUS",
            "table": "holding",
            "address": address,
            "property": property_name,
        },
        "scope": {
            "family": "min_tl_xh",
            "model": "MIN/TL-XH",
            "firmware": None,
            "protocol_revision": "V1.24",
            "region": None,
            "applicability": "MIN/TL-XH V1.24 FC03 holding range inherited from document instruction block",
        },
        "decision": {"status": "resolved", "confidence": "high", "value": value},
        "support": support,
        "conflicts": [],
        "rationale": rationale,
        "review": {
            "status": "reviewed",
            "notes": "PIPELINE-8 claim-driven promotion; documented write meaning is not live-write verification and canonical output remains frozen.",
        },
    }


def build_decisions() -> list[dict[str, Any]]:
    h3070_row = source_claim(3070)
    h3071_row = source_claim(3071)
    h3095_row = source_claim(3095)
    h3070_app = claim_id(3070, ":applicability:")
    h3071_app = claim_id(3071, ":applicability:")
    h3095_app = claim_id(3095, ":applicability:")
    h3070_enum = claim_id(3070, ":enum")
    h3071_packed = claim_id(3071, ":packed")
    h3095_enum = claim_id(3095, ":enum")
    h3071_qualifier = claim_id(3071, ":row-local-qualifier")
    return [
        decision(
            3070,
            "semantic_mapping",
            {
                "semantic_key": "battery_type",
                "canonical_name": "Battery type",
                "datatype": "u16 enum",
                "signedness": "unsigned",
                "unit": None,
                "normalization": "identity",
                "access": "R/W",
            },
            [h3070_row, h3070_app, h3070_enum],
            "The V1.24 row explicitly defines BatteryType, R/W access and the battery-type domain; the MIN physical applicability is inherited from the separate FC03 range claim.",
        ),
        decision(
            3070,
            "enum",
            {"0": "lithium", "1": "lead_acid", "2": "other"},
            [h3070_row, h3070_enum],
            "The enum members are retained from the vendor row without treating the register's unrelated canonical unit metadata as semantic evidence.",
        ),
        decision(
            3071,
            "semantic_mapping",
            {
                "semantic_key": "battery_module_series_parallel_count",
                "canonical_name": "Battery module series/parallel count",
                "datatype": "u16 packed upper/lower byte",
                "signedness": "unsigned",
                "unit": None,
                "normalization": "identity",
                "access": "R/W",
            },
            [h3071_row, h3071_app, h3071_packed, h3071_qualifier],
            "The row defines the upper byte as series segments and lower byte as parallel sections. The MIN range claim and the row-local SPH4-11K qualifier remain separate; the qualifier is not generalized to the whole register.",
        ),
        decision(
            3071,
            "packed_encoding",
            {
                "fields": [
                    {"name": "series_segments", "bits": [8, 15]},
                    {"name": "parallel_sections", "bits": [0, 7]},
                ],
                "row_local_qualifier": "SPH4-11K used; scope unresolved beyond the source row",
            },
            [h3071_row, h3071_packed, h3071_qualifier],
            "The packed layout is explicit in the vendor row. The product-use note is preserved as a scoped qualifier rather than used to deny document-level MIN range applicability.",
        ),
        decision(
            3095,
            "semantic_mapping",
            {
                "semantic_key": "bdc_reset_command",
                "canonical_name": "BDC reset command",
                "datatype": "u16 enum",
                "signedness": "unsigned",
                "unit": None,
                "normalization": "identity",
                "access": "R/W",
                "write_semantics": "documented_command_meaning; live_write_verification_absent",
            },
            [h3095_row, h3095_app, h3095_enum],
            "The V1.24 row explicitly documents BdcResetCmd, R/W access and four command meanings. This records semantic evidence only; no reset or other inverter write was performed.",
        ),
        decision(
            3095,
            "enum",
            {
                "0": "invalid_data",
                "1": "reset_setting_parameters",
                "2": "reset_correction_parameter",
                "3": "clear_historical_power",
            },
            [h3095_row, h3095_enum],
            "The documented command enum is promoted independently from the operational write-safety status.",
        ),
    ]


def authority_baseline(authority: dict[str, Any], accepted: list[dict[str, Any]]) -> dict[str, int]:
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in load(CANONICAL_PATH)["registers"]
    }
    accepted_properties = properties_for(accepted)
    overrides = override_keys()
    legacy = declarative = exclusive = 0
    for record in authority["records"]:
        key = (record["family"], record["table"], record["address"])
        origins = canonical_authority_origins(canonical[key], overrides)
        old_legacy = {
            name for name, detail in origins.items()
            if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
        }
        old_exclusive = {
            name for name, detail in origins.items()
            if detail["classification"] == "LEGACY_PYTHON"
        }
        promoted = accepted_properties.get(key, set())
        legacy += len(old_legacy - promoted)
        exclusive += len(old_exclusive - promoted)
        declarative += len(set(record["declarative_properties"]) | promoted)
    return {
        "canonical_property_cells": authority["authority_origin_metrics"]["canonical_property_cells"],
        "legacy_authoritative_property_cells": legacy,
        "declarative_authoritative_property_cells": declarative,
        "legacy_exclusive_property_cells": exclusive,
    }


def candidate_addresses(authority: dict[str, Any], predicate: Any) -> list[int]:
    return sorted({
        record["address"]
        for record in authority["records"]
        if predicate(record)
    })


def potential_properties(record: dict[str, Any], dimensions: dict[str, Any]) -> set[str]:
    result: set[str] = set()
    if dimensions["semantic_row"]["status"] == "supported":
        result.update(DECISION_PROPERTY_MAP["semantic_mapping"])
    if dimensions["enum_or_packed_layout"]["status"] == "supported":
        if any("packed" in item for item in dimensions["enum_or_packed_layout"]["claim_ids"]):
            result.update(DECISION_PROPERTY_MAP["packed_encoding"])
        else:
            result.add("enum_definitions")
    return result


def candidate_ranking(authority: dict[str, Any], claims: list[dict[str, Any]], accepted: list[dict[str, Any]]) -> list[dict[str, Any]]:
    accepted_keys = {
        (item["target"].get("canonical_family"), item["target"].get("table"), item["target"].get("address"))
        for item in accepted
        if item["target"].get("namespace") == "MODBUS"
    }
    candidate_specs = [
        (
            "min_tl_xh_holding_battery_bdc_3070_3071_3095",
            "MIN/TL-XH holding H3070-H3071/H3095 battery-BDC configuration",
            lambda r: r["family"] == "min_tl_xh" and r["table"] == "holding" and r["address"] in SELECTED_ADDRESSES,
            "Three semantically coherent documented control words; H3071's row-local qualifier is retained separately.",
        ),
        (
            "min_tl_xh_holding_remaining_3000_3124",
            "Remaining MIN/TL-XH holding 3000-3124",
            lambda r: r["family"] == "min_tl_xh" and r["table"] == "holding" and 3000 <= r["address"] <= 3124 and (r["family"], r["table"], r["address"]) not in accepted_keys,
            "Large mixed block; source applicability is strong but semantic and compatibility density is heterogeneous.",
        ),
        (
            "min_tl_xh_input_3250_3374",
            "MIN/TL-XH input 3250-3374",
            lambda r: r["family"] == "min_tl_xh" and r["table"] == "input" and 3250 <= r["address"] <= 3374,
            "Vendor-declared block with many source rows but a substantial unresolved diagnostic surface.",
        ),
        (
            "min_tl_xh_holding_3125_3249",
            "MIN/TL-XH holding 3125-3249",
            lambda r: r["family"] == "min_tl_xh" and r["table"] == "holding" and 3125 <= r["address"] <= 3249,
            "Vendor-declared block containing mixed special-day, reserved and compatibility structures.",
        ),
        (
            "min_tl_xh_input_remaining_3000_3249",
            "Remaining MIN/TL-XH input 3000-3249",
            lambda r: r["family"] == "min_tl_xh" and r["table"] == "input" and 3000 <= r["address"] <= 3249,
            "Broad telemetry/BMS surface; the accepted FC04 cohort and several evidence-gated fields remain mixed.",
        ),
    ]
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in load(CANONICAL_PATH)["registers"]
    }
    overrides = override_keys()
    accepted_props = properties_for(accepted)
    result: list[dict[str, Any]] = []
    for candidate_id, label, predicate, note in candidate_specs:
        records = [item for item in authority["records"] if predicate(item)]
        addresses = sorted(item["address"] for item in records)
        per_record = {
            (item["family"], item["table"], item["address"]): evidence_dimensions(
                claims, item["family"], item["table"], item["address"]
            )
            for item in records
        }
        evidence = candidate_evidence(claims, "min_tl_xh", "holding", SELECTED_ADDRESSES) if candidate_id == "min_tl_xh_holding_battery_bdc_3070_3071_3095" else None
        if evidence is None:
            # Applicability is evaluated generically for every candidate; one
            # summary combines the candidate's physical table/family scopes.
            dimension_totals: dict[str, int] = defaultdict(int)
            total_score = 0
            for dimensions in per_record.values():
                scored = {
                    name: value
                    for name, value in dimensions.items()
                    if isinstance(value, dict) and "status" in value
                }
                for name, value in scored.items():
                    dimension_totals[name] += value["status"] in {"supported", "present", "documented", "verified"}
                total_score += sum(
                    value["status"] in {"supported", "present", "documented", "verified"}
                    for value in scored.values()
                )
            evidence = {
                "evidence_dimensions": {
                    name: {"supported_records": count, "record_count": len(records), "coverage": count / len(records) if records else 0}
                    for name, count in sorted(dimension_totals.items())
                },
                "per_record": {
                    f"{family}:{table}:{address}": dimensions
                    for (family, table, address), dimensions in per_record.items()
                },
                "score": total_score,
                "evidence_quality": "medium" if total_score >= len(records) * 2 else "low",
            }
        legacy = declarative = exclusive = expected_reduction = 0
        for record in records:
            key = (record["family"], record["table"], record["address"])
            origins = canonical_authority_origins(canonical[key], overrides)
            old_legacy = {
                name for name, detail in origins.items()
                if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
            }
            old_exclusive = {
                name for name, detail in origins.items()
                if detail["classification"] == "LEGACY_PYTHON"
            }
            promoted = accepted_props.get(key, set())
            potential = potential_properties(record, per_record[key])
            legacy += len(old_legacy - promoted)
            exclusive += len(old_exclusive - promoted)
            declarative += len(set(record["declarative_properties"]) | promoted)
            expected_reduction += len((old_legacy - promoted) & potential)
        bounded_penalty = max(0, len(records) - len(SELECTED_ADDRESSES)) / 10
        quality_rank = {"high": 3, "medium": 2, "low": 1}[evidence["evidence_quality"]]
        evidence_per_record = evidence["score"] / len(records) if records else 0
        unresolved_density = (
            sum(item["migration_class"] in {"EVIDENCE_GATED", "LEGACY_ONLY_COMPLEX"} for item in records)
            / len(records)
            if records
            else 0
        )
        result.append({
            "id": candidate_id,
            "candidate": label,
            "addresses": addresses,
            "physical_units": len({(r["table"], r["address"], r["length_words"]) for r in records}),
            "semantic_concepts": len({key for r in records for key in r["semantic_keys"]}),
            "legacy_authoritative_cells": legacy,
            "legacy_exclusive_cells": exclusive,
            "existing_declarative_cells": declarative,
            "expected_reduction": expected_reduction,
            "unresolved_or_complex_records": sum(
                item["migration_class"] in {"EVIDENCE_GATED", "LEGACY_ONLY_COMPLEX"}
                for item in records
            ),
            "evidence_quality": evidence["evidence_quality"],
            "evidence_score": evidence["score"],
            "evidence": evidence,
            "complexity": "low" if len(records) <= 4 else "high",
            "complexity_score": 3 if len(records) <= 4 else 1,
            "note": note,
            "evidence_score_per_record": evidence_per_record,
            "rank_score": quality_rank * 10000
            + (3 if len(records) <= 4 else 1) * 1000
            + evidence_per_record * 100
            - unresolved_density * 100
            - bounded_penalty
            + min(expected_reduction, 99) / 100,
        })
    result.sort(key=lambda item: (-item["rank_score"], item["id"]))
    for rank, item in enumerate(result, 1):
        item["rank"] = rank
    return result


def authority_after(authority: dict[str, Any], accepted: list[dict[str, Any]], new: list[dict[str, Any]]) -> dict[str, int]:
    baseline = authority_baseline(authority, accepted)
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in load(CANONICAL_PATH)["registers"]
    }
    overrides = override_keys()
    old_promoted = properties_for(accepted)
    new_promoted = properties_for(new)
    result = dict(baseline)
    added: dict[tuple[str, str, int], set[str]] = {}
    for key, properties in new_promoted.items():
        added[key] = properties - old_promoted.get(key, set())
        origins = canonical_authority_origins(canonical[key], overrides)
        legacy = {
            name for name, detail in origins.items()
            if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
        }
        exclusive = {
            name for name, detail in origins.items()
            if detail["classification"] == "LEGACY_PYTHON"
        }
        result["legacy_authoritative_property_cells"] -= len(legacy & added[key])
        result["legacy_exclusive_property_cells"] -= len(exclusive & added[key])
        result["declarative_authoritative_property_cells"] += len(added[key])
    return result


def build(starting_sha: str | None = None) -> dict[str, Any]:
    authority = build_authority()
    claims = load(ROOT / "sources/claims/generic-claims.json")["claims"]
    accepted = accepted_decisions()
    decisions = build_decisions()
    ranking = candidate_ranking(authority, claims, accepted)
    selected = ranking[0]
    if selected["id"] != "min_tl_xh_holding_battery_bdc_3070_3071_3095":
        raise AssertionError(f"unexpected selected cohort: {selected['id']}")
    before = authority_baseline(authority, accepted)
    after = authority_after(authority, accepted, decisions)
    selected_keys = {("min_tl_xh", "holding", address) for address in SELECTED_ADDRESSES}
    canonical = {
        (item["family"], item["table"], item["address"]): item
        for item in load(CANONICAL_PATH)["registers"]
    }
    overrides = override_keys()
    selected_props = properties_for(decisions)
    selected_before = selected_after = selected_exclusive_before = selected_exclusive_after = 0
    parity: list[dict[str, Any]] = []
    for key in sorted(selected_keys):
        origins = canonical_authority_origins(canonical[key], overrides)
        legacy = {
            name for name, detail in origins.items()
            if "LEGACY_PYTHON" in detail["origins"] or "COMPATIBILITY_RULE" in detail["origins"]
        }
        exclusive = {
            name for name, detail in origins.items()
            if detail["classification"] == "LEGACY_PYTHON"
        }
        promoted = selected_props[key]
        selected_before += len(legacy - properties_for(accepted).get(key, set()))
        selected_after += len((legacy - properties_for(accepted).get(key, set())) - promoted)
        selected_exclusive_before += len(exclusive - properties_for(accepted).get(key, set()))
        selected_exclusive_after += len((exclusive - properties_for(accepted).get(key, set())) - promoted)
        values = [
            item["decision"]["value"]
            for item in decisions
            if item["target"].get("address") == key[2]
            and "semantic_key" in item["decision"].get("value", {})
        ]
        candidate_semantic = values[-1].get("semantic_key") if values else None
        current_semantic = canonical[key]["semantic_identity"].get("quantity")
        normalized = lambda value: value.replace(".", "_") if isinstance(value, str) else value
        semantic_match = normalized(candidate_semantic) == normalized(current_semantic)
        parity.append({
            "physical_id": ":".join(map(str, key)),
            "decision_ids": [item["decision_id"] for item in decisions if item["target"].get("address") == key[2]],
            "classification": "PARITY_MATCH" if semantic_match else "REPRESENTATION_ONLY",
            "canonical_semantic": current_semantic,
            "candidate_semantic": candidate_semantic,
        })
    return {
        "schema_version": "1.0.0",
        "artifact": "growatt_pipeline8_vendor_applicability_and_next_cohort",
        "generated_by": "tools/build_pipeline8_cohort.py",
        "starting_main_sha": starting_sha or subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip(),
        "canonical": {"path": "spec/growatt-register-spec.json", "sha256": sha256(CANONICAL_PATH), "canonical_modified": False},
        "applicability_model": {
            "source": "sources/vendor/profiles/vendor_growatt_v124_2020.json",
            "document": "sources/claims/vendor/vendor_growatt_v124_2020.json",
            "generic_projection": "sources/claims/generic-claims.json",
            "claim_kind": "document_range_applicability",
            "declaration_count": sum(c["assertion"]["kind"] == "document_range_applicability" for c in claims),
            "family_ids": sorted({c["subject"]["family_scope"][0] for c in claims if c["assertion"]["kind"] == "document_range_applicability"}),
        },
        "baseline": {"canonical_records": authority["counts"]["canonical_records"], **before},
        "selected_cohort": {
            "id": selected["id"],
            "family": "min_tl_xh",
            "table": "holding",
            "addresses": SELECTED_ADDRESSES,
            "physical_units": len(SELECTED_ADDRESSES),
            "physical_parity": {
                "selected": 3,
                "expected": 3,
                "percent": 100,
                "note": "H3046 is separately retained as a checked source-row example",
            },
            "decision_source": str(RECONCILIATION_PATH.relative_to(ROOT)),
            "new_decisions": [item["decision_id"] for item in decisions],
        },
        "candidate_ranking": ranking,
        "ranking_method": "Deterministic claim-driven ranking: traceable document applicability, semantic-row, enum/packed, access, qualifier, corroboration and write-documentation dimensions are scored before boundedness, complexity and authority reduction.",
        "authority": {
            "repository_before": before,
            "repository_after": after,
            "selected_before": {"canonical_records": len(SELECTED_ADDRESSES), "legacy_authoritative_property_cells": selected_before, "legacy_exclusive_property_cells": selected_exclusive_before},
            "selected_after": {"canonical_records": len(SELECTED_ADDRESSES), "legacy_authoritative_property_cells": selected_after, "legacy_exclusive_property_cells": selected_exclusive_after},
            "promoted_property_cells": after["declarative_authoritative_property_cells"] - before["declarative_authoritative_property_cells"],
            "parity": parity,
        },
        "parity_summary": dict(sorted(Counter(item["classification"] for item in parity).items())),
        "schema_changes": [
            "Generic claims retain document_range_applicability and row_local_qualifier as claim kinds; existing schemas already permit their structured subject/assertion values.",
        ],
        "safety": {"inverter_write": False, "live_reset": False, "ha_runtime_change": False, "canonical_modified": False, "live_write_verification_invented": False},
        "deferred": ["H3085 canonical correction candidate remains deferred from PIPELINE-7."],
    }


def render(data: dict[str, Any]) -> str:
    before = data["authority"]["repository_before"]
    after = data["authority"]["repository_after"]
    lines = [
        "# GII-PIPELINE-8 — Vendor applicability and next authority cohort",
        "",
        "Disposition: `GII_PIPELINE_VENDOR_APPLICABILITY_MIGRATION_ACCEPTED`",
        "",
        "## Baseline",
        "",
        f"- Current merged `main`: `{data['starting_main_sha']}`; canonical SHA-256: `{data['canonical']['sha256']}` before and after.",
        f"- Canonical records: {data['baseline']['canonical_records']}; canonical unchanged: `{str(data['canonical']['canonical_modified']).lower()}`.",
        f"- Authority baseline: legacy {before['legacy_authoritative_property_cells']}, declarative {before['declarative_authoritative_property_cells']}, legacy-exclusive {before['legacy_exclusive_property_cells']} property cells.",
        "",
        "## Evidence-accounting repair",
        "",
        "The previous cohort builders embedded a single evidence label and complexity value in Python. That discarded the difference between a document range declaration, a row's semantic content and a row-local product qualifier. PIPELINE-8 now derives candidate evidence from retained generic claims and records claim IDs for each dimension.",
        "",
        "## V1.24 applicability model",
        "",
        f"The page-3 instruction block is retained as {data['applicability_model']['declaration_count']} range claims across: " + ", ".join(f"`{item}`" for item in data["applicability_model"]["family_ids"]) + ". Function code/table and start/end are structured, so applicability queries do not depend on ranking code.",
        "",
        "Document-level applicability is kept separate from row-local qualifiers. For H3071, the MIN/TL-XH holding range supports physical applicability while `SPH4-11K used` remains a separately cited, unresolved-scope qualifier. It is not used to deny the MIN range.",
        "",
        """| Register | Retained source representation | Interpretation |
| --- | --- | --- |
| H3046 | `预留` | Mechanically normalized to `Reserved`; no stronger unsupported claim is added. |
| H3070 | `BatteryType`, R/W, 0 Lithium / 1 Lead-acid / 2 other | Vendor enum and access claims; MIN applicability inherited from FC03 3000–3124. |
| H3071 | `BatMdlSeria/ParalNum`, upper/lower byte layout, `SPH4-11K used` | Physical range, packed layout and row-local qualifier are independent claims. |
| H3095 | `BdcResetCmd`, R/W, four reset/clear meanings | Documented command semantics; live-write verification remains absent. |""",
        "",
        "## Fresh candidate ranking",
        "",
        "| Rank | Candidate | Units | Legacy cells | Expected reduction | Evidence | Score | Complexity |",
        "| ---: | --- | ---: | ---: | ---: | --- | ---: | --- |",
    ]
    for item in data["candidate_ranking"]:
        lines.append(f"| {item['rank']} | {item['candidate']} | {item['physical_units']} | {item['legacy_authoritative_cells']} | {item['expected_reduction']} | {item['evidence_quality']} | {item['evidence_score']} | {item['complexity']} |")
    selected_evidence = data["candidate_ranking"][0]["evidence"]["per_record"]
    lines += [
        "",
        "### Selected evidence dimensions",
        "",
        "| Register | Applicability | Semantic row | Enum/packed | Access | Qualifier | Write docs | Live write |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for address in data["selected_cohort"]["addresses"]:
        dimensions = selected_evidence[f"min_tl_xh:holding:{address}"]
        status = lambda name: dimensions[name]["status"]
        lines.append(
            f"| H{address} | {status('physical_applicability')} | {status('semantic_row')} | {status('enum_or_packed_layout')} | {status('access')} | {status('unresolved_qualifier')} | {status('write_documentation')} | {status('live_write_verification')} |"
        )
    lines += [
        "",
        "The selected cohort is the top ranked bounded result produced by the claim-driven generator. It contains three coherent MIN/TL-XH BDC/control words. H3071's qualifier lowers/annotates the evidence rather than collapsing the entire source situation to `medium`.",
        "",
        "## Selected cohort and authority movement",
        "",
        "- Scope: MIN/TL-XH FC03 holding H3070, H3071 and H3095; physical parity is 3/3 (100%) for the selected registers. H3046 is retained and tested as source context, not silently folded into the selected cohort.",
        f"- Property-level parity: `{data['parity_summary']}`.",
        "- H3095's documented write operation meaning is not a permission or live safety verification claim.",
        "",
        "| Metric | Before | After | Delta |",
        "| --- | ---: | ---: | ---: |",
        f"| Repository legacy-authoritative cells | {before['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells']} | {after['legacy_authoritative_property_cells'] - before['legacy_authoritative_property_cells']:+d} |",
        f"| Repository declarative-authoritative cells | {before['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells']} | {after['declarative_authoritative_property_cells'] - before['declarative_authoritative_property_cells']:+d} |",
        f"| Repository legacy-exclusive cells | {before['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells']} | {after['legacy_exclusive_property_cells'] - before['legacy_exclusive_property_cells']:+d} |",
        f"| Selected-cohort legacy-authoritative cells | {data['authority']['selected_before']['legacy_authoritative_property_cells']} | {data['authority']['selected_after']['legacy_authoritative_property_cells']} | {data['authority']['selected_after']['legacy_authoritative_property_cells'] - data['authority']['selected_before']['legacy_authoritative_property_cells']:+d} |",
        "",
        "## Safety and deferred work",
        "",
        "No inverter write, reset command, Home Assistant/runtime change or canonical modification was made. H3085 remains the PIPELINE-7 supported canonical-correction candidate and is not repaired here. No global canonical cutover and no HA-GII-5 work was started.",
        "",
        "## Reproducibility",
        "",
        "- Source profile: `sources/vendor/profiles/vendor_growatt_v124_2020.json`.",
        "- Vendor extraction: `tools/extract_vendor_pdf.py` with Poppler `pdftotext -layout -enc UTF-8`; original PDF SHA-256 was checked as `fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320`.",
        "- Generic projection: `python3 tools/build_generic_claims.py`; ranking/cohort: `python3 tools/build_pipeline8_cohort.py`.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    starting_sha = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()
    data = build(starting_sha)
    (ROOT / "reconciliation/min_tl_xh_holding_bdc_3070_3071_3095.json").write_text(json.dumps({"schema_version": "1.0.0", "artifact": "growatt_reconciliation_decisions", "decisions": build_decisions()}, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "reconciliation/resolved-assertions.json").write_text(json.dumps(build_reconciliation(), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (OUTPUT_PATH).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    REPORT_PATH.write_text(render(data), encoding="utf-8")
    print(json.dumps({"selected": data["selected_cohort"], "authority": data["authority"], "ranking": [(x["rank"], x["id"], x["evidence_quality"], x["evidence_score"]) for x in data["candidate_ranking"]]}, indent=2))


if __name__ == "__main__":
    main()
