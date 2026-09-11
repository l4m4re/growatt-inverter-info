# GII-2 — MIN / TL-XH semantic cleanup and evidence review

Status: `GII_MIN_TL_XH_MAPPING_CLEANUP_ACCEPTED_WITH_FOLLOW_UP`

Branch: `research/gii-2-min-tl-xh-semantic-cleanup-20260911`

Parent baseline: `401a56d344ac2f64babde3d22eff3cd588ffd3b4`

## Scope and safety

This review covers the canonical, project-independent MIN/TL-XH projection in
`spec/growatt-register-spec.json`, with the live-relevant model profile
`MIN 6000TL-XH`. It does not modify Home Assistant, the broker, polling,
transport, entity mappings, or write behavior. No write evidence is added.

The canonical consumer artifact remains `spec/growatt-register-spec.json`.
The consolidated audit and compatibility views remain generated intermediate
and migration products. The model-specific review input is
`sources/evidence/min-6000tl-xh-semantic-review.json`; the readable projection
is `GII-2_MIN_TL_XH_AUDIT_MATRIX.md`.

The retained live evidence is used as read-only corroboration. A successful
FC03/FC04 response establishes address reachability, not semantic proof. A
plausible decoded value is likewise supporting evidence only.

## Evidence basis

The review uses the existing retained corpus and its provenance graph:

- Growatt V1.24 structured vendor tables;
- the model-specific MIN 6000TL-XH map;
- retained read-only MIN block validation and live samples;
- Grott, OpenInverter gateway, inverter-to-MQTT and HA snapshots;
- the existing HA-5 regression evidence for signed BMS current.

The evidence levels remain distinct: vendor-documented, implementation
correlated, HA-correlated, read-observed, value-plausible, and semantically
verified. No field is promoted to write-accepted or behavior-verified.

## Physical identity and overlapping namespaces

Physical identity is unchanged and remains `(family, table, address)`. Holding
and input namespaces are never merged. In particular:

| Physical register | Canonical meaning |
|---|---|
| `MIN/TL-XH H3047` | Battery-first charge power rate |
| `MIN/TL-XH I3047..I3048` | Inverter runtime, logical high/low words |
| `MIN/TL-XH H3081` | UPS/EPS frequency selection |
| `MIN/TL-XH I3081..I3082` | PV4 lifetime energy, logical high/low words |

Logical multi-word fields are represented separately from their physical
words. Each physical word now has `length_words: 1`; the complete field and
word order are carried by `logical_fields`. This prevents a component word
from being mistaken for another two-word field.

## Control and schedule corrections

The MIN holding controls are now explicitly reviewed for `H3036–H3049` and
`H3079–H3082`.

- `H3036` and `H3037` are grid-first discharge-rate and stop-SOC controls.
- `H3038–H3045` are four packed grid-first schedule start/control and end
  words.
- `H3047`, `H3048` and `H3049` are battery-first charge rate, battery-first
  stop SOC and AC-charge enable.
- `H3050–H3059` are the corresponding packed battery-first schedule words.
- `H3079–H3082` are UPS/EPS enable, voltage, frequency and load-first stop
  SOC controls.

The packed schedule words have no W or kWh unit. The inherited unit values
were datatype collisions from unrelated fields. Schedule controls remain
read/write-capable in the map, but this review does not establish safe write
policy.

Raw zero at `H3082` remains an observation and is not used to replace the
vendor-documented load-first stop-SOC meaning.

## Warning and diagnostic separation

The former warning-code collisions are split into their physical meanings:

- `I110` is the high warning bitfield word and `I111` is the warning subcode;
  they are separate one-word records. The old two-word `/10` warning-code
  interpretation is rejected for this address pair.
- `I3110` is a vendor-defined inverter warning bitfield. It is one word and
  remains `UNCERTAIN` at bit-definition level.
- `I3111` is vendor `uwPresentFFTValue[CHANNEL_A]`, not a warning code.
- `I3167` and `I3168` are BDC fault and warning codes, distinct from inverter
  warning fields. Their numeric codebooks remain unresolved.

The current HA audit therefore reports a concrete `length_mismatch` at
`I3110`: the retained HA mapping still requests two words. This is an audit
finding for a future consumer review, not a runtime change in GII-2.

## BDC and BMS semantics

`I3164` is corrected from a BDC-presence interpretation to the vendor's
“whether to parse BDC data separately” flag. Retained raw zero does not prove
that a BDC is absent. `I3165`–`I3168` retain vendor-defined BDC mode/status and
fault/warning meanings; the codebooks are not invented.

