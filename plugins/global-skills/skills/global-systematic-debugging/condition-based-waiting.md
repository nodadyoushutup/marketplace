# Condition-Based Waiting

Wait for an observable contract, not an arbitrary delay. Every wait needs a
bounded timeout and useful, secret-safe failure evidence.

## Preferred order

1. Await the operation's promise, future, task, process, or event.
2. Use the repository or library helper for the observable condition.
3. Poll a stable external condition with a deadline and moderate interval.
4. Use a fixed delay only when elapsed time is itself under test.

Do not create a polling helper when the configured test, process, container, or
client library already provides one.

## Polling requirements

A custom poll must use a monotonic clock, include a deadline, sleep between
checks, return the observed value, stop on terminal failure, and include only a
bounded redacted summary of the last observation in its timeout error. Unit
tests must not poll real production state.

For UI tests, prefer configured web-first assertions on accessible visible
conditions. For asynchronous backend work, prefer result handles, events,
durable state transitions, or library-supported retry assertions. Restore fake
timers and global state during cleanup.

For processes, wait for completion when termination is expected. For servers,
wait for documented readiness rather than sleeping or treating a listening port
as full readiness. Distinguish a container running from a service being healthy.

Before increasing a timeout, determine whether the event never occurs, the
observer subscribes too late, state is cached, cleanup cancels work, another
consumer owns the work, a transaction is uncommitted, global state leaked, or
the deadline is genuinely below the supported latency budget.

Repeat flaky scenarios enough to distinguish a fix from chance and report the
count. Do not repeatedly trigger a mutating operation while waiting for its
result.
