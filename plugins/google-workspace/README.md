# google-workspace

Google Workspace craft — Gmail, Drive, Calendar, Docs, Sheets. Install when
the project uses Google Workspace MCP (or equivalent).

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `google-workspace-gmail` | Search / draft / send / labels |
| `google-workspace-drive` | Files, folders, sharing |
| `google-workspace-calendar` | Events, free/busy, OOO |
| `google-workspace-docs` | Docs and Sheets edits |

All rules are **agent-requested** (`alwaysApply: false`).

## Skills

| Skill | Purpose |
| --- | --- |
| `google-workspace` | Index / gate |

## Commands

- `/google-workspace` → Workspace surface craft

## Pairing

- `global-mcp-first` — Google Workspace MCP before raw Gmail/Drive APIs
- `global-host-url` — never hand the user localhost links
- `google-cloud` — GCP / gcloud / project sibling (not Workspace)
- `atlassian` / `freshservice` — tracker siblings when filing from mail

## Diagrams

- [`docs/google-workspace-workflow.drawio`](docs/google-workspace-workflow.drawio) — gate → act → evidence
