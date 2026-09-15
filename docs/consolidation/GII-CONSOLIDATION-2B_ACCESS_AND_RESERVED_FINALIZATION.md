# GII-CONSOLIDATION-2B — Review-resolved access and reserved-state finalization

This additive current-state correction records reviewed conclusions without
rewriting historical C2/C2A artifacts or the frozen canonical specification.

## Current resolutions

| Register | Current result | Resolution |
|---|---|---|
| H122 | `read_write` | reviewed vendor correction; current reviewed raw access `R/W` |
| H123 | `read_write` | reviewed vendor correction; current reviewed raw access `R/W` |
| H1002 | `read_write` | reviewed vendor access enriches canonical read evidence |
| H1003 | `read_write` | `W` means writable marker; existing read evidence is retained |

The historical extracted H122/H123 value `R` remains in the historical source
claim. The current candidate carries the reviewed correction explicitly and
does not silently rewrite that provenance.

## Reserved ranges

| Range | Current status | Basis |
|---|---|---|
| H3115–H3124 | `RESERVED` | explicit vendor reserved rows |
| I3281–I3374 | `RESERVED` | vendor range, no semantic rows, Shine reads range, repeated all-zero observations |

I3250–I3280 remains outside the reserved tail and is not changed. The current
candidate does not instantiate individual semantic registers for I3281–I3374.

## Counts and lineage

- Retained access conflicts: `4` before → `0` after.
- Active current research queue: `0`.
- Candidate register count: `1486`.
- Parent C2A candidate SHA-256: `b3f0644ecdc7691db53412a1d1dd830dfdd5597cb8f6880dc2748a8bff962ec6`.
- Frozen canonical SHA-256: `e692d646e34040af999ba4854f65803e4218e184d9e04f2982c06d60782ee405` (unchanged).
- Historical C2/C2A and PIPELINE-6..11 artifacts remain unchanged.
- No HA, broker, inverter, Shine, cloud, or live operation was performed.

## Access normalization

In the V1.24 holding-register write-capability column, `R/W` means readable
and writable, `R` means readable and not writable, and `W` means writable with
readability unspecified. `W` is never treated as proof of write-only access.

## Generated current artifacts

- `spec/growatt-register-spec-v2-candidate.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2B_ACCESS_AND_RESERVED_FINALIZATION.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2B_CONFLICTS.json`
- `docs/consolidation/data/GII-CONSOLIDATION-2B_RESEARCH_QUEUE.json`

`GII_C2B_REVIEW_RESOLVED_FINALIZATION_ACCEPTED`
