# GII PIPELINE-3: generic claim-level provenance

Status: implemented on `feature/gii-pipeline-3-generic-claims-20260913`.

PIPELINE-3 adds an unresolved, source-independent evidence layer beside the
existing vendor and canonical pipelines. A claim is an assertion made or
observed by one source; it is not canonical truth and this phase deliberately
does not select a winner.

```text
vendor PDFs / captures / APIs / implementations / reviews
                         |
                         v
                    source adapters
                         |
                         v
                    generic claims
                    /            \
             conflicts          queries
                    |
                    v
       PIPELINE-4 declarative reconciliation (later)
```

## Model

The four concepts are separate:

* `sources/claims/source-registry.json` identifies a source and its artifact,
  revision, digest, and authority class. It contains no precedence rule.
* `subject` identifies the thing being discussed. Normal Modbus subjects use
  `namespace=MODBUS`, `table`, and `address`; holding and input addresses are
  consequently different identities. `GROWATT_FC0x20` is a separate
  proprietary namespace. Logical subjects model pairs and other non-physical
  relationships without replacing physical subjects.
* `assertion` records one source statement or observation. Kinds cover source
  rows, names/descriptions/access, packed fields and enums, semantic and
  implementation assertions, raw/decoded reads, cloud correlations, writes,
  readbacks, and human interpretation. `source_text` and `raw_value` retain
  source wording independently from the assertion value.
* `provenance` points to an exact artifact location wherever the retained
  source permits it: PDF claim artifact plus digest/page/row, JSON pointer,
  implementation snapshot pointer, or capture digest. `scope` is separate and
  first-class; unknown applicability is not silently broadened.

Evidence `method`, interpretation `confidence`, and result `status` are
separate fields. In particular `stock_shine_write_observed` is not
`write_verified`: the retained natural Time Period 2 event has no raw FC16
request, CRC, ACK, or readback frame. The legacy evidence field
`reconstructed_request_pdu_without_crc` remains as a compatibility alias; the
new name is `reconstructed_rtu_request_without_crc` because the value includes
the unit address.

## Migration and adapters

`tools/build_generic_claims.py` deterministically projects:

* all three PIPELINE-2 vendor source rows, retaining raw/reconstructed text,
  fragments, continuation references, diagnostics, review state and exact
  source-row provenance;
* retained MIN read-only observations, including H3036-H3059, H3081-H3082,
  I3000/I3101/I3110/I3111/I3165/I3166/I3170/I3211/I3212/I3217 where the
  retained evidence contains the value;
* the RE-4 cloud oracle, including non-discriminating I3166/I3211/I3212
  experiments and provisional I3111 correlation;
* the natural Shine H3040-H3041 logical write/readback event;
* actual retained HA, OpenInverterGateway, Grott, and inverter-to-mqtt
  snapshots. These are implementation assertions, not authority or truth;
* human-reviewed semantic records and the retained proprietary FC0x20
  summary. FC20 is recorded as function byte `0x20` (decimal 32), not as
  Modbus input register 20.

The generated adapter views are in `sources/claims/implementation/`; the
combined deterministic output is `sources/claims/generic-claims.json`.

## Examples and queries

```bash
python tools/query_claims.py --table holding --address 3040
python tools/query_claims.py --table holding --address 3049
python tools/query_claims.py --table input --address 3165
python tools/query_claims.py --table input --address 3111
python tools/query_claims.py --namespace GROWATT_FC0x20
```

H3040/H3041 can show vendor packed layout, retained raw values, and the natural
Shine transition. The retained implementation snapshots do not falsely claim
an H3040 holding mapping; their nearby H3047 and I3047 claims demonstrate the
implementation evidence and namespace boundary. H3047 and I3047
remain separate physical subjects. I3165 shows the vendor codebook, live raw
value, reviewed interpretation and cloud consistency independently. I3111's
cloud relationship remains provisional. The FC20 claim has no Modbus table or
address and cannot collide with FC04/input claims.

## Contradictions and validation

`tools/report_claim_conflicts.py` groups claims by physical/logical subject and
assertion kind, reports differing values, and labels them as wording, access,
datatype, unit, semantic, value, or unresolved categories. It never resolves
or suppresses a conflict. The current report intentionally contains extraction
fragment differences and implementation disagreements; these are inputs to
PIPELINE-4, not failures of this migration.

`tools/validate_claims.py` checks unique IDs, registered sources, namespace and
table/address identity, address ranges, provenance artifacts and JSON
pointers, scope/evidence completeness, and bit ranges. Contradictory claims
remain valid claims.

## Boundary and limitations

This phase does not modify `spec/growatt-register-spec.json`, compatibility
outputs, generator semantics, HA, broker, live configuration, or inverter
state. It does not reconcile wording, resolve source conflicts, or make the
canonical build consume generic claims. Vendor PDF originals, raw captures,
firmware, and installation-specific material remain outside the public claim
projection. Some retained live values (notably I3101/I3110/I3111 and several
other input words) are available as reviewed/cloud evidence rather than a
fresh raw sample in the compact live JSON; their provenance states that
limitation.

PIPELINE-4 should next define declarative subject/property normalization,
conflict review workflows, and explicit source-to-semantic reconciliation.
Only after that review should canonical generation or HA consumers be changed.
