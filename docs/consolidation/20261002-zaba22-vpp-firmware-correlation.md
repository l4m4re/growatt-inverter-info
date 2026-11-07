# ZABA22 firmware and VPP V2.01 correlation

## Scope

This review imports the normalized Growatt VPP V2.01 register rows and the
public-safe static analysis projection of the ZABA22 firmware for the
MIN 2.5-6KTL-XH/XH2 family. The firmware binary, raw serial captures and
hardware access remain outside this repository.

The source rows originate from the checked-in \`Growatt_ModbusTCP\` repository;
the exact source revision and file hashes are retained in
[sources/external/growatt-modbus-tcp-registers.snapshot.json](../../sources/external/growatt-modbus-tcp-registers.snapshot.json).
The firmware-derived evidence is retained in
[sources/evidence/zaba22-firmware-register-correlation.json](../../sources/evidence/zaba22-firmware-register-correlation.json).

## Accepted VPP source projection

The canonical specification now contains 180 normalized VPP V2.01 rows in
seven source-native blocks:

- FC03 holding: 30000–30999 and 32000–32099;
- FC04 input: 31000–31599;
- family scope: MIN/TL-XH/XH2 VPP V2.01.

These rows are marked \`SOURCE_ONLY\` in the generated specification. That
records the protocol source without claiming that every reserved or
model-conditional row is populated by every inverter.

The model-specific XH profiles remain available in the firmware correlation
source. In particular, the profile distinguishes the MIN TL-XH and MIN TL-XH2
layouts and retains the alternative interpretations around input 31018/31019.

## Static firmware facts

- ZABA22 FC03 uses the VPP holding table at `0x0802ae24` with byte offset
  `2 * (address - 30000)`; the complete-request guard gives direct
  single-word coverage through 30498, while 30499 falls through.
- ZABA22 FC04 uses the VPP input table at `0x0802ae28` through address 31299
  for single-word reads, subject to the complete-request guard; 31300 falls
  through.
- The recovered write switch contains exact cases for VPP control addresses,
  including 30100, 30101, 30407, 30408, 30409 and 30410. It contains 74
  exact cases in the recovered \`modbus_write_registers\` body, all in the
  30100–30475 span.
- Legacy FC03/FC04 provider ranges and their storage expressions are retained
  separately in the firmware evidence artifact; they are not flattened into
  the VPP table.

## Conflicts and limits

- VPP documents 30409 as signed INT16 with range -100..100, while the
  recovered ZABA22 write comparison accepts unsigned raw values 0..100.
- Input 31018/31019 have mutually exclusive 2-string and 3-string profile
  interpretations. The canonical VPP source rows preserve the protocol
  document; the profile alternatives remain evidence rather than a forced
  canonical choice.
- A provider symbol is not a runtime RAM address. The evidence artifact
  preserves the distinction between public register, provider, pointer and
  field offset.

The evidence artifact also exposes an `arm_modbus_reconstruction` section for
downstream tooling. It includes the complete VPP access/conformance rows, the
V2.03 target-address audit, and the FC20 channel-0/producer/provider
correlations with hashes of the originating reports. This is a derived
validation projection: unresolved meanings and documentation-only claims stay
marked as such.

## Rebuild and validation

From the GII checkout with sibling source repositories available:

\`\`\`bash
python tools/import_vpp_and_firmware_analysis.py
python tools/build_spec.py
python tools/validate_spec.py
\`\`\`

The importer is deterministic and only writes normalized/public-safe source
artifacts and the consolidated VPP source projection.
