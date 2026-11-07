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

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/proxmox-workflow.drawio`](docs/proxmox-workflow.drawio) — gate → act → evidence
