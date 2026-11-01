---
name: global-writing-for-agents
description: >-
  Author skills, AGENTS.md / CLAUDE.md, and docs agents load by pointer. Use
  when creating or editing skill bodies, skill descriptions, or agent guidance.
  Pair with global-asd-ste100 for unambiguous wording and
  global-policy-evolution when promoting durable policy.
---

# Writing for agents

Write documents that an agent will **run**, not documents a human will skim
once. Skills, standing-order files, and pointer docs all share the same craft.
Packaging differs; the levers do not.

When the document is a **skill**, also read [SKILL-MECHANICS.md](SKILL-MECHANICS.md)
(frontmatter, discovery vs slash-only, routers). Prefer STE-flavored clarity
from `global-asd-ste100`. For supply-chain review before install, use
`global-skill-intake`. For promoting durable policy into a repo, use
`global-policy-evolution`.

## Context pointers

A **pointer** is a short always-loaded line that names out-of-context material
and when to open it. Skill `description:` fields and `AGENTS.md` doc lines are
pointers. The **wording** decides whether the agent loads the target — not how
good the target is. A must-have file behind a vague pointer is a reliability
bug: sharpen the pointer first; only inline if sharpening fails.

Every pointer must:

1. Say what the material is.
2. List the **distinct cases** that should fire it (real branches, not synonym
   soup for one case).

Always-loaded pointers cost every turn. Prune harder than body text:

- Put the trigger word first.
- One trigger per real branch; collapse synonyms.
- Drop identity the body already states.

## Two budgets

| Budget | What it costs | Where it lives |
| --- | --- | --- |
| **Context** | Tokens and attention every turn | Always-loaded files and descriptions |
| **Human index** | The operator remembering what exists | Slash-only skills, undocumented docs |

Material behind a pointer escapes context cost except for the pointer line.
Material with no pointer at all lives only in the human’s head — fine when
that is intentional.

## Information hierarchy

Documents mix **steps** (ordered actions) and **reference** (rules/facts
consulted on demand). Rank each piece by how soon the agent needs it:

1. **In-file steps** — primary path, in order.
2. **In-file reference** — peers under one heading (flat rule sets are fine).
3. **Disclosed reference** — sibling or external file, loaded only when a
   pointer fires.

Push too little down → the top bloats. Push too much → the agent misses what
it needs on every run.

**Progressive disclosure** is moving material down that ladder so the top stays
runnable. Branch test: keep what every path needs inline; hide what only some
paths need.

**Co-location:** once a piece has a rung, keep its definition, rules, and
caveats under one heading. Scattering one idea across the file is not the same
as intentional duplication — it is fragmentation.

**Sprawl:** the file is simply too long even when every line is live. Cure:
disclose reference, split by branch or sequence, delete sediment.

## Steps need done-checks

Every step ends on a **completion check** the agent can evaluate.

- **Clear?** Vague (“understand the system”) invites quitting early. Sharpen
  the bound before you hide later steps.
- **Demanding?** “Every modified model accounted for” forces dig work that
  “produce a list” does not. Exhaustiveness can bind a flat rule set too
  (“every rule applied”).

Strong checks are both observable and exhaustive.

## When to split a document

Split only when the cut earns a budget trade:

- **By sequence** — later steps tempt the agent to rush the current one; keep
  the later work out of view across a real boundary (handoff / subagent), not
  a fake inline “part 2”.
- **By discovery** — skill-specific; see [SKILL-MECHANICS.md](SKILL-MECHANICS.md).

## Anchor words

An **anchor word** is a short pretrained concept the model already knows
(_tracer_, _red_, _tight_, _lesson_). Repeat the token; do not restate the
essay. Prefer an existing word over a coined one — coining costs definition
tokens and recruits no priors.

Use anchors in the body (same behavior every time the word appears) and in
pointers (shared language across prompts/docs/code makes discovery reliable).

Collapse restatements into anchors when you can:

- “fast, deterministic, low-overhead” → _tight_
- “a loop you trust on the bug” → _red_

**Prefer positives over bans.** “Don’t think of an elephant” loads the
elephant. State the target behavior (“write one-line comments”). Keep a
prohibition only as a hard guardrail you cannot phrase positively — and pair
it with the positive target.

## Prune relentlessly

- **One source of truth** per meaning. Duplicate meanings inflate rank and
  rot. (Repeating an *anchor token* is intentional; repeating the essay is not.)
- Treat the **environment** as truth too (`package.json`, layout, `--help`).
  Docs that restate easy lookups are stale caches. Cache only what looking up
  cannot give: unwritten convention, why, gotchas.
- Delete lines that no longer bear on the task, or that never did.
- Delete **no-ops**: instructions the model already follows by default. Test by
  behavior change, not by debate. Whole sentence out — do not nibble adjectives.
