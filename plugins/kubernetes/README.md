# kubernetes

Agnostic Kubernetes craft — portable manifest authoring plus pod/event/log
triage. Install when Kubernetes MCP is available. Site overlays stay in
private site repos.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `kubernetes-manifests` | Manifest craft (YAML floor + shape, labels, probes, images) |
| `kubernetes-triage` | Workload / event status |
| `kubernetes-logs` | Short log excerpts |
| `kubernetes-external-secrets` | ExternalSecret / SecretStore craft (no values in git) |
| `kubernetes-addons` | Load balancer, ingress, Postgres operator, cache portable notes |
| `kubernetes-safety` | Destructive action gates |

## Skills

| Skill | Purpose |
| --- | --- |
| `kubernetes` | Index / gate |

## Commands

- `/kubernetes` → cluster triage

## Related capabilities

- Metrics / dashboards — out of scope here
- Secret-provider product craft — out of scope here (key names only via ESO)
- Site-specific overlays — private site repos

## Diagrams

- [`docs/kubernetes-workflow.drawio`](docs/kubernetes-workflow.drawio) — gate → act → evidence
