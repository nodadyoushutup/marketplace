# Runtime Debugging Playbooks

Use only sections relevant to the observed failure.

## Application startup or routing

- Compare effective configuration and precedence with documented requirements.
- Trace entrypoint imports, registrations, route or command binding, and startup
  ordering.
- Distinguish liveness, readiness, registration, and dependency health.
- Verify the correct process reloaded after discovery inputs changed.
- Do not create a second application or connection merely to inspect behavior.

## Database and migrations

- Establish the exact database/schema, revision state, failing operation, and
  transaction/rollback state.
- Distinguish query, validation, serialization, flush, commit, and post-commit
  side-effect failures.
- Use read-only inspection first.
- Never rewrite an applied migration or use ad hoc stamping, downgrade, drop,
  reset, recreation, or shared-data mutation as exploratory repair.

## Registration or discovery

```text
configuration or mounted source
→ entrypoint
→ module import
→ registration identity
→ public inventory
→ consumer lookup
```

Import success does not prove registration. Verify the owning process and
effective public inventory.

## UI rendering and interaction

- Inspect visible state, console errors, requests/responses, and event cleanup.
- Verify loading, empty, unauthorized, error, cancellation, stale-response, and
  success paths.
- Reproduce through user-visible actions and assert accessible output.
- Check effect dependencies, duplicate setup, stable identity, and cleanup.

## Workers, queues, and schedules

- Separate registration, persistence, enqueue, routing, execution, retries,
  redelivery, idempotency, scheduling, and singleton ownership.
- Use an isolated known payload.
- Do not purge queues or manually mark work successful to hide the symptom.

## Tool or protocol integrations

- Classify service startup, transport/session setup, capability discovery,
  schema validation, handler execution, result normalization, and upstream
  access separately.
- A successful liveness response does not prove capability registration or
  upstream readiness.
- Keep credentials out of logs and use sandbox or read-only operations first.

## Containers and orchestration

- Compare rendered configuration, image/build inputs, command/entrypoint, mounts,
  volumes, networks, effective user, environment presence, healthcheck, restart
  count, and internal versus published ports.
- Inspect only the affected service first.
- Rebuild when image contents changed, recreate when startup configuration
  changed, and restart when code is mounted but discovery occurs at boot.
- Avoid volume deletion, pruning, and broad stack teardown.

## Performance

Measure a representative workload and baseline. Separate queue delay, execution,
queries, payload size, network latency, rendering, retries, CPU, memory, and I/O
at the owning boundary. Profile the smallest representative path; do not hide
latency by increasing timeouts.

## Build or CI-only failures

Compare resolved dependency versions, runtime and platform, environment
presence, working directory, generated artifacts, test order, parallelism,
isolation, and cache state. Do not clear every cache first; test the smallest
specific cache or dependency hypothesis while preserving original evidence.
