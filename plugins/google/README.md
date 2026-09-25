# google

Unified Google Workspace craft — Gmail, Drive, Calendar, Docs, Sheets.
Install when the project uses Google Workspace MCP (or equivalent).

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `google-gmail` | Search / draft / send / labels |
| `google-drive` | Files, folders, sharing |
| `google-calendar` | Events, free/busy, OOO |
| `google-docs` | Docs and Sheets edits |

All rules are **agent-requested** (`alwaysApply: false`).

## Skills

| Skill | Purpose |
| --- | --- |
| `google` | Index / gate |

## Commands

- `/google` → Workspace surface craft

## Pairing

- `global-mcp-first` — Google Workspace MCP before raw Gmail/Drive APIs
- `global-host-url` — never hand the user localhost links
- `atlassian` / `freshservice` — tracker siblings when filing from mail
