#!/usr/bin/env python3
"""Render the generated MIN/TL-XH evidence-review matrix."""

# ruff: noqa: T201

import json
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
SPEC_PATH = REPO / "spec" / "growatt-register-spec.json"
REVIEW_PATH = REPO / "sources" / "evidence" / "min-6000tl-xh-semantic-review.json"
OUTPUT_PATH = REPO / "docs" / "reverse-engineering" / "GII-2_MIN_TL_XH_AUDIT_MATRIX.md"

AUDIT_RANGES = {
    "holding": ((3036, 3049), (3050, 3059), (3079, 3082)),
    "input": ((95, 99), (110, 112), (3041, 3047), (3095, 3099), (3110, 3111), (3164, 3181), (3191, 3232)),
}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def selected(table: str, address: int) -> bool:
    return any(start <= address <= end for start, end in AUDIT_RANGES[table])


def cell(value: Any) -> str:
    """Keep source text inside one Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ")


def source_claims(record: dict[str, Any]) -> str:
    vendor = ", ".join(record["vendor"]["variable_names"]) or "—"
    implementations = ", ".join(
        source
        for source in ("grott", "openinverter_gateway", "inverter_to_mqtt", "home_assistant")
        if source in record.get("source_aliases", {})
    )
    return cell(f"vendor: {vendor}; correlated: {implementations or '—'}")


def live_evidence(record: dict[str, Any], review: dict[str, Any] | None) -> str:
    if review and review.get("live_observation"):
        return cell(review["live_observation"])
    if record.get("validation_evidence"):
        return cell("; ".join(item["source"] for item in record["validation_evidence"]))
    return "not retained for this physical field"


def render() -> str:
    spec = load(SPEC_PATH)
    review_rows = {
        (item["table"], int(item["address"])): item
        for item in load(REVIEW_PATH)["records"]
    }
    records = [
        record
        for record in spec["registers"]
        if record["family"] == "min_tl_xh" and selected(record["table"], record["address"])
    ]
    lines = [
        "# GII-2 MIN/TL-XH evidence-review matrix",
        "",
        "Generated from `spec/growatt-register-spec.json` and the model-specific review overlay. The matrix preserves physical identity as family + table + address; it is not a second semantic source.",
        "",
        "| Physical field | Length | Current canonical semantic | Measurement point | Datatype / signed / scale | Unit / access | Vendor and correlated claims | HA/live evidence | Resolution | GII-2 disposition |",
        "|---|---:|---|---|---|---|---|---|---|---|",
    ]
    for record in records:
        review = review_rows.get((record["table"], record["address"]))
        normalized = record["normalized"]
        identity = record["semantic_identity"]
        disposition = review.get("disposition", "UNRESOLVED") if review else "UNRESOLVED"
        lines.append(
            "| {physical} | {length} | `{quantity}` {name} | {point} | `{raw}` / {signed} / {scale} | {unit} / {access} | {claims} | {live} | `{status}` / {confidence} | `{disposition}` |".format(
                physical=cell(record["physical_id"]),
                length=record["length_words"],
                quantity=identity["quantity"] or "unassigned",
                name=cell(normalized["name"] or "—"),
                point=cell(identity["measurement_point"]),
                raw=cell(normalized["raw_type"] or "—"),
                signed=normalized["signed"],
                scale=normalized["scale"] if normalized["scale"] is not None else "—",
                unit=cell(normalized["unit"] or "—"),
                access=normalized["access"],
                claims=source_claims(record),
                live=live_evidence(record, review),
                status=record["resolution"]["status"],
                confidence=record["resolution"]["confidence"],
                disposition=disposition,
            )
        )
    return "\n".join(lines) + "\n"


def main() -> None:
    OUTPUT_PATH.write_text(render(), encoding="utf-8")
    print(f"wrote {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
