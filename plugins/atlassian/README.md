# atlassian

Unified Atlassian craft for Claude Code and Cursor — **Jira** + **Confluence**
in one plugin. Install when the project uses Atlassian MCP (or equivalent). No
project- or space-specific keys hard-coded.

## Rules (Cursor)

### Jira

| Rule | Purpose |
| --- | --- |
| `atlassian-jira-create` | When to file; create-only default; epic parent; never invent IDs |
| `atlassian-jira-description` | Overview + numbered Requirements + matching AC |
| `atlassian-jira-story` | New work / development |
| `atlassian-jira-bug` | Defects and maintenance fixes |
| `atlassian-jira-task` | Non-code / light chores |
| `atlassian-jira-subtask` | Child slices (explicit ask only) |
| `atlassian-jira-epic` | Milestone parents (explicit ask only) |
| `atlassian-jira-status` | Backlog → on deck → In Progress → Done |

### Confluence

| Rule | Purpose |
| --- | --- |
| `atlassian-confluence-create` | When to file; create-only default; search before create; never invent IDs |
| `atlassian-confluence-structure` | Overview + headed H2 sections |
| `atlassian-confluence-page` | Standard documentation page |
| `atlassian-confluence-update` | Prefer section updates; preserve macros |
| `atlassian-confluence-diagrams` | Author with `drawio-author`, then attach |

All rules are **agent-requested** (`alwaysApply: false`) so cold clones without
Atlassian do not load them every turn.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `atlassian` | Index / gate — routes Jira vs Confluence |

## Commands

- `/atlassian` → route tracker or docs work
- `/jira` → file or shape an issue (short slash UX)
- `/confluence` → create, update, or shape a page (short slash UX)

## Pairing

- `global-execute-first` — create-only wins when the primary verb is
  file/ticket or docs/wiki
- `business-analyst` — shape problem/AC before filing or documenting when the
  ask is fuzzy
- `drawio-author` / `drawio-repair` — figures before attach
  (`atlassian-confluence-diagrams`)
- `code-workflow` — implement only after an explicit second verb or a named
  existing issue

## Diagrams

- [`docs/atlassian-jira-workflow.drawio`](docs/atlassian-jira-workflow.drawio)
  — ticketless gate → create-only vs implement → status lifecycle
- [`docs/atlassian-confluence-workflow.drawio`](docs/atlassian-confluence-workflow.drawio)
  — pageless gate → search-before-create → create-only vs update → diagram
  attach
