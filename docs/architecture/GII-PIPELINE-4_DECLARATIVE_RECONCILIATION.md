# GII-PIPELINE-4 — Declarative reconciliation

Status: implemented as a shadow pipeline; canonical generator cutover is deferred to PIPELINE-5.

Starting point: `1b929fa4b46fb7f7bb8b7bd0beeebc7eb3074fe3` (PIPELINE-3)

## Architecture

PIPELINE-4 adds the missing review layer:

```text
raw/vendor/runtime sources
          ↓
generic claims
          ↓
declarative reconciliation decisions
          ↓
shadow resolved assertions
          ↓                 ↘ comparison only
[PIPELINE-5] canonical generator   current canonical spec
```

`sources/claims/generic-claims.json` remains the provenance graph. A decision
in `reconciliation/min_tl_xh.json` selects a property explicitly and cites
exact claim IDs. It also records rejected claims, scope, confidence, rationale,
review status, and unresolved questions. No source precedence rule is applied.

`tools/build_reconciliation.py` deterministically assembles these decisions
into `reconciliation/resolved-assertions.json`. The result is marked
`shadow_only_not_canonical`; it cannot overwrite or feed the canonical spec.
`tools/compare_reconciliation_to_canonical.py` reads the canonical spec only
as a comparison target.

## Scope-aware conflicts

`reconciliation/scope-mappings.json` is the explicit vocabulary bridge from
vendor family labels to reconciliation scopes. It distinguishes equivalent,
subset, overlapping, disjoint, and unknown applicability without substring
matching. `tools/report_claim_conflicts.py` now includes scope in conflict
identity. The original 201 groups remain 201 groups, but the post-repair
classification is:

```text
hard conflicts:             46
potential scope conflicts: 155
value conflicts:             7
access conflicts:            1
wording differences:        38
```

An unknown scope is never silently resolved. Disjoint family claims do not
become hard conflicts, and holding/input identity stays separate (for example
H3047 and I3047).

## Representative MIN/TL-XH reconciliation

The 29 declarative decisions cover the reviewed MIN/TL-XH status, BDC/BMS,
EMS, and FC20 subjects. They preserve the physical identity `(family, table,
address)` while also exposing semantic keys and logical relationships.

The XH schedule is represented as nine generic slots:

| slots | start/control | end |
| --- | --- | --- |
| 1 | H3038 | H3039 |
| 2 | H3040 | H3041 |
| 3 | H3042 | H3043 |
| 4 | H3044 | H3045 |
| 5–9 | H3050, H3052, H3054, H3056, H3058 | following register |

H3046 is explicitly reserved. All slots reference reusable V1.24 start and
end templates. Start words resolve minute bits 0–7, hour bits 8–12,
priority bits 13–14, and enable bit 15. End words resolve minute/hour and
reserve bits 13–15. Priority value 3 is reserved/unknown. Parser artefacts
such as 6, 7, 12, and 15 are rejected as enum values. The retained H3040/H3041
Shine event supports a logical write/readback relationship, but not exact-wire
write verification.

Access is decided independently of semantic naming. Incomplete vendor access
cells are not upgraded merely because a record is a control. H3047–H3049,
H3036, and H3037 retain their semantic decisions without inventing write
evidence.

The input decisions retain the reviewed findings: I3000 and I3166 packed
fields, the complete I3165 codebook including 22/23/24, documented I3211 bits
only, I3212 enum, non-negative I3101 and I3170, signed directional I3217, and
the physical I3111 PresentFFT name. Cloud `sys_fault_word3`/`word4` findings
are relationship edges; I3111's word-4 relationship remains provisional.
FC0x20 remains a separate unresolved proprietary profile (function `0x20`,
observed request/response shape only).

## Hidden-authority audit and migration boundary

`reconciliation/python-semantic-inventory.json` inventories the register and
domain knowledge still embedded in Python. It classifies presentation,
compatibility, generic transformation, and semantic rules, and identifies the
29 decisions that now represent the PIPELINE-4 cut. The legacy generator still
contains duplicated semantic overrides because changing them would be a
canonical cutover. They are migration bridges, not new evidence.

No new register-specific semantic literals were added to generator Python.
PIPELINE-5 may remove the inventoried `SEMANTIC_RENAMES`, packed/enum/bitfield
overrides, direct-name fallbacks, semantic rules, role/capability/transport
tables, and related legacy bridges only after candidate-to-canonical parity is
reviewed.

## Validation and next boundary

`tools/validate_reconciliation.py` checks decision IDs, target identity,
claim references, scope, packed ranges/overlaps, logical template references,
and shadow-only status. The focused reconciliation tests cover scope handling,
TOU slots, packed fields, reserved bits, status codebooks, FC20 separation,
canonical non-use, and deterministic regeneration.

The canonical `spec/growatt-register-spec.json` is intentionally unchanged.
Compatibility output and Home Assistant, broker, inverter, and live
configuration are outside this task. The next task is PIPELINE-5: a controlled
cutover of reconciled assertions into the canonical generator with explicit
parity and review gates.
