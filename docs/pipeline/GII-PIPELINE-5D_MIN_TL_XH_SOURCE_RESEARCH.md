# GII-PIPELINE-5D — MIN/TL-XH FC04 source-research closure

## Disposition

`GII_PIPELINE_FC04_SOURCE_CLOSURE_ACCEPTED_WITH_FOLLOW_UP`

Starting SHA: `4eb8b10364751e4d29243481501c4c72b6def69a`  
Branch: `research/gii-pipeline-5d-min-tlxh-source-closure-20260913`  
Implementation commit: `4c820ce`  
Canonical modified: `false`  
Active experiments: none

PIPELINE-5D reviewed exactly the 17 `SOURCE_RESEARCH_CANDIDATE` records from
PIPELINE-5C. It did not reopen the 51 insufficient-evidence records, inject
Cloud/Shine values, or alter the inverter, broker, Home Assistant, or canonical
register specification.

## Deliverables

The review is represented by:

- `sources/evidence/gii-pipeline-5d-fc04-source-research.json` — structured,
  property-level source findings and absence-of-evidence records;
- `sources/claims/gii-pipeline-5d-fc04.json` — generic claims generated from
  those findings;
- `reconciliation/min_tl_xh_fc04_source_research_20260913.json` — one
  claim-linked decision for every reviewed property;
- `docs/pipeline/data/GII-PIPELINE-5D_FC04_SOURCE_RESEARCH.json` — deterministic
  inventory and metrics;
- `tools/build_fc04_source_research.py` and
  `tools/validate_fc04_source_research.py` — offline rebuild and validation.

## Sources and method

The original V1.24 PDF was the primary source. Its SHA-256 is:

```text
fac88d609d74ff6b3c9c31ed65370d166d1fb17461e91b4b4855018fe232a320
```

Pages 74–82 were inspected using native `pdftotext -layout` extraction and
rendered page images. The retained structured V1.24 table transcription was
checked against the visible rows. The `T06NNNNXMOD` Grott snapshot was used as
implementation/layout corroboration. Curated input mappings, canonical output,
retained live Modbus evidence and retained Cloud evidence were searched for
candidate-specific claims; the latter three supplied no independent semantic
mapping for these addresses. The canonical output was used only as a frozen
parity target, never as evidence.

For every candidate the machine-readable evidence records all sources checked,
the exact vendor row/page or implementation field, the supported properties,
and the properties that remain unresolved. Holding/input identity was kept
separate: for example, holding 3085 is `ComAddress`, while input 3085 is
documented as `Reserved`.

## Candidate results

Fourteen candidates are fully resolved at the protocol-role scope: the vendor
explicitly labels the input word `Reserved`, and Grott independently carries a
single-word `reservedNNNN` field. Their numeric signedness/scale/unit are
not applicable rather than silently assumed.

| Input register | V1.24 source row | Grott corroboration | Result |
|---:|---|---|---|
| 3085 | p.74, `Reserved` | `reserved3085`, one word | reserved/unsupported; do not confuse with holding 3085 `ComAddress` |
| 3116 | p.76, `Reserved` | `reserved3116`, one word | reserved/unsupported |
| 3117 | p.76, `Reserved` | `reserved3117`, one word | reserved/unsupported |
| 3120 | p.76, `Reserved` | `reserved3120`, one word | reserved/unsupported |
| 3143 | p.77, `Reserved` | `reserved3143`, one word | reserved/unsupported; 3144 is a separate Priority field |
| 3163 | p.77, `Reserved` | `reserved3163`, one word | reserved/unsupported; 3164 is a separate NewBdcFlag field |
| 3186 | p.79, `Reserved` | `reserved3186`, one word | reserved/unsupported; 3187 is a separate BDC1_Flag field |
| 3206 | p.80, `Reserved` | `reserved3206`, one word | reserved/unsupported |
| 3207 | p.80, `Reserved` | `reserved3207`, one word | reserved/unsupported |
| 3208 | p.80, `Reserved` | `reserved3208`, one word | reserved/unsupported |
| 3209 | p.80, `Reserved` | `reserved3209`, one word | reserved/unsupported |
| 3227 | p.82, `Reserved` | `reserved3227`, one word | reserved/unsupported |
| 3228 | p.82, `Reserved` | `reserved3228`, one word | reserved/unsupported |
| 3229 | p.82, `Reserved` | `reserved3229`, one word | reserved/unsupported |

