---
name: kopia
description: >-
  Agnostic Kopia craft: repository and snapshot inventory plus gated
  snapshot/restore/forget. Prefer MCP when connected; otherwise kopia CLI.
  Skip when the user did not authorize this surface.
---

# kopia

## Gate

No explicit Kopia / snapshot / repository backup ask → **skip**. Kubernetes
Velero asks belong in `velero` — do not absorb them here. Prefer a connected
MCP (`global-mcp-first`); else `kopia` CLI against a resolved repository config.

## Load map

| Need | Rule |
| --- | --- |
| List repos / snapshots / policies | `kopia-inventory` |
| Snapshot / restore / forget / maintain gates | `kopia-safety` |

## Defaults

1. Never invent repository path, snapshot id, or policy path — list/resolve first.
2. Resolve repo config from operator config/env — never invent credentials.
3. Read inventory before mutate; restores are data-loss shaped.
4. Pair with `velero` for cluster backups; this plugin owns Kopia repos/snapshots.
