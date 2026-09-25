# freshservice

Agnostic Freshservice ITSM craft — create gates, ticket body shape, status
honesty. Install when the project uses Freshservice (MCP or API).

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `freshservice-create` | Create-only filing gate |
| `freshservice-ticket` | Description shape |
| `freshservice-status` | Status / priority honesty |

All rules are **agent-requested** (`alwaysApply: false`).

## Skills

| Skill | Purpose |
| --- | --- |
| `freshservice` | Index / gate |

## Commands

- `/freshservice` → ticket craft

## Pairing

- `atlassian` — Jira/Confluence when both trackers are in play
- `business-analyst` — shape vague asks before filing
- `global-mcp-first` — Freshservice MCP before ad-hoc API wrappers

## Diagrams

- [`docs/freshservice-workflow.drawio`](docs/freshservice-workflow.drawio) — gate → act → evidence
