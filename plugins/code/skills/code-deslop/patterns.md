# Hygiene Patterns

Use these as prompts for evidence, not a checklist.

## Dead files, exports, and branches

**Smell:** a symbol appears only in its definition and re-export, or a branch
depends on a value no producer emits.

**Check:** dynamic imports, registries, reflection, configuration, entrypoints,
scripts, tests, serialized data, and external APIs.

**Fix:** delete the definition and transitive residue only at Verified or
Probable confidence.

## Obsolete dual paths

**Smell:** `current ?? legacy`, alternate key spellings, or two readers for one
meaning.

**Check:** exact producer output, persisted forms, compatibility policy, and
external consumers. Similar spelling is not proof of equivalence.

**Fix:** keep the canonical contract and remove the obsolete arm. If both forms
remain live, coordinate producer and consumer changes or leave it Suspected.

## Thin wrappers and trivial indirection

Inline one-use pass-through functions, components, and methods that add no
policy, lifecycle, naming contract, or reuse. Keep wrappers that establish a
public boundary, stable identity, or meaningful domain vocabulary.

## Silent failure

Empty catches and rejected operations converted to success hide broken state.
Preserve explicit error propagation and add bounded, redacted context where
useful.

## Incomplete wiring

Controls without handlers, registrations without implementations, placeholder
modules, always-empty allowlists, and no-op hooks should be completed when the
contract is live or deleted when it is not.

## Premature abstraction

Generic helpers with one trivial implementation, catch-all utility modules, and
speculative extension points increase surface without reducing complexity.
Inline or move behavior to the owner. Do not merge implementations whose
validation, ordering, retry, or error semantics differ.

## Derived state and memo noise

Remove state, effects, memoization, or callbacks that only mirror current inputs
when no identity, performance, or lifecycle contract requires them. Preserve
observable ordering and cleanup.

## Test and fixture residue

After deleting behavior, remove or rewrite tests, fixtures, snapshots, exports,
and comments that only assert the deleted surface. Finish broader permanence
review in [test-review.md](test-review.md).

## Host isolation leakage (when the repo has product packages)

**Smell:** shared/substrate code imports, names, or encodes a specific product
package — including comments, fixtures, and identifiers whose purpose is only
that product.

**Fix:** move the surface or test into the owning product package, or replace
it with a generic contract the product registers. Follow host isolation rules
when present.

## Do not strip automatically

- live public or persisted compatibility contracts
- security reconciliation or credential migration
- dynamic registrations and package entrypoints
- generated or vendored outputs
- applied migrations
- externally consumed APIs
- behavior that is merely unfamiliar or has no easy textual reference
