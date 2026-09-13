#!/usr/bin/env python3
"""Build the source-independent claim projection without reconciling it."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CLAIMS_DIR = ROOT / "sources" / "claims"

VENDOR_FILES = [
    "vendor/vendor_growatt_v305_2013.json",
    "vendor/vendor_growatt_v314_2016.json",
    "vendor/vendor_growatt_v124_2020.json",
]
KEY_ADDRESSES = {
    ("holding", address)
    for address in [3036, 3037, *range(3038, 3060), 3081, 3082]
} | {
    ("input", address)
    for address in [3000, 3101, 3110, 3111, 3165, 3166, 3170, 3211, 3212, 3217]
}


def load(relative: str) -> Any:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def dump(value: Any, relative: str) -> None:
    path = ROOT / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def scope(family: Any, applicability: str, **extra: Any) -> dict[str, Any]:
    return {"family": family, "applicability": applicability, **extra}


def subject(
    namespace: str,
    family: Any,
    table: str | None = None,
    address: int | None = None,
    address_end: int | None = None,
    logical_object: str | None = None,
    field: str | None = None,
) -> dict[str, Any]:
    result: dict[str, Any] = {"namespace": namespace, "family_scope": family}
    if table is not None:
        result["table"] = table
    if address is not None:
        result["address"] = address
    if address_end is not None:
        result["address_end"] = address_end
    if logical_object is not None:
        result["logical_object"] = logical_object
    if field is not None:
        result["field"] = field
    return result


def claim(
    claim_id: str,
    source_id: str,
    source_type: str,
    claim_subject: dict[str, Any],
    kind: str,
    value: Any,
    provenance: dict[str, Any],
    claim_scope: dict[str, Any],
    method: str,
    confidence: str,
    status: str,
    **assertion: Any,
) -> dict[str, Any]:
    assertion_data = {"kind": kind, "value": value, **assertion}
    return {
        "claim_id": claim_id,
        "source_id": source_id,
        "source_type": source_type,
        "subject": claim_subject,
        "assertion": assertion_data,
        "provenance": provenance,
        "scope": claim_scope,
        "evidence": {"method": method, "confidence": confidence, "status": status},
    }


def vendor_claims() -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for relative in VENDOR_FILES:
        document = load(f"sources/claims/{relative}")
        doc = document["document"]
        source_id = doc["document_id"]
        source_type = "vendor_document"
        for row in document["claims"]:
            address = row["parsed_address"]
            address_end = row["parsed_address_end"]
            family = row["family_scope"]
            if address is None:
                row_subject = subject(
                    "LOGICAL", family, logical_object=f"vendor_row:{row['source_row_id']}", field="source_row"
                )
            else:
                row_subject = subject(
                    "MODBUS", family, row["register_table"], address, address_end
                )
            provenance = {
                "source_artifact": f"sources/claims/{relative}",
                "document_sha256": row["document_sha256"],
                "page": row["page"],
                "page_end": row["page_end"],
                "section": row["section_id"],
                "source_row": row["source_row_id"],
            }
            row_value = {
                key: copy.deepcopy(row[key])
                for key in (
                    "raw_address_expression", "parsed_address", "parsed_address_end",
                    "raw_variable", "reconstructed_variable", "raw_description",
                    "raw_value_text", "raw_unit_text", "raw_access_text", "raw_initial_text",
                    "raw_note", "raw_row_text", "reconstructed_row_text", "source_status",
                    "continuation_refs", "source_fragments", "diagnostics", "review_note",
                )
                if key in row
            }
            result.append(claim(
                f"{source_id}:source-row:{row['claim_id']}", source_id, source_type, row_subject,
                "vendor_source_row", row_value, provenance,
                scope(family, "vendor row scope", protocol_revision=doc.get("declared_revision")),
                "vendor_documented", row["extraction_confidence"], row["source_status"],
                source_text=row.get("raw_row_text"), raw_value=row_value,
            ))
            if address is None or (row["register_table"], address) not in KEY_ADDRESSES:
                continue
            base = f"{source_id}:assertion:{row['claim_id']}"
            if row.get("raw_variable") or row.get("reconstructed_variable"):
                result.append(claim(
                    f"{base}:name", source_id, source_type, row_subject, "register_name",
                    row.get("reconstructed_variable") or row.get("raw_variable"), provenance,
                    scope(family, "vendor row scope", protocol_revision=doc.get("declared_revision")),
                    "vendor_documented", row["extraction_confidence"], row["source_status"],
                    source_text=row.get("raw_variable"), raw_value=row.get("raw_variable"),
                ))
            if row.get("raw_access_text"):
                result.append(claim(
                    f"{base}:access", source_id, source_type, row_subject, "access",
                    row["raw_access_text"], provenance,
                    scope(family, "vendor row scope", protocol_revision=doc.get("declared_revision")),
                    "vendor_documented", row["extraction_confidence"], row["source_status"],
                    source_text=row["raw_access_text"], raw_value=row["raw_access_text"],
                ))
            description = " ".join(filter(None, [row.get("raw_description"), row.get("raw_note")]))
            if description:
                result.append(claim(
                    f"{base}:description", source_id, source_type, row_subject, "description",
                    description, provenance,
                    scope(family, "vendor row scope", protocol_revision=doc.get("declared_revision")),
                    "vendor_documented", row["extraction_confidence"], row["source_status"],
                    source_text=row.get("raw_description"), raw_value=row.get("raw_note"),
                ))
            if row.get("raw_note") and ("Bit" in row["raw_note"] or "bit" in row["raw_note"]):
                result.append(claim(
                    f"{base}:packed", source_id, source_type, row_subject, "packed_field",
                    row["raw_note"], provenance,
                    scope(family, "vendor row scope", protocol_revision=doc.get("declared_revision")),
                    "vendor_documented", row["extraction_confidence"], row["source_status"],
                    source_text=row["raw_note"], raw_value=row["raw_value_text"],
                ))
            if row.get("raw_value_text") and (":" in row["raw_value_text"] or "0=" in row["raw_value_text"]):
                result.append(claim(
                    f"{base}:enum", source_id, source_type, row_subject, "enum_member",
                    row["raw_value_text"], provenance,
                    scope(family, "vendor row scope", protocol_revision=doc.get("declared_revision")),
                    "vendor_documented", row["extraction_confidence"], row["source_status"],
                    source_text=row["raw_value_text"], raw_value=row["raw_value_text"],
                ))
    return result


def live_claims() -> list[dict[str, Any]]:
    data = load("sources/evidence/min-6000tl-xh-live-validation.json")
    result: list[dict[str, Any]] = []
    family = ["MIN 6000TL-XH"]
    base_prov = {"source_artifact": "sources/evidence/min-6000tl-xh-live-validation.json", "timestamp": data["meta"]["captured_at"]}
    groups = {
        "fc03_3036_count14_registers": ("holding", 3036),
        "fc03_3081_count2_registers": ("holding", 3081),
        "fc03_3050_count10_registers": ("holding", 3050),
        "fc03_3070_count3_registers": ("holding", 3070),
        "fc03_3079_count4_registers": ("holding", 3079),
        "fc04_3000_count11_registers": ("input", 3000),
        "fc04_3021_count13_registers": ("input", 3021),
        "fc04_3043_count4_registers": ("input", 3043),
        "fc04_3164_count18_registers": ("input", 3164),
    }
    for sample_index, sample in enumerate(data["telemetry_samples"]):
        for key, (table, start) in groups.items():
            if table != "input":
                continue
            values = sample.get(key) or data.get("holding_ems", {}).get(key)
            if values is None:
                continue
            for offset, raw in enumerate(values):
                address = start + offset
                if (table, address) not in KEY_ADDRESSES:
                    continue
                provenance = {**base_prov, "json_pointer": f"/telemetry_samples/{sample_index}/{key}/{offset}", "record_id": f"sample-{sample_index}-{key}"}
                result.append(claim(
                    f"min_live:raw:{table}:{address}:sample-{sample_index}", "min_live_validation", "live_modbus_observation",
                    subject("MODBUS", family, table, address), "raw_read_observation", raw, provenance,
                    scope(family, "retained read-only MIN 6000TL-XH sample", model="MIN 6000TL-XH", protocol_revision="V1.24"),
                    "live_read_observed", "high", "observed", raw_value=raw,
                ))
        decoded = sample.get("decoded", {})
        decoded_map = {
            "status": ("input", 3000), "battery_voltage_v": ("input", 3169),
            "battery_current_a": ("input", 3170), "battery_soc_pct": ("input", 3171),
            "battery_discharge_w": ("input", 3179), "battery_charge_w": ("input", 3180),
        }
        for field, value in decoded.items():
            if field not in decoded_map:
                continue
            table, address = decoded_map[field]
            result.append(claim(
                f"min_live:decoded:{field}:sample-{sample_index}", "min_live_validation", "live_modbus_observation",
                subject("MODBUS", family, table, address), "decoded_read_observation", value,
                {**base_prov, "json_pointer": f"/telemetry_samples/{sample_index}/decoded/{field}", "record_id": f"sample-{sample_index}"},
                scope(family, "retained read-only MIN 6000TL-XH sample", model="MIN 6000TL-XH", protocol_revision="V1.24"),
                "live_decode_correlated", "high", "observed",
            ))
    holding = data["holding_ems"]
    for key, values in holding.items():
        if not key.endswith("_registers"):
            continue
        start = int(key.split("_")[1])
        for offset, raw in enumerate(values):
            address = start + offset
            if ("holding", address) not in KEY_ADDRESSES:
                continue
            result.append(claim(
                f"min_live:holding:{address}:{key}", "min_live_validation", "live_modbus_observation",
                subject("MODBUS", family, "holding", address), "raw_read_observation", raw,
                {**base_prov, "json_pointer": f"/holding_ems/{key}/{offset}", "record_id": key},
                scope(family, "retained read-only EMS holding sample", model="MIN 6000TL-XH", protocol_revision="V1.24"),
                "live_read_observed", "high", "observed", raw_value=raw,
            ))
    return result


def map_claims() -> list[dict[str, Any]]:
    data = load("sources/evidence/min-6000tl-xh-register-map.json")
    result: list[dict[str, Any]] = []
    for table in ("holding", "input"):
        for index, row in enumerate(data[table]):
            address = row["register"]
            if (table, address) not in KEY_ADDRESSES:
                continue
            result.append(claim(
                f"min_register_map:{table}:{address}:{index}", "min_register_map", "retained_evidence_map",
                subject("MODBUS", ["MIN 6000TL-XH"], table, address), "description", row,
                {"source_artifact": "sources/evidence/min-6000tl-xh-register-map.json", "json_pointer": f"/{table}/{index}"},
                scope(["MIN 6000TL-XH"], "retained evidence map", model="MIN 6000TL-XH"),
                "human_reviewed_evidence_map", row.get("confidence", "unknown"), "retained",
            ))
    return result


def semantic_review_claims() -> list[dict[str, Any]]:
    data = load("sources/evidence/min-6000tl-xh-semantic-review.json")
    result: list[dict[str, Any]] = []
    for index, row in enumerate(data["records"]):
        if "address" not in row or (row["table"], row["address"]) not in KEY_ADDRESSES:
            continue
        result.append(claim(
            f"min_semantic_review:{row['table']}:{row['address']}:{index}", "min_semantic_review", "human_review_artifact",
            subject("MODBUS", ["MIN 6000TL-XH"], row["table"], row["address"]), "human_interpretation", row,
            {"source_artifact": "sources/evidence/min-6000tl-xh-semantic-review.json", "json_pointer": f"/records/{index}"},
            scope(["MIN 6000TL-XH"], "review artifact scope", model="MIN 6000TL-XH"),
            "human_interpretation", row.get("confidence", "unknown"), row.get("resolution_status", "reviewed"),
        ))
    return result


def cloud_claims() -> list[dict[str, Any]]:
    data = load("sources/evidence/min-6000tl-xh-cloud-oracle-validation.json")
    result: list[dict[str, Any]] = []
    for index, row in enumerate(data["records"]):
        result.append(claim(
            f"min_cloud_oracle:input:{row['address']}:{index}", "min_cloud_oracle", "cloud_api_correlation",
            subject("MODBUS", ["MIN 6000TL-XH"], "input", row["address"]), "cloud_field_observation", row,
            {"source_artifact": "sources/evidence/min-6000tl-xh-cloud-oracle-validation.json", "json_pointer": f"/records/{index}", "record_id": str(index)},
            scope(["MIN 6000TL-XH"], "bounded read-only cloud-correlation experiment", model="MIN 6000TL-XH"),
            "cloud_correlated" if row["result"] != "not_discriminating" else "non_discriminating_experiment",
            row["confidence"], row["result"], raw_value=row["injected_value"], observation=row.get("cloud_fields"),
        ))
    return result


def shine_claims() -> list[dict[str, Any]]:
    data = load("sources/evidence/min-6000tl-xh-shine-tou-write.json")
    prov = {"source_artifact": "sources/evidence/min-6000tl-xh-shine-tou-write.json", "json_pointer": "/"}
    family = ["MIN/TL-XH"]
    result = [claim(
        "min_shine_tou:write:h3040-h3041", "min_shine_tou_write", "stock_shine_observation",
        subject("LOGICAL", family, logical_object="xh_schedule_slot_2", field="write_transition"),
        "stock_shine_write_observation", data["state_transition"], prov,
        scope(family, "natural portal/stock-Shine event", model="MIN 6000TL-XH", protocol_revision="V1.24"),
        "stock_shine_write_observed", "medium", "logically_associated_not_byte_verified",
        raw_value=data["observed_protocol"], source_text=data["action"],
    ), claim(
        "min_shine_tou:readback:h3040-h3041", "min_shine_tou_write", "stock_shine_observation",
        subject("MODBUS", family, "holding", 3040, 3041), "readback_observation", data["readback"],
        {**prov, "json_pointer": "/readback"}, scope(family, "natural portal/stock-Shine event", model="MIN 6000TL-XH", protocol_revision="V1.24"),
        "readback_observed", "medium", "observed_without_raw_frame",
    ), claim(
        "min_shine_tou:relationship:h3040-h3041", "min_shine_tou_write", "stock_shine_observation",
        subject("LOGICAL", family, logical_object="xh_schedule_slot_2", field="register_pair"),
        "logical_relationship", {"registers": ["H3040", "H3041"], "role": "start/control and end"},
        {**prov, "json_pointer": "/registers"}, scope(family, "natural portal/stock-Shine event", model="MIN 6000TL-XH", protocol_revision="V1.24"),
        "stock_shine_request_observed", "high", "relationship_observed",
    )]
    return result


def implementation_claims(source_id: str, relative: str) -> list[dict[str, Any]]:
    data = load(relative)
    result: list[dict[str, Any]] = []

    def add(record: dict[str, Any], pointer: str, table: str | None, address: int | None, logical: str, field: str) -> None:
        family = ["unknown"]
        if table is None or address is None:
            sub = subject("IMPLEMENTATION", family, logical_object=logical, field=field)
        else:
            sub = subject("MODBUS", family, table, address)
        result.append(claim(
            f"{source_id}:{pointer.lstrip('/').replace('/', ':')}", source_id, "implementation_snapshot", sub,
            "implementation_register_mapping", copy.deepcopy(record),
            {"source_artifact": relative, "json_pointer": pointer},
            scope(family, "implementation snapshot does not establish canonical applicability"),
            "implementation_asserted", "medium", "observed_in_source_snapshot", source_text=str(record.get("name", record.get("label", record.get("text", "")))),
        ))

    if source_id == "ha_runtime":
        def walk(value: Any, path: str = "") -> None:
            if isinstance(value, dict):
                if isinstance(value.get("register"), int):
                    table = "holding" if "holding" in path else "input" if "input" in path else None
                    add(value, path, table, value["register"], path, value.get("name", "register"))
                for key, child in value.items(): walk(child, f"{path}/{key}")
            elif isinstance(value, list):
                for index, child in enumerate(value): walk(child, f"{path}/{index}")
        walk(data)
    elif source_id == "openinverter_gateway":
        for device, device_data in data.get("devices", {}).items():
            for table_key, records_key in (("input", "input_registers"), ("holding", "holding_registers")):
                for index, record in enumerate(device_data.get(records_key, [])):
                    add(record, f"/devices/{device}/{records_key}/{index}", table_key, record.get("address"), device, record.get("label", "register"))
    elif source_id == "grott":
        for layout, layout_data in data.get("layouts", {}).items():
            for index, record in enumerate(layout_data.get("fields", [])):
                add(record, f"/layouts/{layout}/fields/{index}", None, None, f"grott_layout:{layout}", record.get("field", "field"))
    elif source_id == "inverter_to_mqtt":
        for table_key, records in data.get("markdown_registers", {}).items():
            table = "holding" if "holding" in table_key else "input"
            for index, record in enumerate(records):
                add(record, f"/markdown_registers/{table_key}/{index}", table, record.get("address"), "markdown_register", str(record.get("address", "row")))
    return result


def fc20_claims() -> list[dict[str, Any]]:
    data = load("docs/reverse-engineering/GII-MIN-RE-1_evidence.json")
    return [claim(
        "shine_fc20:response:sample", "shine_fc20_research", "stock_shine_observation",
        subject("GROWATT_FC0x20", ["MIN 6000TL-XH"], logical_object="fc20_response", field="opaque_payload"),
        "raw_read_observation", {"function_code_hex": "0x20", "function_code_decimal": 32, "words_per_response": data["live_evidence"]["growatt_fc0x20_words_per_response"], "request_count": data["live_evidence"]["growatt_fc0x20_requests"], "semantics": "unresolved"},
        {"source_artifact": "docs/reverse-engineering/GII-MIN-RE-1_evidence.json", "json_pointer": "/live_evidence", "capture_sha256": data["live_evidence"]["growatt_fc0x20_capture_sha256"]},
        scope(["MIN 6000TL-XH"], "retained proprietary FC0x20 capture summary", model="MIN 6000TL-XH"),
        "stock_shine_request_observed", "medium", "opaque_namespace_retained",
    )]


def build() -> list[dict[str, Any]]:
    all_claims: list[dict[str, Any]] = []
    all_claims.extend(vendor_claims())
    all_claims.extend(live_claims())
    all_claims.extend(map_claims())
    all_claims.extend(semantic_review_claims())
    all_claims.extend(cloud_claims())
    all_claims.extend(shine_claims())
    for source_id, relative in (
        ("ha_runtime", "sources/runtime/ha-local-registers.snapshot.json"),
        ("openinverter_gateway", "sources/external/openinverter-gateway-registers.snapshot.json"),
        ("grott", "sources/external/grott-register-layouts.snapshot.json"),
        ("inverter_to_mqtt", "sources/external/inverter-to-mqtt-registers.snapshot.json"),
    ):
        adapter = implementation_claims(source_id, relative)
        dump({"schema_version": "1.0.0", "artifact": "growatt_generic_claim_adapter", "source_id": source_id, "claims": adapter}, f"sources/claims/implementation/{source_id}.json")
        all_claims.extend(adapter)
    all_claims.extend(fc20_claims())
    all_claims.sort(key=lambda item: item["claim_id"])
    dump({"schema_version": "1.0.0", "artifact": "growatt_generic_source_claims", "generated_by": "tools/build_generic_claims.py", "sources": "sources/claims/source-registry.json", "claims": all_claims}, "sources/claims/generic-claims.json")
    return all_claims


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", help="build and report the claim count")
    parser.parse_args()
    claims = build()
    print(f"generated {len(claims)} generic claims")


if __name__ == "__main__":
    main()
