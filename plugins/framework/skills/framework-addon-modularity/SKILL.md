---
name: framework-addon-modularity
description: >-
  Audits and fixes addon modularity and removability across framework/addons
  and addons — depends vs optional_depends, deferred guarded optional imports,
  reverse edges, and cascade closures. Use for modularity audit, removability,
  cross-addon hygiene, “can I remove addon X”, or when changing manifests or
  cross-addon Python imports. Scope one addon name or all addons. For Isolation
  or Substrate hygiene phases, use framework-addon-isolation /
  framework-addon-substrate.
---

# Addon Modularity Audit

Intentional review of cross-addon boundaries. Keep addons removable: deleting addon `X` from disk must only require removing `X`’s reverse **required** dependents—not random import breakage. Prefer `optional_depends` when a soft edge is honest; escalate to hard `depends` only for intrinsically required peers (often substrate/`system`/`auth`). The same prefer-optional rule of thumb applies among base framework addons.

Invariants live in `framework-addon-structure`,
`framework-addon-hygiene-checks`, and
`docs/sphinx/source/addons.md`. This skill is the review playbook.

## When To Use

- User says modularity review / removability / cross-addon hygiene / “can I remove X”.
- Editing `__manifest__.py` `depends` / `optional_depends`, or adding imports of `addons.*` / `framework.addons.*`.
- After consolidating or splitting product addons.
- **Renaming an addon** (`addons/<old>` → `addons/<new>`): after code moves,
  run `python3 scripts/addon/check_addon_rename_cutover.py --from <old> --to <new>`
  (optional `--apply`). Deslop/isolation do not cover live DB/S3 identity —
  this script is the rename done-gate. Details in
  `framework-addon-data-lifecycle`.

For Isolation or Substrate hygiene phases, use
`framework-addon-isolation` and `framework-addon-substrate` instead (combined
as one phase on hygiene Stories).

Do not use this skill for ordinary feature work inside a single addon with no new cross-addon edges.

## Addon-dev posture

Custom-addon sessions keep edits in `addons/<name>/` by default. Framework and
`framework/addons/` changes are exceptional: only when a generic contract must
land in the substrate, and the handoff must state what changed and why an
in-addon fix was insufficient. Intentional base-framework sessions may edit
those trees normally, still without naming any custom addon. Isolation
authority: `framework-custom-addon-isolation`.

## Audit mode

Default to **audit and fix** for an explicit change request: complete the full
workflow and apply Verified and Probable fixes. For a review, audit, or
removability question, stay **read-only**: complete inventory and removability,
report findings, and skip Clean. Running the dependency checker and focused
read-only tests is allowed in either mode.

## Scope

| Scope | Meaning |
|-------|---------|
| `all` | Every addon under `framework/addons/` and `addons/` |
| `<name>` | That addon plus its direct edges (imports it makes and imports of it) |

Never propose removing `system` (substrate). `auth` may hard-depend on `system` helpers.

## Removability (cascade is intentional)

Removing addon `X` is valid only when every addon that **hard-depends** on `X`
is also absent. For example, removing an invented `example_platform` addon also
removes `example_feature` when the latter declares it in `depends`. That is
correct—not a modularity bug. Optional dependents may remain if they use
deferred guarded bridges.

Before claiming “remove X and the app still works,” compute the reverse required closure with `required_dependents(name, infos)` from `framework/runtimes/api/app/registry/dependency_audit.py`. There is no hardcoded list of supported addon sets: every install closure and every single-addon removal is derived from the manifests on disk by `framework/addons/system/api/tests/test_addon_removability.py`, so an addon shipped from outside this repository is covered too.

## Workflow

Copy and track:

```
Addon modularity:
- [ ] 1. Scope (all | <name>)
- [ ] 2. Baseline: python scripts/addon/check_addon_dependencies.py
- [ ] 3. Inventory findings (Verified / Probable / Suspected)
- [ ] 4. Isolation / Substrate handoff (if hygiene Story — use those skills)
- [ ] 5. Clean Verified + Probable
- [ ] 6. Removability: reverse required closure
- [ ] 7. Validate checker + focused removability/audit tests
```

### 1. Scope

State `all` or the addon name. For one addon, still run the full-tree checker (edges are global) but focus inventory narrative on that addon.

### 2. Baseline

```bash
python scripts/addon/check_addon_dependencies.py
```

This audits undeclared hard imports, top-level optional imports, reverse dependencies, and manifest overlap. Exit non-zero = Verified findings.

### 3. Inventory

For each finding record ID, path:line, what, confidence, fix.

Rank findings as critical, high, medium, or low. Include impact and confidence
(Verified / Probable / Suspected), cite exact files and lines, and recommend the
smallest fix and validation command.

Hunt:

| Smell | Confidence guide | Fix |
|-------|------------------|-----|
| Import of addon Y without Y in direct `depends` | Verified | Add to `depends` or remove import |
| Top-level import of an `optional_depends` target | Verified | Defer behind guard; prefer `optional_<name>.py` bridge |
| Provider imports consumer that depends on it | Verified | Move code to consumer or shared substrate |
| Same name in `depends` and `optional_depends` | Verified | Keep one |
| Optional use without unavailable path | Probable | Guard + soft-fail message / skip |
| Test in provider imports consumer package | Verified | Move assertion to consumer tests |
| File under `framework/` or `framework/addons/` imports `addons.<product>` or `@addons/<product>` | Verified | Move it into that addon (`api/tests`, `gui/tests`, `mcp/tests`) — or run `framework-addon-isolation` |
| Glue-worthy optional surface sprawl | Suspected | Prefer glue addon; do not auto-merge |

**Canonical optional bridge pattern:** deferred `from addons.<name>…` after an
availability check, with explicit unavailable behavior. Optional bridges belong
under the consumer addon, while hard dependencies use required bridges or
normal imports and must be listed in `depends`; do not prefix required bridge
modules with `optional_`.

### 4. Isolation / Substrate handoff

If this pass is part of a hygiene Story, run
`framework-addon-isolation` and
`framework-addon-substrate` as the combined phase
(one report). Do not duplicate those checklists here. Cache Leverage Check
stays with Substrate / cache contracts.

### 5. Clean

In audit-and-fix mode, apply Verified and Probable fixes. In read-only mode,
skip this step and report the recommended fixes. Leave Suspected findings
listed in either mode. Do not invent new glue addons unless the user expands
scope.

Update Sphinx `autoapimodule` stubs only when deleting modules. Ignore `.framework-addons` mirrors when counting imports.

### 6. Removability check

For target `X` (or each custom addon when scope is `all`):

1. Compute the reverse required closure with `required_dependents(X, discover_addon_manifest_infos())` — everything listed goes when X goes.
2. Confirm nothing outside that closure references X: the checker covers framework-tree imports and name literals, but a sibling product addon may still import X without declaring it.
3. Run `framework/addons/system/api/tests/test_addon_removability.py` and `test_addon_dependency_audit.py` (API container if host lacks addon deps).

### 7. Validate

- Re-run `python scripts/addon/check_addon_dependencies.py` (must pass).
- Focused removability/audit pytest.
- When optional bridges changed: soft-fail tests under the consumer addon.

## ADHD close-out

Lead with checker pass/fail and severity-ranked findings. Follow with reverse
closures, Suspected leftovers, and a concise removability verdict. In
audit-and-fix mode, state which closures were cleaned. Give one next action if
anything remains.