Three candidates are partially resolved because the source establishes useful
layout/encoding facts but does not establish every semantic property:

| Input register | Supported | Still unresolved | Evidence/contradiction |
|---:|---|---|---|
| 3096 | one word; `Temp4` is marked `Reserved`; 0.1 °C notation; V1.24 applicability | signedness | The vendor row visibly says `Temp4 / Reserved / 0.1°C`; this is not proof of an active temperature quantity. Grott has `temp4`, divide 10. |
| 3109 | one word; vendor datatype is `bitfield`; V1.24 applicability | semantic quantity, bit meanings/enums | The vendor name/description cells are blank. Grott calls it `reserved3109`, which is implementation corroboration, not a vendor semantic definition. |
| 3233 | one word between documented 3232 and 3234 rows; V1.24 applicability | semantic quantity, scale, unit, signedness | The vendor row is visibly blank. Grott calls it `reserved3233`; that label is not promoted to vendor-proven meaning. |

No candidate was promoted to an active HA entity, a write target, or a guessed
numeric decoder. In particular, “reserved” is a protocol-role conclusion and
does not mean that a device can never return a non-zero diagnostic value there.

## Property-level progress

The 17 candidates produced these source-supported declarative property claims:

| Property | Newly supported cells |
|---|---:|
| physical identity/layout | 17 |
| word length | 17 |
| model applicability | 17 |
| physical/protocol role | 15 |
| scale | 1 (I3096) |
| unit | 1 (I3096) |
| packed-field container | 1 (I3109) |

Signedness, actual bit meanings, and the semantic quantity of I3109/I3233 remain
unresolved. `NOT_APPLICABLE` is used only where the register is explicitly a
reserved protocol slot; it is not used to hide missing evidence.

The four 5C `DERIVED_OR_AGGREGATE` candidates (I3041, I3042, I3045 and I3046)
were reviewed only as a cheap documentary follow-up. No retained source
explicitly proves a sum, average, difference, maximum/minimum, or other formula,
so all four remain `DERIVED_OR_AGGREGATE` candidates. No formula was inferred.

## Authority and parity

The existing PIPELINE-5A authority tool was rerun against the frozen canonical
output. For the 17 candidate records its before/after numbers are unchanged:

| Metric | Before 5D | After 5D |
|---|---:|---:|
| cohort declarative-authoritative property cells | 0 | 0 |
| cohort legacy-authoritative dependency cells | 52 | 52 |
| repository declarative-authoritative property cells | 242 | 242 |
| repository legacy-authoritative property cells | 49,622 | 49,622 |
| repository canonical property cells | 49,864 | 49,864 |

This unchanged 5A result is intentional: 5D adds property-level declarative
evidence and reconciliation, but does not cut that evidence into the canonical
generator. The 5D review itself adds 69 source-supported property claims (17
physical identities, 17 lengths, 17 applicability claims, 15 protocol roles,
one scale, one unit and one packed-field container). They are ready for a later
authority migration after review.

Canonical parity is therefore `true`; the canonical SHA remains the PIPELINE-5C
parity SHA. There is no canonical correction candidate in this task.

## Validation

The following offline commands pass:

```text
python3 tools/build_fc04_source_research.py --check
python3 tools/validate_fc04_source_research.py
python3 tools/validate_fc04_migration.py
python3 tools/validate_resolved_register_reference.py
python3 tools/validate_register_spec.py
python3 tools/validate_authority_coverage.py
python3 -m pytest -q
```

The complete test suite requires no Cloud token, live hardware or private
network. The source-research validator checks exact 17-record coverage,
property-claim/reconciliation linkage, deterministic output, canonical freeze,
absence of secrets, and the no-experiment safety boundary.

## Deferred follow-up

The next useful step is not more semantic archaeology in this cohort. The
remaining open facts are the bit meanings of I3109, the actual role of I3233,
and signedness for the reserved I3096 slot; none has enough evidence here for a
safe decoder. PIPELINE-5C's 51 insufficient-evidence and 54 counter/history
targets remain out of scope. The MIN/TL-XH FC04 3000–3249 cohort should now be
treated as frozen at this evidence-supported state while the authority program
selects its next high-value migration cohort.
