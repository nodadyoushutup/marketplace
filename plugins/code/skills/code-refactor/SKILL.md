---
name: code-refactor
description: >-
  Audit and apply behavior-preserving structural refactoring across Python and
  JavaScript/TypeScript/JSX. Use for refactor audit, ownership/decomposition
  cleanup, or when asked to restructure live code without behavior change.
---

# Refactor

Intentional **behavior-preserving** structure work on live code: ownership,
decomposition, naming drift, readable modules.

## When to use

- User says refactor audit / restructure / ownership cleanup / decomposition
- After `code-deslopify` needs a focused structure pass
- Clear live-code structure debt in a bounded scope (not a rewrite epic)

Do not use for feature behavior changes, dead-path deletion (`code-deslopify`),
or inventing shared platform packages from product code.

## Audit mode

Default to **audit and fix** for an explicit refactor request. For a
review-only ask, stay **read-only**: inventory candidates and recommended
moves; skip edits.

## Scope

Bound to named paths, a package, or the current change plus direct
callers/tests. Exclude generated, mirrored, vendored, and applied migration
files. Do not absorb unrelated dirty-tree work.

## Workflow

```
Refactor:
- [ ] 1. Scope (paths / languages)
- [ ] 2. Behavior contract (callers, tests, identities)
- [ ] 3. Inventory structural candidates
- [ ] 4. Apply language mechanics (below) or report only
- [ ] 5. Validate focused / owner checks
```

### 1. Scope

State paths and languages (Python, JS/TS/JSX, or both). Prefer the smallest
set that contains the ownership problem.

### 2. Behavior contract

Before moving code:

1. Identify callers, tests, public imports/exports, registrations,
   entrypoints, serialization, events, and side effects.
2. Record behavior, errors, ordering, identities, and lifecycle ownership that
   must remain unchanged.
3. Find focused tests or add characterization coverage when behavior is
   unclear.
4. Use `code-investigation` when ownership or reachability is uncertain.
   Missing textual references do not prove an API is unused.

### 3. Inventory

| Candidate | Confidence guide |
|-----------|------------------|
| Mixed ownership in one module | Probable |
| Name drifted from current feature / boundary | Probable |
| Deep nesting or god function with clear seams | Probable |
| Dependency direction wrong for the package boundary | Verified when imports prove it |
| Extract shared platform package | Out of scope unless the repo already owns that audit |
| Rewrite for taste / hypothetical future | Skip |

Rank critical / high / medium / low. Prefer local extractions over package
redesign.

### 4. Apply

Preserve public inputs, outputs, errors, side-effect order, state ownership,
cancellation, cleanup, and externally observed identities. If no clear
structural candidate exists, make no structural edit and say so.

Follow the language section(s) below for the files in scope.

### 5. Validate

Run focused checks after risky batches, then the owning suite or repository
gate. Do not claim success from linting or import checks alone.

## Python mechanics

- Refactor around responsibilities and ownership, not arbitrary line counts.
- Separate parsing, validation, transformation, I/O, persistence,
  orchestration, and presentation when they change for different reasons.
- Prefer explicit inputs, outputs, and dependencies over hidden mutation.
- Preserve exception semantics, logging context, side-effect order,
  transaction ownership, and cleanup.
- Preserve async, generator, context-manager, cancellation, signal, and
  subprocess behavior.
- Extract one complete responsibility with an intent-revealing name.
- Preserve public signatures, keyword behavior, decorators, and patch targets.
- Split a class when it has multiple reasons to change, not merely many
  methods. Prefer composition for extracted behavior with independent state.
- Create modules around cohesive capabilities; keep imports one-directional.
- Check dynamic imports, plugin discovery, CLI/task registration,
  serialization, persisted identities, and test patch paths.
- Avoid `common.py`, `helpers.py`, and `utils.py` dumping grounds.
- Move one responsibility at a time; keep intermediate states testable.
- Use an AST codemod only for a repetitive, mechanical, tested transformation.

## JavaScript / TypeScript / JSX mechanics

- Refactor around responsibility, state ownership, and lifecycle, not line
  count.
- Prefer explicit parameters, return values, props, and context over mutation
  or hidden module state.
- Preserve errors, loading states, accessibility, event order, and cleanup.
- Preserve producer/consumer payload contracts and public identities.
- Prefer pure functions for parsing, normalization, filtering, and mapping.
- Preserve `null` / `undefined` / empty / zero / false semantics.
- Preserve thrown errors, rejected promises, cancellation, and signal handling.
- Keep sequential work sequential; parallelize only independent operations.
- Split components only around clear presentation or stateful ownership.
- Extract hooks when state and lifecycle form one cohesive capability.
- Keep hook order unconditional; keep effects for external synchronization.
- Preserve Strict Mode behavior, stale-closure semantics, and cleanup for
  requests, subscriptions, timers, listeners, and object URLs.
- Put API calls and response normalization at a clear boundary.
- Avoid broad `utils` / `helpers` / `common` modules and circular imports.
- Do not use regex replacement for syntax-aware changes; AST codemod only when
  mechanical and tested.

## Close-out

Lead with what moved (or “no structural candidates”). List deferred items.
One next action if anything remains.
