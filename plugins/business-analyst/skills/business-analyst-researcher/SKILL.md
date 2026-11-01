---
name: business-analyst-researcher
description: >-
  Find cited evidence for an external unknown during planning. Use with
  business-analyst-planner when a library, API, or tool contract is not in
  the repo. Do not use for questions the codebase already answers.
---

# Researcher

## Gate

Follow `business-analyst-research` before any search. If the repo can answer
the question, stop and read the repository instead of searching outside it.

## Load map

| Role | Owns |
| --- | --- |
| `business-analyst-planner` | Whether this answer changes scope |
| Repository read | How this repo is put together |
| This skill | Sources outside the repo |

## Defaults

- One primary source beats three blogs.
- A disputed fact stays disputed.
- Recommend the reversible option when two current docs disagree.
- Do not implement the product from the research.

## Procedure

1. Write the question, the version or product constraint, and what decision
   it unblocks. **Done when** a searcher could not confuse it with a repo
   question.
2. Search primary sources first: official docs, release notes, the project's
   own changelog or source. **Done when** you have a candidate answer or you
   have confirmed the primary source does not cover it.
3. Use secondary sources only as leads. Confirm anything the plan will depend
   on. **Done when** each load-bearing claim has a primary citation or is
   marked unknown.
4. Check deprecation and security notes for the version the plan would pin.
   **Done when** you either found a constraint or recorded that you looked.
5. Return the packet below. **Done when** the planner can accept, reject, or
   default the recommendation without opening the sources.

## Return packet

1. **Answer** — the recommendation in one short paragraph.
2. **Known / disputed / unknown** — three explicit lists. Empty lists are
   written as "none".
3. **Sources** — title and URL for each load-bearing claim.
4. **Caveats** — version, license, or deprecation limits.
5. **Implication** — one change to the plan, or "no plan change".

Do not paste credentials, private payloads, or long verbatim copyrighted text.
Summarize and cite.
