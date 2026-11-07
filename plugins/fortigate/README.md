# fortigate

Agnostic FortiGate craft: inventory policies/addresses/routes and gated firewall changes via MCP. Prefer FortiGate MCP; never invent policy ids; destructive needs explicit verb.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `fortigate-inventory` | List devices, policies, addresses, routes, and interfaces via MCP |
| `fortigate-safety` | Create/update/delete firewall policy or routes need an explicit verb |

## Skills

| Skill | Purpose |
| --- | --- |
| `fortigate` | Index / gate |

## Commands

- `/fortigate` → FortiGate inventory or gated policy change

## Related capabilities

- Neighbor products and surfaces are out of scope for this plugin — stop if
  the ask is not this product.

## Diagrams

- [`docs/fortigate-workflow.drawio`](docs/fortigate-workflow.drawio) — gate → act → evidence
