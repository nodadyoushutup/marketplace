# business-analyst

Always-on product and planning craft: stay-out gate, build-ready briefs,
product-sequence plans, and external research. While this plugin is installed,
`business-analyst-baseline` applies on every turn. Pair with **`global`**
(posture) and **`code`** (implementation / `code-technical-lead`).

No product, host, or site layout belongs in this plugin.

## Rules

| Rule | Purpose |
| --- | --- |
| `business-analyst-baseline` | Always-on stay-out / write-brief gate |
| `business-analyst-brief` | Brief sections and the testable-requirement bar |
| `business-analyst-when` | When to skip analysis and when to plan |
| `business-analyst-research` | Gate before searching outside the repo |

## Skills

| Skill | Purpose |
| --- | --- |
| `business-analyst` | Brief playbook and routing |
| `business-analyst-planner` | Lock a product-sequence plan |
| `business-analyst-researcher` | Cited external evidence |

## Agents

| Agent | Purpose |
| --- | --- |
| `business-analyst` | Shape problem, requirements, acceptance criteria |
| `business-analyst-planner` | Lock product sequence (not technical approach) |
| `business-analyst-researcher` | External evidence outside the repo |

## Commands

- `/business-analyst` → `business-analyst`
- `/business-analyst-plan` → `business-analyst-planner` (and `business-analyst-researcher` only for an external unknown)

## Diagrams

- [`docs/business-analyst-workflow.drawio`](docs/business-analyst-workflow.drawio) — gate → brief → planner/researcher → `code-technical-lead` → `code-workflow`
- [`docs/business-analyst-workflow.png`](docs/business-analyst-workflow.png) — same map, black background

## Defaults

- Stay out of already-scoped work; implement without a brief.
- At most one blocker question; everything else is a marked assumption.
- Technical approach and touch map → `code-technical-lead`.
- Ticket/page filing → `atlassian`. Chat paste hygiene → `global-pasted-secrets`.
