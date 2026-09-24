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

## Framework → custom-addon identity and purpose leakage

**Smell:** tracked framework or `framework/addons/*` code imports, names, or
encodes a specific custom addon from `addons/<name>/` — including comments,
fixtures, env examples, and identifiers whose purpose is that product
(`is_example_widget_…`, `example_host_…` keys, hard-coded hostnames, etc.).

**Smell (tests / purpose):** a framework or runtime test exists mainly to prove
a custom-addon feature (settings table, product workflow, domain class set,
overlay policy). Invented `example.*` names do **not** clear this smell. Product
coverage belongs under `addons/<name>/`.

**Check:** `python3 scripts/addon/check_addon_isolation.py` and
`.venv/bin/python scripts/addon/check_addon_dependencies.py`; also reread touched
symbols and new tests for product-specific vocabulary and motivating scenarios
the checkers may miss. Ask: would this test still be written if that addon
never existed?

**Fix:** move the surface or test into the owning custom addon, or replace it
with a generic framework contract the addon registers. Invented fixtures
(`example_addon`, `example.record`) are fine **only** for generic substrate
contracts. Declared base↔base addon edges are not this smell.

**Addon-dev note:** when the session is custom-addon work, prefer fixing inside
`addons/<name>/`. A framework edit to clear leakage needs an explicit handoff
justification (see isolation rule).

## Do not strip automatically

- live public or persisted compatibility contracts
- security reconciliation or credential migration
- dynamic registrations and package entrypoints
- generated or vendored outputs
- applied migrations
- externally consumed APIs
- behavior that is merely unfamiliar or has no easy textual reference
