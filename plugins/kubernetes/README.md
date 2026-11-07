# kubernetes

Agnostic Kubernetes craft — portable manifest authoring plus pod/event/log
triage. Install when Kubernetes MCP is available. Site overlays stay in
private `homelab`.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `kubernetes-manifests` | Manifest craft on top of `code-yaml` (shape, labels, probes, images) |
| `kubernetes-triage` | Workload / event status |
| `kubernetes-logs` | Short log excerpts |
| `kubernetes-safety` | Destructive action gates |

## Skills

| Skill | Purpose |
| --- | --- |
| `kubernetes` | Index / gate |

## Commands

- `/kubernetes` → cluster triage

## Pairing

- `grafana` — metrics/logs correlation
- `homelab` (private) — site-specific k8s overlays
- `global-mcp-first` — Kubernetes MCP before kubectl side paths

## Diagrams

- [`docs/kubernetes-workflow.drawio`](docs/kubernetes-workflow.drawio) — gate → act → evidence
