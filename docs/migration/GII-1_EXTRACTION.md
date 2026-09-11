# GII-1 extraction checkpoint

Status: `GROWATT_INVERTER_INFO_BASELINE_ESTABLISHED_WITH_FOLLOW_UP`

The register/reverse-engineering knowledge pipeline has been extracted from
the consolidated HA research line into this repository. The extraction is a
history-filtered copy with the meaningful register-specification history
retained; Git object IDs are necessarily rewritten by the filtering step.
The source HA repository was not rewritten, rebased, cleaned or otherwise
modified.

## Included

- vendor-derived structured V1.24 table data;
- curated register and datatype interpretations;
- normalized snapshots from Grott, OpenInverterGateway and
  inverter-to-mqtt-esp8266;
- the HA mapping snapshot as implementation evidence;
- sanitized MIN 6000TL-XH map, live-read and native-block evidence;
- graph, consolidated audit, compatibility reference and canonical spec;
- deterministic builders, validators, tests and optional extractors.

The canonical product is `spec/growatt-register-spec.json`. The compatibility
JSON remains available for bounded consumer migration, but its metadata
explicitly identifies it as generated and non-canonical.

## Excluded or deferred

Vendor PDFs and text exports, firmware/flash dumps, portal data, raw captures,
credentials, private installation identifiers, broker code/configuration and
the HA runtime were not copied. PDF checksums and source classifications are
recorded in `sources/manifest.json`. The Shine/proprietary protocol remains a
separate research thread and is not represented as ordinary Growatt register
semantics.

Exact external revisions are pinned where the local checkout provided a
verifiable Git revision. OpenInverterGateway did not provide one in the source
workspace, so its normalized snapshot is explicitly marked as unpinned.

## Follow-up before consumer migration

1. Review the generated canonical spec and its source classifications.
2. Resolve any remaining source/legal publication questions, especially for
   vendor-derived rows.
3. Add project-independent register tests as new semantics are accepted.
4. Migrate HA and broker consumers in a separate reviewed change; preserve HA
   entity identity/statistics and the existing runtime safety contract.
5. Add write evidence only after controlled, reversible hardware validation.
