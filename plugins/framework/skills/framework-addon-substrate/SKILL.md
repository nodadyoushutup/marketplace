---
name: framework-addon-substrate
description: >-
  Audits whether shared addon capability should become or extend a base
  framework/addons substrate. Use for Substrate Check, “should this be a base
  addon”, Extraction candidates, or Isolation + Substrate hygiene phase. Scope
  one addon name, a peer set, or all addons.
---

# Addon Substrate Audit

Intentional review: has this addon (or its peers) accumulated enough
**generic** capability that it belongs in `framework/addons/` as always-there
platform capacity?

Invariants live in `framework-addon-hygiene-checks`,
`framework-addon-structure`, and
`framework-cache-contracts`. This skill is the review
playbook.

On full per-addon hygiene Stories, Isolation and Substrate are **one combined
phase** — run `framework-addon-isolation` first (or in parallel inventory), then
this skill, **one report**. Alone, this skill is a focused extraction /
platform-boundary pass.

This is **not** local helper cleanup (that is Refactor) and **not** dead-path
deletion (that is Deslop).

## When To Use

- User says substrate check / “should this be a base addon” / extract to
  `framework/addons/`.
- Per-addon hygiene **Isolation + Substrate** phase (pair with isolation).
- After noticing the same agnostic pattern in two or more addons.
- When creating a new addon or heavily reworking expensive shared reads
  (include Cache Leverage Check).

Do not use for product-domain logic that only one custom addon needs — keep
that under `addons/<name>/`.

## Audit mode

Default to **audit and fix** only when the user asked to extract/implement.
For a review / “should we extract” question, stay **read-only**: record
candidates and gates; do not start a large extraction unless authorized.

## Scope

| Scope | Meaning |
|-------|---------|
| `<name>` | That addon plus peers that share its patterns |
| `peers` | Explicit set of addon names the user named |
| `all` | Broad scan of `framework/addons/` and ignored `addons/` for duplicated agnostic capability |

## Workflow

Copy and track:

```
Addon substrate:
- [ ] 1. Scope (<name> | peers | all)
- [ ] 2. Isolation precondition (or combined pass)
- [ ] 3. Candidate inventory
- [ ] 4. Gate each candidate (all four must pass)
- [ ] 5. Cache Leverage Check (when applicable)
- [ ] 6. Extract / extend / defer (audit-and-fix only)
- [ ] 7. Validate manifests, isolation, focused tests
```

### 1. Scope

State the addon(s). Compare at least one peer when looking for multi-consumer
leverage.

### 2. Isolation precondition

Do not extract product purpose into substrate. If isolation findings remain in
scope, fix or list them first via
`framework-addon-isolation`. New substrate must pass
the empty-`addons/` stranger test.

### 3. Candidate inventory

List concrete candidates: modules, contracts, UI primitives, shared services.
For each: current owners, approximate size/surface, known consumers.

### 4. Gates (all required)

| Gate | Pass means |
|------|------------|
| Material volume | Enough logic/contracts/primitives for an honest addon boundary |
| Multi-consumer leverage | ≥2 current consumers, or clear future reach across custom addons |
| Agnostic bar | Not product-tied; empty-`addons/` stranger still wants it |
| Platform worth | Belongs in `framework/addons/`, not private glue under `addons/` |

- **Extract / extend** only when all gates pass. Consumers may gain honest hard
  `depends` when the peer is intrinsically required; keep `optional_depends`
  for soft enhancements.
- **Do not extract** for aesthetics, single-caller helpers, or product-domain
  logic.
- Large warranted extractions may be a follow-up Story — record the candidate;
  do not silently drop it.

### 5. Cache Leverage Check

When the scoped work is a new addon or substantial expensive shared reads,
decide cache vs skip vs follow-up per
`framework-cache-contracts`. Note the decision in the
report. Skip trivial edits. This is not a separate hygiene phase.

### 6. Extract / extend

In audit-and-fix mode only:

1. Prefer extending an existing base addon when the capability fits.
2. Otherwise create `framework/addons/<new>/` with honest manifest/entrypoints.
3. Move agnostic code only; leave product vocabulary in owning `addons/<name>/`.
4. Update consumer `depends` / `optional_depends` and deferred bridges.
5. Re-run isolation + dependency scanners.

### 7. Validate

```bash
python3 scripts/addon/check_addon_isolation.py
.venv/bin/python scripts/addon/check_addon_dependencies.py
```

Focused owner tests for the new/extended substrate and updated consumers.

## ADHD close-out

Lead with candidates and gate pass/fail. State extract / defer / skip for each.
Note Cache Leverage decision when it ran. One next action (follow-up Story,
consumer hard-depends train, or Deslop phase).
