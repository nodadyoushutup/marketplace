# argocd

Agnostic Argo CD craft: list/get apps, sync status, and gated sync/action via MCP. Prefer Argo CD MCP; never invent app names.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `argocd-apps` | List and inspect Applications / AppProjects via MCP |
| `argocd-sync` | Sync / refresh / resource actions need an explicit verb naming the app |

## Skills

| Skill | Purpose |
| --- | --- |
| `argocd` | Index / gate |

## Commands

- `/argocd` → Argo CD app status or gated sync

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/argocd-workflow.drawio`](docs/argocd-workflow.drawio) — gate → act → evidence
