---
name: code-systematic-debugging
description: >-
  Diagnose bugs, test failures, flaky behavior, performance regressions, build
  failures, and runtime integration problems before fixing them. Use whenever
  behavior is unexpected or the cause is not already proven.
---

# Systematic Debugging

Find the smallest evidence-backed explanation that accounts for the observation.
Do not confuse a plausible symptom with a verified cause.

## Authorization and scope

Distinguish:

- **Diagnose:** investigate and report; do not implement a fix.
- **Fix:** investigate, make the smallest justified correction, and verify it.
- **Mitigate:** preserve service safely within explicit authority, label the
  mitigation, and continue root-cause work afterward.
- **Monitor:** observe the requested condition without treating unchanged state
  as failure.

Do not deploy, restart shared or production services, mutate external systems or
data, run migrations, rotate credentials, clear queues or caches, or use
destructive container/database commands without explicit authorization.
Local-dev restarts of the services under change are already authorized when the
user asked for a fix. Confirm definitive authentication, authorization, quota,
entitlement, or access denials once when useful and report them; do not bypass
them. Do not stop to ask whether to diagnose vs fix when the user reported a
bug — fix it.

## Preparation

1. Read repository instructions for affected language, runtime, data, tests,
   operations, and documentation.
2. Read the nearest implementation, tests, configuration, and hand-authored
   docs.
3. Inspect active processes before starting another server, watcher, worker, or
   dependency.
4. Use `.cursor/skills/code-investigation/SKILL.md` for non-trivial
   behavior tracing.

## Phase 1 — Establish the failure

Record expected behavior and its source, actual behavior and complete error,
minimal reproduction, first known failing boundary, affected environment and
data scope, recurrence pattern, last known working state, and relevant changes.

Preserve safe identifiers, timestamps, status codes, and failing test names.
Do not dump environments, headers, cookies, credentials, private payloads, or
database rows. Record only secret presence, source, and safe fingerprints.
Use isolated fixtures, mocks, sandboxes, disposable data, or read-only requests
when reproduction could mutate persistent state or call a real provider.

## Phase 2 — Localize the boundary

Trace the minimum complete path:

```text
user or client input
  → transport or interface
  → validation and authorization
  → orchestration and domain logic
  → persistence or external dependency
  → returned, emitted, or rendered result
```

At each boundary compare input schema, output contract, configuration source,
registration state, persisted state, process ownership, restart/discovery
lifecycle, timing, cancellation, retries, and idempotency.

Prefer existing logs, tests, health/readiness checks, traces, request IDs,
browser evidence, and safe read-only inspection. Add temporary instrumentation
only when it distinguishes hypotheses, code changes are authorized, and output
can remain bounded and secret-safe. See
[root-cause-tracing.md](root-cause-tracing.md).

## Phase 3 — Test hypotheses

Use one falsifiable hypothesis:

```text
Cause: <specific mechanism>
Evidence: <observations it explains>
Discriminator: <smallest safe confirming or rejecting check>
Expected result: <observable outcome>
```

Rank by evidence, test one variable at a time, and prefer reversible read-only
checks. When a hypothesis fails, record the evidence, remove temporary changes,
revisit assumptions, and form a new hypothesis. Do not stack speculative fixes.
Stop for user direction only when execute-first names a blocker (irreversible
data loss, a missing secret, or two incompatible user-visible outcomes with no
reversible default). A broad or product-defining ownership change is that third
blocker only when there is no reversible default; otherwise pick the existing
code's owner and continue.

## Phase 4 — Correct the cause

When authorized:

1. Add the smallest reliable regression test when practical.
2. Correct the earliest owned contract violation.
3. Keep unrelated refactors out.
4. Coordinate public contract changes across all owners when required.
5. Remove temporary diagnostics or retain only bounded, redacted observability
   with ongoing value.

A mitigation may precede complete analysis when it is safer during an incident.
State risk and rollback and do not hide corruption or access failures. Do not
force an automated test when the failure cannot be represented safely or
deterministically; document the reproduction and strongest practical check.

## Phase 5 — Verify

Verify in increasing scope:

1. original reproduction
2. focused regression test
3. owning suite with normal isolation
4. adjacent contracts and integrations as risk warrants
5. runtime registration, readiness, and behavior at crossed boundaries

A process being up, a port opening, or a build passing does not prove the
contract. Repeat intermittent scenarios enough to distinguish a correction from
chance and report the count. Use [runtime-playbooks.md](runtime-playbooks.md)
and [condition-based-waiting.md](condition-based-waiting.md) as needed.

## Report

Report the observed failure and scope, verified root cause or clearly labeled
leading hypothesis, decisive evidence, mitigation and residual risk, changed
files and behavior when authorized, exact verification and results, and blocked
checks. Never invent a root cause to make the investigation look complete.
