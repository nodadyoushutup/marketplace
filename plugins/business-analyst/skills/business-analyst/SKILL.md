---
name: business-analyst
description: >-
  Shape problem, outcomes, requirements, and acceptance criteria; route to
  planner or researcher when needed. Use for unclear product asks, story
  shaping, or "what should we build" before implementation. Do not implement.
---

# Business analyst

## Gate

Work is read-only shaping. Do not edit product code, run migrations, or
mutate runtime. Implementation is a later pass. This plugin stops at the
brief or the plan.

Skip this skill when `business-analyst-when` / `business-analyst-baseline`
says the ask is already scoped.

## Load map

| Need | Load |
| --- | --- |
| Always-on stay-out / engage gate | `business-analyst-baseline` |
| Brief sections and the quality bar | `business-analyst-brief` |
| Whether to plan at all | `business-analyst-when` |
| Lock a product sequence | `business-analyst-planner` |
| A fact outside this repo | `business-analyst-research`, then `business-analyst-researcher` |
| Technical approach / touch map | a later technical-approach pass |

## Defaults

- One reversible default beats an open question.
- At most one blocker question. Everything else continues.
- Do not invent a tracker project, board, or assignee.
- Do not name a product the user did not name.
- Stakeholders, priority, non-functionals, and success signal may be `none`
  / `not measured` — write the line explicitly.

## Procedure

1. Restate the ask in one sentence. **Done when** a reader can see who is
   affected.
2. Check `business-analyst-baseline` / `business-analyst-when`. **Done when**
   you either exit to implementation or continue here.
3. Write the brief in `business-analyst-brief` order. **Done when** every
   requirement has a matching check, or you marked the gap as an assumption.
4. If product sequence or acceptance is still unclear, or the user asked for
   a plan this turn, hand off to `business-analyst-planner`. **Done when**
   the planner has a locked plan or you recorded why a plan is unnecessary.
5. Name the next action: lock a plan, name implementation as a later pass,
   or hand off for implementation. **Done when** that action is one sentence.

## Deliverable

Use every section in `business-analyst-brief`. Lead the reply with the
outcome and the requirement count.
