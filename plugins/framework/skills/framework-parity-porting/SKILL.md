---
name: framework-parity-porting
description: >-
  Assess and port a foreign application codebase into custom addons with
  parity planning. Use when the operator points at an external repo, directory,
  or path and asks to assess, plan, port, or achieve parity in this framework.
  Not for ordinary in-repo features or explain-only reviews.
---

# Parity / porting (foreign code → custom addons)

Orchestrate bringing foreign application code into this framework as custom
addons under `addons/<name>/`. This skill owns the pipeline only. It does
**not** replace isolation, substrate, hygiene, GUI, coding, or verification
playbooks — call those skills by name.

Invariants live in `framework-parity-porting`.

## Trigger (both required)

Activate only when **both** are true:

1. The operator points at foreign code (repo URL, clone path, directory, or
   attached tree **outside** ordinary in-checkout feature work).
2. The operator asks to **assess**, **plan**, **port**, or achieve **parity**
   into this framework.

### Non-triggers (do not start Assess→Port)

- “Look at / explain / review this code” with no port or parity ask
- Ordinary in-repo feature, bug, or hygiene work
- Pointing at `addons/<name>/` already in this workspace without a foreign
  source port ask

## Port shapes

Record exactly one shape in Assess:

| Shape | Meaning |
| --- | --- |
| `full-app` | Bring the whole app into one or more custom addons |
| `feature-island` | Bring only selected capabilities from a larger legacy system |

Do not assume only one shape. Scope the parity matrix to the recorded shape.

## Parity rank (highest first)

1. **capability** — user-visible features (can the user do X)
2. **behavior-API** — contracts and behavior those features need
3. **GUI-flow** — interaction and navigation flow

Visual look is not acceptance unless the operator explicitly raises it for a
matrix row. Pixel-perfect UI clone is never required by default.

## Phase gates

```
Assess → Plan (parity matrix on Jira) → STOP for operator go → Port slices → Verify
```

**Trigger vs proceed:** First-turn words like `port` / `port this` / `parity`
only start Assess→Plan. They do **not** authorize implementation.

Proceed language applies **only after** the Plan Jira comment exists (or the
Plan is already present and this turn’s execute paste authorizes implement).
Proceed examples: `go`, `proceed`, `implement`, `port it` (post-Plan only).

Until proceed:

- Do not create `addons/<name>/` dirs or remotes
- Do not implement port code or commits
- Assess/Plan and the Jira plan comment are allowed

Exception: same-turn `/code-execute-jira <KEY>` when the Plan comment
already exists on a port Story after Plan.

## Hard refuses

- Edit the foreign tree unless the operator explicitly asks
- Copy secrets, credentials, tokens, or production dumps (invent fixtures)
- Put product identity or purpose into tracked framework / base-addon tests
- Hide non-trivial substrate extracts inside the product port (file a separate
  framework Story)
- Start a full port from explain-only language

## Call existing skills (do not copy their checklists)

| Concern | Skill / rule |
| --- | --- |
| Isolation / stranger test | `framework-addon-isolation` |
| Substrate extract vs addon-local | `framework-addon-substrate` |
| Hygiene phase order | `framework-addon-hygiene-checks`, then `framework-addon-modularity`, `code-deslop`, `code-refactor` as needed |
| GUI appearance / page patterns | `framework-gui-appearance`, `framework-gui-page-patterns` |
| Implementation workflow | `code-workflow` |
| Done claims | `code-verification-before-completion` |
| GUI dogfood | `browser-automation` |

## Workflow

Copy and track:

```
Parity / porting:
- [ ] 1. Confirm trigger + port shape
- [ ] 2. Assess (read-only foreign source)
- [ ] 3. Publish Plan (parity matrix Jira comment)
- [ ] 4. STOP until operator go (+ confirm addon names)
- [ ] 5. Port vertical slices (call isolation/substrate/GUI skills)
- [ ] 6. Verify by parity rank
```

### 1. Confirm trigger + shape

State the foreign root path/URL and `full-app` or `feature-island`. If shape is
unclear, default to `feature-island` when the operator named selected
capabilities; otherwise `full-app`, and record the assumption.

### 2. Assess (foreign source read-only)

Inventory and map to framework concepts:

- Proposed custom addon split and names (operator must confirm before create)
- Isolation boundaries (stranger test) — call isolation skill for the method
- Substrate vs addon-local candidates — call substrate skill for the method
- Runtime entrypoints, data lifecycle
- **Do-not-port map:** source auth, Docker, CI, config, routing, storage →
  framework equivalents (port behavior; do not copy their substrate)
- GUI surface inventory

**Pattern conflict default:** adapt to framework norms. If the source pattern
is clearly better and reusable across apps, propose substrate (separate Story
when non-trivial). If product-specific, keep it in the addon. Record the
choice on affected matrix rows.

Optional: launch `framework-parity-assessor` for a read-only Assess/Plan draft.

### 3. Plan artifact — parity matrix

Publish as a **Jira comment** on the work issue before port coding. After
`addons/<name>/` exists, an optional copy under that addon is allowed.

Each row **must** include:

| Column | Values |
| --- | --- |
| Source capability | Short name of what the source does |
| Parity rank | `capability` / `behavior-API` / `GUI-flow` |
| Target | `addon` / `substrate` / `drop` / `defer` |
| Owning addon | `addons/<name>/` when target is `addon` |
| GUI strategy | `base` or `addon-variant` + reason |
| Verify method | `test` / `browser` / `both` |
| Verify note | Short how-to-verify (command, UI path, or browser checklist). Required when verify method is `browser` or `both`; recommended for `test` |

Also include in the same comment: port shape, do-not-port map, proposed addon
names/split. Screenshots are optional evidence. Pixel-perfect UI is not AC.

### 4. Operator go + name confirm

Stop after Plan. Wait for proceed language. Confirm addon name(s) before
creating dirs or remotes when proposing a new name or split.

### 5. Port (vertical slices)

For each slice: one user journey end-to-end (API + GUI + tests) before the next.

- Foreign tree stays read-only
- Product code and tests only under `addons/<name>/`
- Tracked framework stays free of product identity and purpose
- Sequence: Isolation + Substrate checks → implement slice → hygiene as needed
- GUI: base components and page patterns first; `addon-variant` only when the
  matrix names unreplicable special behavior
- Non-trivial substrate → separate framework Story; do not smuggle it

### 6. Verify (by parity rank)

For every matrix row marked to port:

1. Prove **capability** first
2. Then **behavior-API** contracts
3. Then **GUI-flow** when in scope (browser dogfood via
   `browser-automation` when verify method needs it)

Require:

- Addon-owned pytest/vitest under the owning addon
- Isolation + substrate hygiene before claiming the slice done
- `code-verification-before-completion` before “done” / “fixed” claims

## Done for a port slice

- Matrix rows for the slice have evidence for their verify methods
- No isolation leakage into tracked framework
- Operator can follow how-to-verify steps on the live checkout
