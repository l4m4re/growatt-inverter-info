# GII-PIPELINE-5: canonical generator cutover

Status: **not accepted; cutover deliberately stopped at the starting gate**.

Final disposition:

`GII_PIPELINE_CANONICAL_CUTOVER_NOT_ACCEPTED`

## Scope

This task tested whether the PIPELINE-4 declarative reconciliation can replace
the current canonical generator without losing accepted canonical output. No
register meaning, Home Assistant consumer, broker, inverter or production
configuration was changed.

## Starting state

| Item | Value |
| --- | --- |
| Branch | `feature/gii-pipeline-4-declarative-reconciliation-20260913` |
| Starting HEAD | `8ceb8cd94f50235af4fc10b44ad8cbb355919518` |
| PIPELINE-4A disposition | `GII_PIPELINE_RECONCILIATION_REPAIR_ACCEPTED` |
| Canonical artifact | `spec/growatt-register-spec.json` |
| Canonical SHA-256 | `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` |
| Canonical Git blob | `0a25325bcebf0477ee887051b26c562f3d53daf0` |
| Working tree | clean |

The task branch was created from this exact starting point:

`feature/gii-pipeline-5-canonical-generator-cutover-20260913`

The starting commit is an ancestor of the task branch and the canonical
artifact was retained unchanged in that Git object. This is the exact
pre-cutover comparison artifact; no second editable copy was introduced.

## Starting-gate validation

The following commands completed successfully before any cutover change:

```text
python3 tools/build_reconciliation.py
generated 29 decisions: {'provisionally_resolved': 1, 'reserved': 1, 'resolved': 26, 'unresolved': 1}

python3 tools/validate_reconciliation.py
valid: reconciliation decisions and shadow candidate

python3 tools/report_claim_conflicts.py
conflicts=201 hard=46 potential_scope=155 categories={'access_conflict': 1, 'potential_scope_conflict': 155, 'value_conflict': 7, 'wording_difference': 38}

python3 tools/compare_reconciliation_to_canonical.py
compared 18 physical decisions; canonical_modified=false

python3 tools/validate_claims.py
valid: 4178 claims

python3 tools/validate_register_spec.py
ok: true, records: 4048, unique_semantics: 978, runtime_unique_findings: 22, human_docs: 11

python3 tools/validate_resolved_register_reference.py
ok: true, records: 4048, write_verified: 0

python3 -m pytest -q
48 passed
```

The regenerated shadow and comparison outputs were deterministic and the
working tree remained clean. The canonical SHA-256 stayed unchanged.

## Blocking parity result

The PIPELINE-4 candidate is a reviewed shadow layer, not yet a complete
canonical register model:

| Representation | Physical records/targets |
| --- | ---: |
| Declarative reconciliation decisions with physical MODBUS targets | 18 |
| Current canonical specification | 4,048 |
| Physical coverage of the candidate | 18 / 4,048 (0.44%) |

The current `tools/build_register_spec.py` still reads
`knowledge/compatibility/growatt-register-reference.json`. It also still
contains the migration bridges recorded in
`reconciliation/python-semantic-inventory.json`, including semantic renames,
packed-field and enum overrides, normalization overrides, and fallback
semantic rules. Those bridges supply accepted meaning for thousands of
records that have no declarative reconciliation decision yet.

Consequently, a generator changed now would have to choose one of two invalid
outcomes:

* omit most of the 4,048 canonical records and their family/protocol/logical
  metadata; or
* continue using the compatibility/legacy Python semantic path as an
  additional authority.

Neither outcome satisfies the PIPELINE-5 invariant that the declarative model
and validated reconciliation/provenance pipeline become the single editable
authority. The existing 18-target comparison is therefore not a full
canonical equivalence proof; it is only the PIPELINE-4 representative parity
check.

## What was not cut over

No generated canonical file was rewritten, no generated-file protection or CI
regeneration check was added, and no downstream consumer path was changed.
This is intentional: those changes would falsely advertise a successful
cutover while the full declarative model is incomplete.

The accepted PIPELINE-4A semantics remain protected in the unchanged
canonical artifact, including:

* I3000 separate mode/status byte decoding, including `0x0001` → mode `0`
  (`Waiting module`) and status `1` (`Normal`);
* H3036/H3037 percentage interpretation with H3036 value `255` unresolved;
* H3082 ratio-to-percentage provenance.

## Required next work before a retry

The next cutover attempt must first migrate the remaining generator authority
into claim-supported declarative data, at least for:

* the full physical register baseline and family applicability;
* remaining semantic keys and canonical names;
* enum, bitfield and packed-field definitions;
* normalization, unit and scale decisions;
* logical fields and relationship roles;
* protocol/capability/read-plan metadata;
* claim/evidence links for each promoted property.

Then a temporary full-output parity gate can compare the generated result with
the retained pre-cutover artifact. Only after that comparison is exact (or
structurally equivalent with every difference explained) should the canonical
authority be switched and generated-output protection be enabled.

## Disposition

`GII_PIPELINE_CANONICAL_CUTOVER_NOT_ACCEPTED`

No further pipeline stage was started.
