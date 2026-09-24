---
name: code-javascript-refactor
description: >-
  Apply behavior-preserving structural refactoring to JavaScript, TypeScript,
  JSX, React, and browser lifecycles. Use for decomposition, extraction,
  ownership cleanup, or as the JavaScript structure phase of code-deslopify.
---

# JavaScript Refactor

Repository instructions define style, runtime, module, and validation
conventions. This skill governs structural changes to live code.

## Deslop / hygiene phase

Language mechanics for live JavaScript / TypeScript / JSX / React. For an
intentional refactor **audit** (checklist, scope, report), start at
`.cursor/skills/code-refactor/SKILL.md`, which dispatches here.

This is also Phase B of `.cursor/skills/code-deslopify/SKILL.md` and the
**Refactor Check** (phase 3) on per-addon hygiene Stories after Isolation +
Substrate and Deslop. Local structure and naming live here; extracting a new
shared `framework/addons/` substrate is Isolation + Substrate, not this skill —
see `.cursor/rules/framework-addon-hygiene-checks.mdc`.

## Establish the behavior contract

Before moving code:

1. Identify callers, imports, exports, registrations, tests, events, side
   effects, API contracts, and generated boundaries.
2. Record visible behavior, lifecycle guarantees, error semantics, and ordering
   that must remain unchanged.
3. Find focused tests or add characterization coverage when behavior is unclear.
4. Inspect the working tree so unrelated changes are not absorbed.

Use `code-investigation` when dynamic registration, event flow,
generated imports, or cross-runtime ownership is uncertain.

## Structural principles

- Refactor around responsibility, state ownership, and lifecycle, not line count.
- Keep orchestration at one level of abstraction.
- Prefer explicit parameters, return values, props, and context over mutation or
  hidden module state.
- Preserve errors, loading states, accessibility, event order, and cleanup.
- Preserve producer/consumer payload contracts and public identities.
- Avoid circular imports, catch-all helpers, and new dependencies for ordinary
  refactoring.
- Keep structural, behavioral, and styling changes separate unless all are in
  scope.

## Functions and asynchronous work

- Extract complete transformations, decisions, or boundary operations.
- Prefer pure functions for parsing, normalization, filtering, and mapping.
- Preserve `null`, `undefined`, empty, zero, and false semantics.
- Preserve thrown errors, rejected promises, cancellation, and signal handling.
- Keep sequential work sequential; parallelize only independent operations.
- Preserve latest-wins, deduplication, or deliberate concurrency semantics.
- Do not create one-line wrappers unless they name a real domain boundary.

## React components and hooks

- Split components only around clear presentation or stateful ownership.
- Extract hooks when state and lifecycle form one cohesive capability.
- Keep hook order unconditional and state near the smallest owning subtree.
- Compute derived values during render instead of mirroring them through state.
- Keep effects for synchronization with external systems.
- Preserve dependencies and cleanup for requests, subscriptions, timers,
  listeners, observers, sockets, and object URLs.
- Preserve Strict Mode behavior, stale-closure semantics, form initialization
  and reset, intentional cancellation, and failure reporting.
- Preserve loading, empty, unauthorized, failure, and success paths.
- Do not add memoization, context, reducers, or component fragments merely to
  make the refactor look architectural.

## Module boundaries

- Put API calls and response normalization at a clear boundary.
- Put reusable stateful behavior in focused hooks and pure transformations in
  ordinary modules.
- Preserve established module extensions, package aliases, dynamic imports,
  string keys, public exports, and registration identities.
- Update exports deliberately and check for import cycles.
- Preserve type and documentation contracts when moving public symbols.
- Avoid broad `utils`, `helpers`, and `common` modules.

## Workflow and validation

1. Inspect target, consumers, tests, and runtime wiring.
2. Record preserved behavior and the proposed ownership boundary.
3. Choose the smallest useful function, hook, component, or module extraction.
4. Move one responsibility at a time and keep intermediate states runnable.
5. Update imports, exports, types, documentation, tests, and registrations.
6. Review the diff for accidental contract, DOM, accessibility, or style change.
7. Run configured focused tests and static checks, then build, browser, or
   integration checks in proportion to the moved boundary.

Do not assume conventional script names exist. Use repository-configured
commands and do not claim behavior from a successful build alone. Use an AST
codemod only for a repetitive, mechanical, tested transformation; do not use
regex replacement for syntax-aware changes.
