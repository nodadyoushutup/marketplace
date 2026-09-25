---
name: compose
description: >-
  Agnostic Docker Compose craft: multi-file COMPOSE_FILE layout, project-directory
  anchors, overlays/profiles, day-to-day ops, and hard gates on destructive
  downs/volume wipes. Skip when the user did not authorize Compose work.
---

# compose

## Gate

No explicit Compose / `docker compose` / stack bring-up / overlay / profile ask
→ **skip**. Ordinary app coding does not require this plugin.

## Load map

| Need | Rule |
| --- | --- |
| File layout, `COMPOSE_FILE`, project dir, env paths | `compose-files` |
| `up` / `ps` / `logs` / `config` / pull / pin tags | `compose-ops` |
| `down -v`, volume wipe, prune, secret dumps | `compose-safety` |

## Defaults

1. Resolve the Compose project directory before mutating — never guess.
2. Prefer `docker compose config` (or equivalent) to prove the merge, then act.
3. Pin image tags in Compose; do not silently float on `latest` for shared stacks.
4. Pair with `global-host-url` for any user-facing URL (never hand the user
   `localhost`).
5. Pair with `vault` when credentials belong in a secrets store — not chat.
