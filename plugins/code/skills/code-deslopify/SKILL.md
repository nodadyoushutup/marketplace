---
name: code-deslopify
description: >-
  Audit and clean hygiene residue — dead paths, shims, duplication, and test
  permanence. Use for deslop audit, dead-path cleanup, compatibility-shim
  removal, test-residue cleanup, hygiene phase 2, or after sprawling
  multi-file work.
---

# Deslopify Audit

Intentional cleanup of verified dead, obsolete, duplicated, or accidental
complexity. This is the **global Deslop audit playbook**.

On repos with per-addon hygiene Stories, Deslop is **phase 2** after Isolation
+ Substrate — see `.cursor/rules/framework-addon-hygiene-checks.mdc` when that
rule exists. Do not invent new shared platform/substrate packages here; that
belongs in the Substrate audit (`framework-addon-substrate` in this repo).

Keep three phases separate:

| Phase | Purpose |
|---|---|
| A — Hygiene | Remove verified dead, obsolete, duplicated, or accidental complexity |
| B — Structure | Hand off live-code structure to `code-refactor` (language skills) |
| C — Test review | Delete one-offs, promote durable contracts, and fill clear gaps |

Phase A does not redesign live code. Phase B does not delete uncertain behavior.
Phase C does not start a coverage campaign.

## When To Use

- User says deslop / dead path / shim cleanup / hygiene garbage / test residue.
- After a large plan, new subsystem, hard cut, sprawling multi-file change, or
  AI-heavy implementation that introduced many helpers, wrappers, or tests.
- Hygiene Story phase 2 (after Isolation + Substrate report).

Skip for small focused edits, read-only work, or user-constrained scope.
An explicit deslop request runs all three phases unless the user names only one.

## Audit mode

Default to **audit and fix** for an explicit deslop request. For a review-only
ask, stay **read-only**: inventory Verified / Probable / Suspected; skip deletes
and structural edits.

## Scope

Use files touched by the current change plus only direct producers, callers,
registrations, and tests needed to establish confidence. Exclude generated,
mirrored, vendored, and applied migration files. Preserve unrelated work.

Before calling code dead, check dynamic imports, string registration, public
exports, configuration, entrypoints, scripts, tests, persisted identities, and
external consumers. Use `code-investigation` when reachability is
uncertain.

Classify every hygiene candidate:

- **Verified:** direct evidence proves the path is unused or unreachable.
- **Probable:** multiple signals support removal and no live contract was found.
- **Suspected:** an unresolved external or dynamic contract remains; report it
  and do not delete it automatically.

## Workflow

Copy and track:

```
Deslop:
- [ ] 1. Scope (touched paths / languages)
- [ ] 2. Phase A — Hygiene inventory (+ deletes in audit-and-fix)
- [ ] 3. Phase B — Structure via code-refactor (live code only)
- [ ] 4. Phase C — Test review
- [ ] 5. Validate focused / owner checks
```

1. Define the touched scope and languages.
2. Read [patterns.md](patterns.md), inventory hygiene findings, and rank safe
   deletes before compatibility paths, incomplete wiring, and duplication.
3. In audit-and-fix mode, remove Verified and Probable findings with the
   smallest deletion or inline. Keep one canonical current contract; do not add
   aliases or fallback paths. In read-only mode, report only.
4. For Phase B, follow `.cursor/skills/code-refactor/SKILL.md` (Python and
   JS/TS mechanics live in that skill). If none apply, record that and continue.
5. Read [test-review.md](test-review.md), classify touched and owning tests as
   Delete, Promote, Keep, or Gap-fill, and apply the durable disposition in
   audit-and-fix mode.
6. Run focused checks after risky batches, then the owning suite or repository
   gate required by local instructions.

## Phase A rules

- Prefer deletion and inlining over new abstraction.
- Remove both a dead symbol and tests, fixtures, exports, and documentation that
  exist only for it.
- Remove dual-path reads only after proving producers emit one canonical shape.
- Do not swallow errors or convert failure into misleading success.
- Do not collapse similar implementations until their contracts and error
  semantics are proven equivalent.
- Do not edit generated outputs; edit their source or generator when in scope.
- **Reverse custom-addon identity (Verified, this repository):** tracked
  framework and base-addon trees must not acknowledge a specific custom addon.
  Hunt imports, path/string literals, comments, fixtures, **and** identifiers
  whose name or purpose only make sense for one product addon. Also hunt
  framework/runtime tests whose motivating scenario is a custom-addon feature —
  invented `example.*` names do not clear that smell; move those tests into
  `addons/<name>/`. See `.cursor/rules/framework-custom-addon-isolation.mdc`.
  Base-addon → base-addon edges that are declared and necessary are not this
  smell.

## Phase B rules

- Restructure live logic around responsibility, ownership, and lifecycle via
  `code-refactor`.
- Preserve public inputs, outputs, errors, side-effect order, state ownership,
  cancellation, cleanup, and externally observed identities.
- Prefer local extractions over package redesign during automatic cleanup.
- Do not manufacture a refactor merely to complete the phase.
- Do not invent shared platform packages here (Substrate audit owns that).

## Phase C rules

- Review tests added or edited in the change and owning tests for the feature.
- Delete source-substring archaeology, import-only checks, duplicates,
  placeholders, and residue for removed behavior.
- Promote useful session checks into stable public-boundary regression tests.
- Gap-fill only clear contract holes, using existing isolation and fixtures.
- Do not preserve live-credential probes, production calls, or transient
  runtime-state assumptions as unit tests.

## ADHD close-out

Lead with Phase A removals, Phase B structural moves or none, Phase C
deletes/promotions/gaps or “suite already permanent,” exact verification, and
Suspected leftovers. Never invent work to justify a phase. One next action if
anything remains (often: `code-refactor` hygiene phase 3, or stop).
