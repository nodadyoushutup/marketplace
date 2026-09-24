---
name: global-python-refactor
description: >-
  Apply behavior-preserving structural Python refactoring to functions, classes,
  modules, and packages. Use for decomposition, ownership cleanup, dependency
  direction, or as the Python structure phase of global-deslopify.
---

# Python Refactor

Repository instructions define style, runtime, and validation conventions. This
skill governs structural changes to live Python.

## Deslop / hygiene phase

Language mechanics for live Python. For an intentional refactor **audit**
(checklist, scope, report), start at `.cursor/skills/global-refactor/SKILL.md`,
which dispatches here.

This is also Phase B of `.cursor/skills/global-deslopify/SKILL.md` and the
**Refactor Check** (phase 3) on per-addon hygiene Stories after Isolation +
Substrate and Deslop. Local structure and naming live here; extracting a new
shared `framework/addons/` substrate is Isolation + Substrate, not this skill —
see `.cursor/rules/framework-addon-hygiene-checks.mdc`.

## Establish the behavior contract

Before moving code:

1. Identify callers, tests, public imports, decorators, registrations,
   entrypoints, serialization, and side effects.
2. Record behavior, errors, ordering, identities, and transaction or lifecycle
   ownership that must remain unchanged.
3. Find focused tests or add characterization coverage when behavior is unclear.
4. Inspect the working tree so unrelated changes are not absorbed.

Use `global-code-investigation` when ownership, runtime wiring, or apparent dead
code is uncertain. Missing textual references do not prove an API is unused.

## Structural principles

- Refactor around responsibilities and ownership, not arbitrary line counts.
- Separate parsing, validation, transformation, I/O, persistence,
  orchestration, and presentation when they change for different reasons.
- Keep orchestration readable at one abstraction level.
- Prefer explicit inputs, outputs, and dependencies over hidden mutation.
- Preserve exception semantics, logging context, side-effect order, transaction
  ownership, and cleanup.
- Preserve async, generator, context-manager, cancellation, signal, and
  subprocess behavior.
- Avoid circular imports, import-time surprises, catch-all helper modules, and
  new dependencies for ordinary refactoring.
- Keep behavior changes separate unless explicitly requested.

## Functions and methods

- Extract one complete responsibility with an intent-revealing name.
- Keep inputs and outputs small and explicit.
- Return meaningful values instead of mutating several outer variables.
- Use early returns only when cleanup and control flow remain clear.
- Preserve public signatures, keyword behavior, decorators, and patch targets.
- Keep validation and external effects at their established boundaries.
- If ordering is unsafe, correct it as a separate tested behavior change.
- Do not replace readable flow with a maze of tiny wrappers.

## Classes and modules

- Split a class when it has multiple reasons to change, not merely many methods.
- Separate pure policy from I/O and persistence.
- Keep state with the object that owns its lifecycle; prefer composition for
  extracted behavior with independent state or dependencies.
- Preserve inheritance, descriptors, dataclass fields, mappings, and discovery
  metadata.
- Create modules around cohesive capabilities or domain concepts.
- Keep imports one-directional and shared contracts near the dependency root.
- Preserve live public import paths when repository compatibility policy
  requires them.
- Check dynamic imports, plugin discovery, CLI and task registration,
  introspection, serialization, persisted identities, and test patch paths.
- Avoid `common.py`, `helpers.py`, and `utils.py` dumping grounds.

## Behavior-contract checklist

Before declaring a move safe, check:

- validation and authorization boundaries
- transaction, flush, commit, rollback, and side-effect order
- public response, message, event, and configuration shapes
- registration, discovery, decorators, entrypoints, and stable identities
- environment and dependency injection ownership
- retry, idempotency, timeout, cancellation, and cleanup semantics
- serialization and persisted module or class references

Import success alone does not prove registration or runtime behavior.

## Workflow and validation

1. Inspect target, callers, tests, and runtime wiring.
2. Record preserved behavior and the proposed responsibility boundary.
3. Choose the smallest useful helper, collaborator, module, or package move.
4. Move one responsibility at a time and keep intermediate states testable.
5. Update imports, tests, documentation, registrations, and patch targets.
6. Review the diff for accidental behavior or public API changes.
7. Run configured compile/import checks, focused tests, lint/type checks, then
   broader registration, startup, or integration checks as risk warrants.

Do not claim success from linting or import checks alone. Use an AST codemod only
for a repetitive, mechanical, tested transformation and remove one-off tooling
unless it has recurring value.

When changing this skill, review [EVALS.md](EVALS.md).