The following distinctions are retained:

- `I3170` is storage-device battery current, signed `/10` by correlated
  implementation evidence, but its sign is not live-validated in the retained
  samples.
- `I3217` is BMS battery current, signed `/100`; retained `0xFEB6` decodes to
  `-3.30 A`. It is not merged with `I3170` merely because both represent
  battery current.
- `I3196` and `I3197` are BMS maximum/minimum SOC diagnostics, not the
  instantaneous SOC field. Retained zero values do not change that identity.
- `I3200` and `I3201` are GaugeFCC and GaugeRM. Their labels are retained as
  full-charge and remaining capacity, but numeric resolution and live
  behavior remain unresolved. Equality in one retained sample while SOC was
  below 100% is not sufficient to prove the scale or a usable capacity
  entity.
- `I3221` is a BMS cycle-count field and `I3222` a BMS SOH percentage; the
  observed zero/100 values are recorded as observations, not behavioral
  validation.

Temperature channels are deliberately neutral. Suffixes A/B/C do not prove
  physical pack numbers or separate BMS instances. Vendor `/0.1 °C` evidence
  is retained for the fields where documented; where the vendor omits scale,
  the scale remains unresolved. The retained `I3176/I3177` and repeated BMS
  temperature fields therefore do not become invented indexed packs.

## Scale and precision decisions

- `I3217` retains signed `/100 A` and the HA-5 regression note.
- `I3230` and `I3231` are vendor-proven `/1000 V`; retained raw values 3314
  and 3311 decode to 3.314 V and 3.311 V. A frontend display of `3 V` must
  not reduce canonical physical resolution.
- `I3224` remains `/100 V` at `STRONG`, below vendor-proven status, based on
  the adjacent documented limit and retained raw 18880 (`188.80 V`) plausibility.
- `I3191`, `I3194`, `I3195`, `I3200` and `I3201` remain explicitly uncertain
  where the retained corpus cannot establish the numeric scale or physical
  scope.

## Grid, import/export and load meaning

The canonical semantic layer keeps the physical meanings separate from source
wording such as “Power to user”, “Power to grid” and “Power user load”. The
existing logical fields distinguish:

- grid import power;
- grid export power;
- house/load power;
- grid import/export energy.

Vendor aliases and implementation names remain in provenance. The retained
live consistency relationships — PV component sums, battery V×I versus power,
PV/output/battery balance, and lifetime-energy component sums — are treated as
corroboration only, not as standalone semantic proof.

## Coverage and audit delta

The physical register count remains 4048: 1805 holding and 2243 input. The
material generated changes from the GII-1 baseline are:

| Metric | Before | After |
|---|---:|---:|
| semantic concepts | 962 | 976 |
| semantically reconciled records | 301 | 320 |
| logical multi-register fields | 552 | 550 |
| unknown-word-order logical fields | 197 | 195 |
| enum-bearing records | 148 | 162 |
| placeholder bitfield records | 43 | 45 |
| HA mapping occurrences checked | 274 | 274 |
| unique physical mappings checked | 206 | 206 |
| unique runtime issue findings | 27 | 22 |
| runtime issue occurrences | 34 | 23 |

The semantic-concept increase reflects explicit BDC, warning, diagnostic and
BMS max/min identities rather than mechanically preserving source names. The
logical-field reduction is the consequence of correcting false two-word
collisions. Runtime findings decrease because corrected physical semantics and
lengths remove false interpretations; the remaining 22 unique findings are
kept visible, including the new `I3110` length mismatch and the existing
signedness disagreements; corrected scale disagreements are retained in the
field-level review where appropriate rather than hidden in the audit.

## Reproducibility and follow-up

The full generated chain was run after the review changes, including graph,
consolidated audit, compatibility reference, canonical spec, validators and
the MIN/TL-XH matrix. The canonical validator reports 4048 records, 0
conflicted records, 60 retained live-read records and 0 write-verified
records. The deterministic generation test runs the spec generator twice and
compares all generated JSON/Markdown hashes.

Before any HA consumer migration, review the 22 remaining runtime findings,
especially the HA length/signedness/scale mismatches. Obtain additional
non-zero live BMS temperature/capacity samples and an independent BMS
codebook before exposing those fields as stable entities. Do not change an
existing entity source or identity solely from this report; instantaneous
sources require side-by-side validation and cumulative energy sources require
delta/rollover/statistics continuity checks.

The canonical mapping is therefore usable as an evidence-aware basis for
read-side HA reconciliation, with the unresolved items explicitly bounded and
without authorizing consumer or runtime changes.
