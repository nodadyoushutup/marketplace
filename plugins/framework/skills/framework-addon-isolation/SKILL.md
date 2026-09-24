---
name: framework-addon-isolation
description: >-
  Audits and fixes custom-addon isolation — stranger-safe boundaries, reverse
  edges, purpose leakage, and empty-addons/ test honesty. Use for isolation
  audit, “does framework know about this product”, Isolation hygiene phase, or
  when framework/base trees may have absorbed product identity. Scope one
  addon name, framework substrate, or all addons.
---

# Addon Isolation Audit

Intentional review of the one-way boundary: custom addons may consume
framework; tracked framework and base addons must never identify a custom
addon by name **or purpose**.

Invariants live in `framework-custom-addon-isolation` and
`framework-addon-hygiene-checks`. This skill is the review
playbook.

On full per-addon hygiene Stories, Isolation and Substrate are **one combined
phase** — run this skill and `framework-addon-substrate` together, one report.
Alone, this skill is a focused isolation pass.

## When To Use

- User says isolation audit / stranger test / reverse edge / purpose leakage.
- Per-addon hygiene **Isolation + Substrate** phase (pair with substrate).
- After product work that touched `framework/`, `scripts/`, `applications/`,
  hand-authored docs, or `.cursor` policy.
- Before committing framework test or policy edits in a workspace that has
  ignored `addons/` checkouts.

Do not use for ordinary feature work that stays entirely under `addons/<name>/`
with no substrate edits.

## Audit mode

Default to **audit and fix** for an explicit change request. For a review /
audit question, stay **read-only**: inventory and report; skip Clean.

## Scope

| Scope | Meaning |
|-------|---------|
| `<name>` | That custom or base addon plus any substrate surfaces it may have leaked into |
| `framework` | Tracked framework / `framework/addons/` / scripts / docs / policy only |
| `all` | Every addon under `framework/addons/` and ignored `addons/` |

## Workflow

Copy and track:

```
Addon isolation:
- [ ] 1. Scope (<name> | framework | all)
- [ ] 2. Baseline scanners
- [ ] 3. Inventory (Verified / Probable / Suspected)
- [ ] 4. Stranger test (empty-addons/ judgment)
- [ ] 5. Clean Verified + Probable (audit-and-fix)
- [ ] 6. Validate scanners + focused tests
```

### 1. Scope

State the scope. Prefer naming one product addon when the ask is about that
addon; use `framework` when hunting substrate pollution without a named product
target (still use invented vocabulary only in reports written into tracked
files).

### 2. Baseline scanners

```bash
python3 scripts/addon/check_addon_isolation.py
.venv/bin/python scripts/addon/check_addon_dependencies.py
```

Isolation scanner catches structural identity (paths, imports, local package
name literals when checkouts exist). Dependency checker catches reverse
imports and undeclared edges. Exit non-zero = Verified findings. Neither
scanner is a purpose denylist — purpose leakage is agent judgment.

### 3. Inventory

For each finding: ID, path:line, what, confidence, smallest fix.

Hunt:

| Smell | Confidence | Fix |
|-------|------------|-----|
| Tracked file imports `addons.<product>` or `@addons/<product>` | Verified | Move into owning addon (incl. its tests) |
| Tracked path/string/comment/doc names a custom addon | Verified | Discover generically, invent `example_*`, or move into the addon |
| Identifier/API purpose only makes sense for one product addon | Verified | Generic contract or move into owning addon |
| Framework/runtime test motivates a product feature (even with `example.*` names) | Verified | Move proof under `addons/<name>/` |
| Reject-path fixtures that deny-list real providers/hosts | Verified | Invented fake values or allowlist-positive only |
| Product vocabulary denylist in a tracked scanner/rule/doc | Verified | Delete denylist; keep structural checks only |
| Base addon hardcodes another **custom** addon | Verified | Remove; optional bridges live in consumer trees |
| Declared necessary base↔base edge | Not a smell | Leave |

### 4. Stranger test

Ask: if every ignored `addons/` checkout disappeared, would a stranger reading
tracked framework (including tests) still learn that a product addon exists —
by name **or** intent?

Fail → Verified isolation defect. Pass scanners alone is not enough.

### 5. Clean

In audit-and-fix mode, apply Verified and Probable fixes. Leave Suspected
listed. Do not invent product-vocab denylists. Do not “prove” product behavior
in substrate tests.

When the ask is a full hygiene phase, continue with
`framework-addon-substrate` in the same report.

### 6. Validate

- Re-run both scanners (must pass).
- Focused owner tests for moved/rewritten surfaces.
- Stop-hook owner tests cover touched files under the open root.

## ADHD close-out

Lead with scanner pass/fail and severity-ranked findings. State stranger-test
verdict. In audit-and-fix mode, list what moved where. One next action if
anything remains (often: Substrate pass, or product-side follow-up under
`addons/<name>/`).
