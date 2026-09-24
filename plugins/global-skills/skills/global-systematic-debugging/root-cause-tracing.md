# Root-Cause Tracing

Trace the failure backward to the earliest owned boundary that violated a
contract.

For each step record:

```text
Boundary:
Observed input:
Expected input:
Observed output or state:
Caller or producer:
Evidence:
```

Keep moving upstream while a layer received already-invalid state. Stop when a
layer produced invalid output, omitted validation at a trust boundary, used the
wrong transaction owner, emitted a side effect at the wrong time, registered
the wrong capability, used stale configuration, or broke lifecycle,
cancellation, cleanup, retry, or idempotency guarantees.

An exception site is not automatically the cause. A database can correctly
reject invalid state produced earlier; a UI can correctly fail on malformed
input; a worker can correctly reject an unregistered operation.

## Generic trace paths

```text
interaction → handler → request → validation → domain logic
            → persistence/external call → response → consumer state

scheduled input → dispatch → queue or transport → execution → retry/result

client → transport/session → registration/schema → handler
       → external dependency → normalized result or error
```

Compare one working path when available and list only meaningful differences.
Confirm the proposed cause predicts both the failure and the discriminator.

## Instrumentation

Use existing logs, traces, tests, request IDs, and safe health metadata first.
Temporary instrumentation should sit at the narrow discriminating boundary,
record only stable IDs, types, counts, transitions, and correlation, avoid
changing race timing, and redact secrets, connection strings, private payloads,
and personal data. Remove it afterward unless it has durable value.

Report root cause, trigger, contributing factors, and downstream symptoms
separately. Add validation where a boundary owns it rather than duplicating the
same guard at every layer.
