# Register knowledge workflow

This document describes how new Growatt register knowledge moves from an
observation to the published specification and then to consumer repositories.
It applies to vendor documentation, independent implementations, read-only
Modbus captures, Shine or cloud correlations, portal observations, and
Home Assistant Recorder correlations.

The project-independent authority is this repository. A consumer repository
may keep a pinned snapshot or a generated consumer projection, but it must not
become a second source of semantic truth.

## Authority and storage

Use these locations for the different kinds of information:

| Information | Location | Role |
| --- | --- | --- |
| Vendor and implementation claims | `sources/claims/`, `sources/vendor/`, `sources/external/` | Retained source wording and provenance |
| Live, portal, cloud, and Recorder observations | `sources/evidence/` | Structured observations, captures, limitations, and correlations |
| Source identities | `sources/claims/source-registry.json` | Stable IDs and artifact metadata |
| Reviewed claim overlays | `sources/claims/generic-claims.json` or a dedicated reviewed artifact | Normalized claims with explicit evidence status |
| Accepted current model | `sources/consolidated/register-blocks.json` | Only reviewed current register semantics and applicability |
| Published products | `spec/` | Generated machine-readable JSON and Markdown |
| Review decisions | `docs/consolidation/` or a focused review document | Conflicts, dispositions, rationale, and acceptance record |

Raw credentials, private portal exports, unredacted network captures, and
large time-series datasets stay outside the public repository. Store a
redacted, reproducible summary with a hash or source reference when it is
needed to support a public claim.

## Lifecycle

### 1. Capture an observation

Start with a separate evidence artifact. Do not edit the generated
specification or rename a register based on a single observation.

Record enough context to reproduce or assess the result:

- model, family, firmware, protocol and device identity scope;
- holding versus input table and the complete address or block;
- acquisition method, timestamp and relevant operating mode;
- raw value and decoded value, including unit and scaling;
- source artifact or capture hash;
- missing data, alternative interpretations and other limitations.

For portal or GUI work, record the control label, the value before and after a
controlled change, the device readback and whether the UI label is only a
correlation. For Recorder work, record the mode, register values, time window,
SOC/power transitions and gaps in the historical data. A Recorder correlation
is behavioural evidence; it is not automatically a protocol definition.

Add a stable `source_id` to `sources/claims/source-registry.json` and keep the
artifact path, source type, authority class and redistribution status there.
Use the existing evidence and claims schemas instead of inventing a second
format.

### 2. Review and classify

Review the new evidence against the vendor table, applicability declaration,
independent implementations and existing live evidence. Keep disagreements
visible. The review record should state:

- the affected `(family, table, address)` identity;
- the original observation and competing claims;
- the disposition and confidence;
- the resolution basis and remaining limitations;
- whether the result is an observation, a provisional interpretation, a
  resolved semantic correction, or an unresolved conflict.

Use a dedicated review document or evidence record similar to
[`min-6000tl-xh-semantic-review.json`](../sources/evidence/min-6000tl-xh-semantic-review.json)
and the consolidation records under `docs/consolidation/`. A reviewed
correction may supersede an extraction mistake in the current model, but the
historical source claim and its original value remain intact.

Reads establish that a register can be read; they do not prove its semantic
meaning. Writes require a separately justified and controlled experiment, with
the resulting risk and readback documented explicitly.

### 3. Accept the current model

After human review, update
`sources/consolidated/register-blocks.json` only with the accepted current
interpretation. Keep conflicts and unresolved alternatives in the source or
review artifacts when they are not resolved.

Regenerate and validate the products:

```bash
python tools/build_spec.py
python tools/validate_spec.py
```

Run the relevant tests, inspect the generated diff, and commit the evidence,
review decision, consolidated model and generated products together. The
commit message or review document should identify the accepted source commit
and the scope of the change.

### 4. Consume the accepted result in Home Assistant

The HA integration consumes an accepted GII commit; it does not promote a
local runtime observation directly into the shared specification.

For each consumer update:

1. Record the exact GII commit and spec checksum in the HA change document.
2. Compare the relevant `(family, table, address)` rows and applicability
   paths with the current runtime mapping.
3. Update the HA runtime mapping or decoder only in a separate, reviewable HA
   change. Generated GII products are input to that review, not generated
   runtime code.
4. Regenerate the HA compatibility/audit views that are still maintained in
   that repository, and run both register-reference and integration tests.
5. Record entity, unit, sign, statistics and Recorder-continuity impact before
   changing an existing HA entity.
6. Link the HA commit back to the GII commit. If the consumer finds a new
   conflict, add evidence to GII first and leave the HA interpretation
   explicitly provisional until it is reviewed.

Until the automated consumer projection is implemented, the HA repository's
`doc/register-spec/` files are migration and compatibility artifacts. They
must carry the GII source commit they were compared with and must not be
treated as an independent canonical register map.

## Review checklist

Before accepting a register change, confirm:

- [ ] evidence is stored under `sources/` with a source-registry entry;
- [ ] holding and input identity are kept separate;
- [ ] family/model applicability is explicit;
- [ ] raw observations and normalized semantics are both retained;
- [ ] conflicts, alternatives and limitations are visible;
- [ ] portal labels or Recorder correlations are not presented as protocol
      proof without supporting evidence;
- [ ] the current consolidated model was changed only after review;
- [ ] generated products and validators are up to date;
- [ ] the consuming HA change records the GII commit and its runtime impact.
