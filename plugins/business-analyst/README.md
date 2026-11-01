# business-analyst

Product and planning craft: business analysis, executable plans, and external
research. Pair with **`global`** (posture) and **`code`** (implementation).

No product, host, or site layout belongs in this plugin.

## Rules

| Rule | Purpose |
| --- | --- |
| `business-analyst-brief` | Brief sections and the testable-requirement bar |
| `business-analyst-when` | When to skip analysis and when to plan |
| `business-analyst-research` | Gate before searching outside the repo |

## Skills

| Skill | Purpose |
| --- | --- |
| `business-analyst` | Brief playbook and routing |
| `business-analyst-planner` | Lock an executable plan |
| `business-analyst-researcher` | Cited external evidence |

## Agents

| Agent | Purpose |
| --- | --- |
| `business-analyst` | Shape problem, requirements, acceptance criteria |
| `business-analyst-planner` | Interview and lock the plan |
| `business-analyst-researcher` | External evidence outside the repo |

## Commands

- `/business-analyst` → `business-analyst`
- `/business-analyst-plan` → `business-analyst-planner` (repository read, and `business-analyst-researcher` only for an external unknown)

## Diagrams

- [`docs/business-analyst-workflow.drawio`](docs/business-analyst-workflow.drawio) — gate → brief → planner/researcher → implementation handoff
- [`docs/business-analyst-workflow.png`](docs/business-analyst-workflow.png) — same map, black background
