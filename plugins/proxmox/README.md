# proxmox

Agnostic Proxmox VE craft: list nodes/VMs, status, and gated power/clone/migrate via MCP. Prefer Proxmox MCP; never invent VMID or touch sacred hosts.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `proxmox-inventory` | List nodes, VMs, storage, and pools via MCP |
| `proxmox-safety` | Destructive Proxmox gates |

## Skills

| Skill | Purpose |
| --- | --- |
| `proxmox` | Index / gate |

## Commands

- `/proxmox` → Proxmox inventory or gated VM ops

## Pairing

- `global-mcp-first` — MCP before CLI/REST
- `homelab` (private) — site overlays when installed

## Diagrams

- [`docs/proxmox-workflow.drawio`](docs/proxmox-workflow.drawio) — gate → act → evidence
