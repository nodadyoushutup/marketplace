# google-cloud

Agnostic Google Cloud craft — projects, Compute/GKE, Cloud Storage, safety
gates. Install when GCP / gcloud (or a Google Cloud MCP) is in play.
Workspace mail/docs stay in `google-workspace`.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `google-cloud-inventory` | Project / resource resolve + list |
| `google-cloud-compute` | Compute Engine / GKE inventory |
| `google-cloud-storage` | GCS buckets / objects |
| `google-cloud-safety` | Delete / IAM / public ACL / keys |

All rules are **agent-requested** (`alwaysApply: false`).

## Skills

| Skill | Purpose |
| --- | --- |
| `google-cloud` | Index / gate |

## Commands

- `/google-cloud` → GCP surface craft

## Pairing

- `global-mcp-first` — Google Cloud MCP before ad-hoc API wrappers
- `kubernetes` — in-cluster triage after GKE context is known
- `vault` — land SA keys / tokens; never chat dumps
- `google-workspace` — Gmail / Drive / Calendar / Docs sibling
- `homelab` (private) — site overlays that name specific projects

## Diagrams

- [`docs/google-cloud-workflow.drawio`](docs/google-cloud-workflow.drawio) — gate → act → evidence
