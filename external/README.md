# External project relationships

This repository stores small, normalized snapshots rather than third-party
source trees. The snapshots are evidence inputs to the graph and are not
treated as canonical truth. Exact revisions and URLs are recorded in
`sources/manifest.json` when known.

The current extraction has usable revisions for Grott and
inverter-to-mqtt-esp8266. The OpenInverterGateway checkout available during
the original research was not a git checkout with a verifiable revision, so
its snapshot is retained with that limitation explicitly recorded.

Refreshers under `tools/extractors/` are optional: they require the relevant
external checkout and are not needed for the self-contained build.
