# GII-CONSOLIDATION-1 — Vendor-native V1.24 register blocks

## Goal

This is an offline, block-oriented candidate for the future Growatt register specification. It keeps the V1.24 vendor structure primary, uses existing repository evidence for enrichment and challenge, and leaves the canonical specification frozen.

## Starting repository state

- Starting merged-main: `fe63d223d83dbadd4be6448802d42b5f9302c64f` (PIPELINE-11 merge).
- V1.24 PDF SHA-256: `fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320`; 85 pages; embedded `pdftotext -layout` extraction.
- Frozen canonical spec SHA-256: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405`.
- No live, cloud, Home Assistant, broker or inverter activity was performed.

### Reproducible extraction command

```text
python3 tools/extract_vendor_pdf.py --pdf ../Homeassistant-Growatt-Local-Modbus/doc/Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf --expected-sha256 fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320 --document-id vendor_growatt_v124_2020 --profile sources/vendor/profiles/vendor_growatt_v124_2020.json --review sources/claims/vendor/reviews/vendor_growatt_v124_2020.json --output sources/claims/vendor/vendor_growatt_v124_2020.json
python3 tools/build_gii_consolidation.py --pdf ../Homeassistant-Growatt-Local-Modbus/doc/Growatt-Inverter-Modbus-RTU-Protocol_II-V1_24-English.pdf
```

The extraction environment used `pdftotext`/`pdfinfo` 25.03.0 and Python 3.14.5. The original PDF is not copied into this repository; only its filename, hash and derived claims are published.

## Growatt V1.24 source-native block structure

The source-native inventory is derived from the original PDF’s layout-preserving claim extraction. Manual visual-review claims are retained as evidence references and are not counted as a second occurrence.

| Source-native block | FC/table | Range | Vendor heading(s) | Families/scopes | Rows | Role status |
|---|---:|---:|---|---|---:|---|
| `v124-holding-p009-first_group-block-01` | FC3 / holding | 0–124 | First group | max_1500v_max_x_lv, min_tl_xh, mod_tl3_xh, storage_mix, storage_spa, storage_sph, tl3_max_mid_mac | 125 | `unresolved_ordinal_label` |
| `v124-holding-p016-second_group-block-02` | FC3 / holding | 125–660 | Second group | max_1500v_max_x_lv, tl3_max_mid_mac | 182 | `unresolved_ordinal_label` |
| `v124-holding-p027-six_group_for_storage_power-block-03` | FC3 / holding | 1000–1249 | Six group for Storage Power | storage_mix, storage_spa, storage_sph | 118 | `vendor_supported` |
| `v124-holding-p035-use_for_tl_x_and_tl_xh-block-04` | FC3 / holding | 3000–3124 | Use for TL-X and TL-XH | min_tl_xh, mod_tl3_xh | 109 | `vendor_supported` |
| `v124-holding-p042-us_machine_type_time_set-block-05` | FC3 / holding | 3125–3222 | US Machine type Time Set | min_tl_xh | 64 | `vendor_supported` |
| `v124-holding-p047-bdc_information_support_up_to_10_parallel_bdc-block-06` | FC3 / holding | 5000–5079 | BDC information (support up to 10 parallel BDC) | — | 4 | `vendor_supported` |
| `v124-input-p047-first_group-block-07` | FC4 / input | 0–124 | First group | max_1500v_max_x_lv, storage_mix, storage_sph, tl3_max_mid_mac | 122 | `unresolved_ordinal_label` |
| `v124-input-p051-second_group-block-08` | FC4 / input | 125–249 | Second group | max_1500v_max_x_lv, tl3_max_mid_mac | 125 | `unresolved_ordinal_label` |
| `v124-input-p056-the_eighth_group_for_pv9_pv16_information-block-09` | FC4 / input | 875–999 | The eighth group for PV9-PV16 information | max_1500v_max_x_lv | 120 | `unresolved` |
| `v124-input-p059-ninth_group_for_storage_power-block-10` | FC4 / input | 1000–1066 | Ninth group for Storage power | storage_mix, storage_spa, storage_sph | 67 | `vendor_supported` |
| `v124-input-p062-bms_infomation-block-11` | FC4 / input | 1082–1124 | BMS Infomation | storage_mix, storage_spa, storage_sph | 43 | `vendor_supported` |
| `v124-input-p062-ups_information_offline-block-12` | FC4 / input | 1067–1081 | Ups information (offline) | storage_mix, storage_spa, storage_sph | 15 | `vendor_supported` |
| `v124-input-p064-ninth_group_reserved_for_storage_power-block-13` | FC4 / input | 1125–2124 | Ninth group reserved for storage power | storage_spa, storage_sph | 116 | `vendor_supported` |
| `v124-input-p070-use_for_tl_x_and_tl_xh-block-14` | FC4 / input | 3000–3280 | Use for TL-X and TL-XH | min_tl_xh, mod_tl3_xh | 274 | `vendor_supported` |
| `v124-input-p084-bdc_and_bms_information_support_up_to_10_parallel_bdcs-block-15` | FC4 / input | 4000–5079 | BDC and BMS information (support up to 10 PARALLEL BDCS) | — | 9 | `vendor_supported` |

Functional headings: **10**; vague/ordinal headings: **5**. The latter remain `unresolved_ordinal_label` and are not promoted to vendor-authored semantics.

## Consolidated block model

The candidate contains **15** consolidated blocks. Each currently maps one V1.24 source-native structural block; shared family use is represented through applicability paths rather than copied family register tables. No cross-source block merge was forced because the available source-native occurrences were not independently proven identical beyond their preserved structure.

## Family/model applicability

All seven V1.24 instruction-block declarations are retained, including MIN/TL-XH, TL3/MAX scopes, MOD TL3-XH and MIX/SPA/SPH storage scopes. The complete raw declaration text is in `spec/growatt-register-spec-v2-candidate.json`; block paths retain declaration ID, function/table, range and qualifiers.

## Register consolidation results

The matrix contains **1493** vendor row definitions. Vendor raw fields and canonical comparison fields are kept separate; selected descriptions and decode metadata are enrichment, not new evidence.

| Register status | Count |
|---|---:|
| Confirmed | 0 |
| Enriched | 980 |
| Qualified | 270 |
| Conflict | 23 |
| Unresolved | 177 |
| Reserved | 43 |

### H107 access normalization

H107 is represented with vendor raw access `W` and normalized access derived from the exact token only. The previous layout-leak form `r    W` is not accepted as a raw access value by the extractor. The regression is generic: access extraction never searches or copies arbitrary neighboring row text.

## Description enrichment and decode metadata

Existing canonical, runtime, external implementation and accepted evidence records are included as compact side-by-side comparison entries in the register matrix. A missing decode property remains visible as `NEEDS_METADATA`; normalization such as `1S` to `s` is not performed as evidence creation in this candidate.

## Write metadata and HA-readiness

Vendor access and write safety remain separate. A documented writable row is not marked live-write-verified. The current candidate reports:

- `READY_READ`: 1149
- `READY_WRITE_DOCUMENTED`: 124
- `READY_WRITE_VERIFIED`: 0
- `NEEDS_METADATA`: 177
- `RESERVED_OR_UNSUPPORTED`: 43

## MIN/TL-XH generated projection

The projection is generated from consolidated blocks plus V1.24 applicability paths. It is not hand-maintained and retains qualifiers such as the TL-XH/TL-XH US distinctions.

- Candidate physical keys: **518**
- Current canonical MIN/TL-XH keys: **895**
- Matching keys: **518**
- New from vendor: **0**
- Missing in candidate: **377**

Comparison category summary:

- `MATCH`: 518
- `ENRICHED`: 217
- `CONFLICT`: 6
- `MISSING_IN_CANDIDATE`: 377
- `NEW_FROM_VENDOR`: 0
- `REPRESENTATION_ONLY`: 0
- `REPRESENTATION_ONLY` definition: No separate representation-only category exists in this candidate; the value is zero until a reviewed non-physical representation is modeled.

## Conflicts

There are **23** explicit comparison conflicts/review candidates. They are listed in `docs/consolidation/data/GII-CONSOLIDATION-1_CONFLICTS.json`; H3085 remains explicitly flagged as a semantic review candidate and is not silently treated as an external-meter setting.

## Unresolved evidence gaps

There are **177** unresolved rows, including ambiguous/unparsed source addresses and rows without a current canonical match. They are listed in `docs/consolidation/data/GII-CONSOLIDATION-1_UNRESOLVED.json` rather than being invented or discarded.

## Safety / canonical freeze

`spec/growatt-register-spec.json` was not modified. The candidate is `spec/growatt-register-spec-v2-candidate.json`; no Home Assistant consumer changes are included. Generated artifacts are deterministic and can be regenerated with `tools/build_gii_consolidation.py` using the original local PDF.

## Generated artifacts

- `sources/vendor/growatt-v1.24-blocks.json`
- `docs/consolidation/data/GII-CONSOLIDATION-1_BLOCK_INVENTORY.json`
- `docs/consolidation/data/GII-CONSOLIDATION-1_REGISTER_MATRIX.json`
- `docs/consolidation/data/GII-CONSOLIDATION-1_CONFLICTS.json`
- `docs/consolidation/data/GII-CONSOLIDATION-1_UNRESOLVED.json`
- `docs/consolidation/data/GII-CONSOLIDATION-1_MIN_TL_XH_PROJECTION.json`
- `spec/growatt-register-spec-v2-candidate.json`
