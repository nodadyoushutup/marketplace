---
name: global-refactor
description: >-
  Audit and apply behavior-preserving structural refactoring across languages.
  Use for refactor audit, ownership/decomposition cleanup, hygiene Refactor
  Check (phase 3), or when asked to restructure live code without behavior
  change. Dispatches to language skills.
---

# Refactor Audit

Intentional **behavior-preserving** structure work on live code: ownership,
decomposition, naming drift, readable modules. This is the **global Refactor
audit playbook**.

Language mechanics live in:

- `.cursor/skills/global-python-refactor/SKILL.md`
- `.cursor/skills/global-javascript-refactor/SKILL.md`

On repos with per-addon hygiene Stories, this is **phase 3** after Isolation +
Substrate and Deslop — see `.cursor/rules/framework-addon-hygiene-checks.mdc`
when that rule exists. Do **not** use this skill to invent shared platform /
substrate packages; reopen `framework-addon-substrate` (or a follow-up Story).

## When To Use

- User says refactor audit / restructure / ownership cleanup / decomposition.
- Hygiene Story **Refactor Check** (phase 3).
- After Deslop Phase B needs a focused structure pass.
- Clear live-code structure debt in a bounded scope (not a rewrite epic).

Do not use for feature behavior changes, dead-path deletion (that is
`global-deslopify` Phase A), or product→platform extraction (Substrate).

## Audit mode

Default to **audit and fix** for an explicit refactor request. For a review-only
ask, stay **read-only**: inventory candidates and recommended moves; skip edits.

## Scope

Bound to named paths, an addon, or the current change plus direct callers/tests.
Exclude generated, mirrored, vendored, and applied migration files. Do not
absorb unrelated dirty-tree work.

## Workflow

Copy and track:

```
Refactor:
- [ ] 1. Scope (paths / languages)
- [ ] 2. Behavior contract (callers, tests, identities)
- [ ] 3. Inventory structural candidates
- [ ] 4. Apply language skills (audit-and-fix) or report only
- [ ] 5. Validate focused / owner checks
```

### 1. Scope

State paths and languages (Python, JS/TS/JSX, or both). Prefer the smallest
set that contains the ownership problem.

### 2. Behavior contract

Before moving code:

1. Identify callers, tests, public imports/exports, registrations, entrypoints,
   serialization, events, and side effects.
2. Record behavior, errors, ordering, identities, and lifecycle ownership that
   must remain unchanged.
3. Find focused tests or add characterization coverage when behavior is unclear.
4. Use `global-code-investigation` when ownership or reachability is uncertain.

### 3. Inventory

List candidates with confidence:

| Candidate | Confidence guide |
|-----------|------------------|
| Mixed ownership in one module (unrelated responsibilities) | Probable |
| Name drifted from current feature / boundary | Probable |
| Deep nesting or god function with clear seams | Probable |
| Dependency direction wrong for the package boundary | Verified when imports prove it |
| Extract shared platform package | **Out of scope** — Substrate audit |
| Rewrite for taste / hypothetical future | Skip |

Rank critical / high / medium / low. Prefer local extractions over package
redesign during hygiene passes.

### 4. Apply

In audit-and-fix mode:

- Python → follow `global-python-refactor`
- JavaScript / TypeScript / JSX / React → follow `global-javascript-refactor`
- Mixed trees → run both, same scope, one report

Preserve public inputs, outputs, errors, side-effect order, state ownership,
cancellation, cleanup, and externally observed identities. If no clear
structural candidate exists, make no structural edit and say so.

In read-only mode, report recommended moves only.

### 5. Validate

Run focused checks after risky batches, then the owning suite or repository
gate required by local instructions. Re-run isolation/dependency scanners when
boundaries between addons or framework packages moved.

## ADHD close-out

Lead with what moved (or “no structural candidates”). List deferred Suspected
items. One next action if anything remains.
