# Test Review

Turn development verification into a small permanent suite that protects public
behavior without freezing implementation details.

## Scope

Review tests added or edited in the current change, tests owned by the touched
feature, and tests that only reference behavior removed in Phase A. Do not roam
the repository during an automatic pass.

## Disposition

| Disposition | Action |
|---|---|
| **Delete** | Remove one-off, duplicate, placeholder, import-only, source-text, or orphan tests |
| **Promote** | Rewrite a useful session check around a stable public contract |
| **Keep** | Preserve an existing deterministic contract or regression test |
| **Gap-fill** | Add the smallest test for a clear uncovered boundary |

Prefer promotion when a transient check caught behavior that must remain
guarded. Leave unclear product intent as Suspected rather than deleting it.

## One-off smells

- names such as scratch, temporary, manual, verify-fix, or smoke-only
- assertions that a module imports, a file exists, or source contains a string
- exact private call graphs or helper call counts with no public outcome
- duplicated scenarios in multiple files
- tautologies that reassert values built by the test
- live credentials, real provider calls, or production runtime state
- fixtures and snapshots for deleted paths
- empty modules and `assert True` placeholders

## Permanent target

Prefer focused tests for validation and rejection, public payload or return
shape, authorization where applicable, persistence and side effects at mocked
boundaries, registration and discovery, lifecycle cleanup, cancellation, and
error propagation. Keep one clear scenario per test and preserve the owning
suite's isolation, fixtures, cleanup, and naming conventions.

## Promotion rules

1. Put the test in the owning suite and name the lasting contract.
2. Use established fixtures instead of copying session bootstrap.
3. Assert user-visible or public-boundary outcomes.
4. Restore environment and global state; avoid suite-order dependence.
5. Mock at the owned external boundary.
6. Keep one regression test when a one-off exposed a real bug.

Gap-fill only obvious holes. Do not create exhaustive matrices, replace one
test layer with another without cause, or expand production code merely to make
tests easier to write.

Run the smallest focused test first, then the owning suite or repository gate.
