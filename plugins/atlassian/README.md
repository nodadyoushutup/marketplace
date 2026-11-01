# atlassian

Unified Atlassian craft for Claude Code and Cursor — **Jira** + **Confluence**
in one plugin. Install when the project uses Atlassian MCP (or equivalent). No
project- or space-specific keys hard-coded.

## Rules (Cursor)

### Jira

| Rule | Purpose |
| --- | --- |
| `atlassian-jira-create` | When to file; create-only default; epic parent; never invent IDs |
| `atlassian-jira-description` | Expand-wrapped Overview + ordered Requirements + matching ordered AC |
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
| `atlassian-confluence-diagrams` | Author a `.drawio` file, then attach it |

All rules are **agent-requested** (`alwaysApply: false`) so cold clones without
Atlassian do not load them every turn.

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `atlassian` | Index / gate — routes Jira vs Confluence |

## Commands

- `/atlassian` → route Jira or Confluence work
- `/jira` → file or shape an issue (short slash UX)
- `/confluence` → create, update, or shape a page (short slash UX)

## Defaults

- Create or update only, unless the user also asked to implement.
- Shape a fuzzy ask into problem, requirements, and acceptance criteria
  before filing. This plugin does not implement product code.
- A figure is a `.drawio` file attached to the page
  (`atlassian-confluence-diagrams`). Do not paste diagram XML into the body.

## Diagrams

- [`docs/atlassian-jira-workflow.drawio`](docs/atlassian-jira-workflow.drawio)
  — ticketless gate → create-only vs implement → status lifecycle
- [`docs/atlassian-confluence-workflow.drawio`](docs/atlassian-confluence-workflow.drawio)
  — pageless gate → search-before-create → create-only vs update → diagram
  attach
