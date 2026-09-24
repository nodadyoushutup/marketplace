# confluence

Agnostic Confluence craft for Claude Code and Cursor. Install when the project
uses Confluence (Atlassian MCP or equivalent). No space-specific keys or
labels hard-coded.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `confluence-create` | When to file; create-only default; search before create; never invent IDs |
| `confluence-structure` | Overview + headed H2 sections |
| `confluence-page` | Standard documentation page |
| `confluence-update` | Prefer section updates; preserve macros |
| `confluence-diagrams` | Author with `drawio-author`, then attach |

All rules are **agent-requested** (`alwaysApply: false`) so cold clones without
Confluence do not load them every turn.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `confluence` | Index / gate for Claude + explicit entry |

## Commands

- `/confluence` → create, update, or shape a page using the rules above

## Pairing

- `global-execute-first` — create-only / update-only wins when the primary
  verb is docs/wiki
- `drawio-author` / `drawio-repair` — figures before attach
  (`confluence-diagrams`)
- `business-analyst` — shape problem/AC before documenting when the ask is
  fuzzy
- `jira` — tracker issues stay in Jira; link from Confluence when useful
- `code-workflow` — implement only after an explicit second verb

## Diagrams

- [`docs/confluence-workflow.drawio`](docs/confluence-workflow.drawio) —
  pageless gate → search-before-create → create-only vs update → diagram
  attach
