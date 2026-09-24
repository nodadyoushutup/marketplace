---
name: global-docker
description: >-
  Operate Docker and Docker Compose from the host CLI — restart vs rebuild
  decisions, log inspection, health verification, and safe recovery. Use when
  code changes need a container restart, a service is unhealthy, an image must
  be rebuilt, or a Compose stack needs to come up, and when deciding which
  command is the smallest one that applies the change.
---

# Docker

You own Docker for the code you just changed. After an edit that a running
container serves, restart or rebuild it yourself and verify it came back. Do not
hand compose commands to the user.

Run Docker through the host `docker` / `docker compose` CLI. It is already
available wherever the agent has shell access, needs no broker, and covers the
whole surface including `exec`, `rm`, `down`, and `prune`.

## Restart vs rebuild

Pick the smallest command that actually applies the change:

| What changed | Command | Why |
|---|---|---|
| Source behind a bind mount | `docker compose restart <svc>` | Files are already inside the container |
| Source copied into the image | `docker compose up -d --build <svc>` | The image is stale until rebuilt |
| Env var, port, volume, or other compose key | `docker compose up -d <svc>` | Needs container recreation, not a restart |
| `Dockerfile`, lockfile, or dependency manifest | `docker compose up -d --build <svc>` | Image inputs changed |
| Nothing running yet | `docker compose up -d` | Cold start |

Rules that follow from the table:

- `restart` does **not** pick up new environment variables or compose changes. If
  a value from the compose file must change, you need `up -d`.
- `up -d --build` with no service name rebuilds and recreates **everything**.
  Always name the services you mean.
- Batch your edits, then restart **once** at the end. Do not restart per file.
- To recreate exactly one service without touching its dependencies:
  `docker compose up -d --no-deps --force-recreate <svc>`.

## Verify, always

A restart is not done until you have checked it. In order:

```bash
docker compose ps                      # state and health
docker compose logs --tail 80 <svc>    # startup errors
curl -s -o /dev/null -w "%{http_code}\n" http://127.0.0.1:<port>/<healthpath>
```

Loopback is for checks run in the execution shell. User-facing URLs must follow
the repository's host-address guidance.

`Up` is not `healthy`. A container that restarts in a loop reports `Up` between
crashes — check `ps` twice or read `restarts` in `docker inspect`. When a service
declares a healthcheck, wait for `healthy` rather than sleeping a fixed time.

## Diagnose a failing container

1. `docker compose logs --tail 120 <svc>` — read the first error, not the last.
2. `docker compose ps` — is it restarting, exited, or unhealthy?
3. `docker inspect <container>` — env, mounts, networks, exit code.
4. `docker compose config` — what Compose actually resolved after `.env`
   interpolation. Use this whenever a variable looks unset.
5. `docker compose exec <svc> sh` — inspect the live filesystem when the mount
   or a generated file is in question.

Exit code 137 is OOM or SIGKILL; 1 is usually an application error in the logs.

## Networks and name collisions

- Service names resolve as hostnames only within a shared network. A container on
  another Compose project is unreachable unless both join the same network.
- When two Compose projects publish the same service alias, the hostname is
  ambiguous from a container attached to both. Give the one you depend on a
  unique network alias and use that name.
- `Conflict. The container name "/x" is already in use` means an orphan from a
  previous project name. `docker rm -f <name>` then `up -d`.

## Safety

- Never commit `.env` or paste secrets from it into output.
- `docker system prune`, `down -v`, and `rm -f` on a data service destroy
  volumes. Ask before running any of them.
- Do not restart shared or production services, run migrations, or clear
  data stores without explicit authorization.
- Treat a mounted `docker.sock` as host-root authority. Never publish it beyond
  loopback.

## Project overlays

A repository that defines its own stack owns the service table, the per-service
restart decisions, and any service that must not be touched. When the repo ships
a `framework-docker-ops` skill or rule, that file wins for those specifics; this skill
covers the general craft.
