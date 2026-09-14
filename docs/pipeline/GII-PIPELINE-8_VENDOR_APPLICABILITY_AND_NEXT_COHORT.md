# GII-PIPELINE-8 — Vendor applicability and next authority cohort

Disposition: `GII_PIPELINE_VENDOR_APPLICABILITY_MIGRATION_ACCEPTED`

## Baseline

- PIPELINE-8 baseline `main`: `044917bd6fd699eddfc9cf76e38fe14f3ae23bab`; PIPELINE-8A repair base: `27c97d411e4ebfb5035bbc0b940af05504784393`; canonical SHA-256: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` before and after.
- Canonical records: 4048; canonical modified: `false`.
- Authority baseline: legacy 49515, declarative 161, legacy-exclusive 41 property cells.

## Evidence-accounting repair

The previous cohort builders embedded a single evidence label and complexity value in Python. That discarded the difference between a document range declaration, a row's semantic content and a row-local product qualifier. PIPELINE-8 now derives candidate evidence from retained generic claims and records claim IDs for each dimension.

## V1.24 applicability model

The page-3 instruction block is retained as 7 distinct declarations and 33 range claims. Source scopes are: `max_1500v_max_x_lv`, `min_tl_xh`, `mod_tl3_xh`, `storage_mix`, `storage_spa`, `storage_sph`, `tl3_max_mid_mac`. Function code/table and start/end are structured, so applicability queries do not depend on ranking code.

Document-level applicability is kept separate from row-local qualifiers. For H3071, the MIN/TL-XH holding range supports physical applicability while `SPH4-11K used` remains a separately cited, unresolved-scope qualifier. It is not used to deny the MIN range.

| Register | Retained source representation | Interpretation |
| --- | --- | --- |
| H3046 | `预留` | Mechanically normalized to `Reserved`; no stronger unsupported claim is added. |
| H3070 | `BatteryType`, R/W, 0 Lithium / 1 Lead-acid / 2 other | Vendor enum and access claims; MIN applicability inherited from FC03 3000–3124. |
| H3071 | `BatMdlSeria/ParalNum`, upper/lower byte layout, `SPH4-11K used` | Physical range, packed layout and row-local qualifier are independent claims. |
| H3095 | `BdcResetCmd`, R/W, four reset/clear meanings | Documented command semantics; live-write verification remains absent. |

## Fresh candidate ranking

| Rank | Candidate | Units | Legacy cells | Expected reduction | Evidence | Score | Complexity |
| ---: | --- | ---: | ---: | ---: | --- | ---: | --- |
| 1 | MIN/TL-XH holding H3070-H3071/H3095 battery-BDC configuration | 3 | 38 | 14 | high | 14 | low |
| 2 | Remaining MIN/TL-XH input 3000-3249 | 250 | 3175 | 1166 | medium | 759 | high |
| 3 | Remaining MIN/TL-XH holding 3000-3124 | 95 | 1195 | 367 | medium | 279 | high |
| 4 | MIN/TL-XH holding 3125-3249 | 125 | 1504 | 48 | low | 36 | high |
| 5 | MIN/TL-XH input 3250-3374 | 125 | 1314 | 94 | low | 23 | high |

### Selected evidence dimensions

| Register | Applicability | Semantic row | Enum/packed | Access | Qualifier | Write docs | Live write |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H3070 | SUPPORTED_UNCONDITIONAL | supported | supported | supported | not_present | documented | absent |
| H3071 | SUPPORTED_UNCONDITIONAL | supported | supported | supported | present | documented | absent |
| H3095 | SUPPORTED_UNCONDITIONAL | supported | supported | supported | not_present | documented | absent |

The selected cohort is the top ranked bounded result produced by the claim-driven generator. It contains three coherent MIN/TL-XH BDC/control words. H3071's qualifier lowers/annotates the evidence rather than collapsing the entire source situation to `medium`.

## PIPELINE-8A applicability-scope repair

The original model used the canonical family `tl3_max_mid_mac` as the only scope for both the TL3-X/MAX/MID/MAC declaration and the separate MAX 1500V/MAX-X LV declaration. PIPELINE-8A preserves that broad canonical grouping but adds the source scopes `tl3_max_mid_mac` and `max_1500v_max_x_lv`; consequently FC04 input 900 is supported for the latter and is not claimed for the former.

MIN ranges H3125-H3249 (FC03) and H3250-H3374 (FC04) retain their TL-XH US and TL-XH qualifiers. Without matching model context, queries return `SUPPORTED_QUALIFIED`; with an explicit matching model variant the qualifier is satisfied but remains conditional. H3070 and H3095 remain `SUPPORTED_UNCONDITIONAL` through the unqualified H3000-H3124 declaration. Applicability results also distinguish `NOT_SUPPORTED_BY_DECLARATION` from `UNRESOLVED` when source scope is absent or insufficient.

All seven declaration IDs and all 33 ranges remain present. H3071's `SPH4-11K used` note remains a separate row-local qualifier. H3046 retains raw `预留` and normalized `Reserved`; H3095 remains documented write semantics without live-write verification.

Canonical SHA remains unchanged and `canonical_modified=false`. Authority movement is unchanged unless the corrected claim-driven scoring changes it; the values below are regenerated rather than forced.

The archived `tools/legacy/validate_min_6000tl_xh_map.py` is not an acceptance gate and requires the absent historical fixture `tools/legacy/min_6000tl_xh_register_map.json`. Current register-spec, resolved-reference, focused invariant and pipeline validators cover the maintained outputs; the legacy fixture was not recreated.

## Selected cohort and authority movement

- Scope: MIN/TL-XH FC03 holding H3070, H3071 and H3095; physical parity is 3/3 (100%) for the selected registers. H3046 is retained and tested as source context, not silently folded into the selected cohort.
- Property-level parity: `{'PARITY_MATCH': 1, 'REPRESENTATION_ONLY': 2}`.
- H3095's documented write operation meaning is not a permission or live safety verification claim.

| Metric | Before | After | Delta |
| --- | ---: | ---: | ---: |
| Repository legacy-authoritative cells | 49515 | 49501 | -14 |
| Repository declarative-authoritative cells | 161 | 180 | +19 |
| Repository legacy-exclusive cells | 41 | 41 | +0 |
| Selected-cohort legacy-authoritative cells | 38 | 24 | -14 |

## Safety and deferred work

No inverter write, reset command, Home Assistant/runtime change or canonical modification was made. H3085 remains the PIPELINE-7 supported canonical-correction candidate and is not repaired here. No global canonical cutover and no HA-GII-5 work was started.

## Reproducibility

- Source profile: `sources/vendor/profiles/vendor_growatt_v124_2020.json`.
- Vendor extraction: `tools/extract_vendor_pdf.py` with Poppler `pdftotext -layout -enc UTF-8`; original PDF SHA-256 was checked as `fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320`.
- Generic projection: `python3 tools/build_generic_claims.py`; ranking/cohort: `python3 tools/build_pipeline8_cohort.py`.
