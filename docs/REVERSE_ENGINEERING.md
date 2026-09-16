# Reverse engineering safely

Use this guide when collecting evidence for a future register review. Keep new
observations separate from vendor wording and from normalized register
semantics until they have been reviewed.

1. Compare the relevant vendor table and applicability declaration.
2. Inspect independent implementation snapshots and record their versions or
   source commits.
3. If hardware evidence is needed, capture read-only Modbus traffic and retain
   the device/model, firmware, function code, address range, and acquisition
   conditions.
4. Correlate cloud or Shine behavior as a separate evidence source. Record
   exactly what the interface exposed and avoid treating labels as protocol
   proof.
5. Add structured evidence under `sources/`, with provenance and limitations.
6. Review the evidence and any conflict explicitly, then update the current
   consolidated source and regenerate the specification.

Reads do not prove register semantics. Polling an address range does not prove
that every address exists or has meaning. A write requires a separately
justified, controlled experiment; persistent configuration writes should be
minimized. This repository's normal build and validation do not communicate
with an inverter or a cloud service.
