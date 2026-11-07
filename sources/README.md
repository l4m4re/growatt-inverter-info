# Source and evidence corpus

This directory contains the retained inputs used to trace and extend the
current specification.

- `consolidated/register-blocks.json` is the accepted current block model read
  by the product builder.
- `legacy/compatibility-registers.json` preserves the frozen predecessor and
  the legacy/non-V1.24 knowledge carried into the current JSON.
- `vendor/` contains vendor-native block structures and profiles.
- `claims/vendor/` contains structured source rows and their provenance.
- `claims/implementation/`, `external/`, and `runtime/` retain
  implementation and runtime snapshots for correlation.
- `evidence/` contains reviewed, structured evidence records.
- `curated/` contains reviewed source overlays and normalization data.
- `vendor/growatt-vpp-v2.01-registers.json` contains the normalized VPP V2.01
  rows imported from `Growatt_ModbusTCP`.
- `vendor/growatt-vpp-v2.03-delta.json` contains the normalized VPP V2.03
  rows that are new or changed relative to V2.01. It is an overlay, not a
  replacement for the V2.01 base and not proof of firmware implementation.
- `external/growatt-modbus-tcp-registers.snapshot.json` records the source
  revision and hashes used for the bidirectional repository correlation.
- `evidence/zaba22-firmware-register-correlation.json` contains derived,
  public-safe static firmware evidence; it does not contain firmware bytes.
  Its `arm_modbus_reconstruction` section keeps the ARM VPP access/conformance
  matrix, V2.03 target audit, and FC20 producer/provider correlation in GII so
  consumers can validate register-map claims against the firmware analysis
  without importing the private analysis checkout.
- `evidence/min-6000tl-xh-portal-battery-settings-20261107.json` records the
  controlled portal-to-Modbus write mapping for the MIN 6000TL-XH Battery
  Settings page, scoped to the observed communication firmware.

The root `manifest.json` records source publication and handling policy. Raw
vendor PDFs, firmware, portal exports, and unreviewed live captures are not
redistributed here.

For adding new evidence, recording human review, updating the consolidated
model, and handing an accepted result to Home Assistant, follow
[`../docs/REGISTER_KNOWLEDGE_WORKFLOW.md`](../docs/REGISTER_KNOWLEDGE_WORKFLOW.md).
