# jira

Agnostic Jira craft for Claude Code and Cursor. Install when the project uses
Jira (Atlassian MCP or equivalent). No project-specific keys or labels.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `jira-create` | When to file; create-only default; epic parent; never invent IDs |
| `jira-description` | Overview + numbered Requirements + matching AC |
| `jira-story` | New work / development |
| `jira-bug` | Defects and maintenance fixes |
| `jira-task` | Non-code / light chores |
| `jira-subtask` | Child slices (explicit ask only) |
| `jira-epic` | Milestone parents (explicit ask only) |
| `jira-status` | Backlog → on deck → In Progress → Done |

All rules are **agent-requested** (`alwaysApply: false`) so cold clones without
Jira do not load them every turn.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `jira` | Index / gate for Claude + explicit entry |

## Commands

- `/jira` → file or shape an issue using the rules above

## Pairing

- `global-execute-first` — create-only wins when the primary verb is file/ticket
- `business-analyst` — shape problem/AC before filing when the ask is fuzzy
- `code-workflow` — implement only after an explicit second verb or a named
  existing issue

## Diagrams

- [`docs/jira-workflow.drawio`](docs/jira-workflow.drawio) — ticketless gate → create-only vs implement → status lifecycle
