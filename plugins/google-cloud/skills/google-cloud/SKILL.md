---
name: google-cloud
description: >-
  Agnostic Google Cloud craft: project resolution, Compute/GKE inventory,
  Cloud Storage, and hard gates on delete/IAM/public ACL. Prefer a Google
  Cloud MCP when ready; else gcloud. Skip when the user did not authorize GCP
  work.
---

# Google Cloud

## Gate

No explicit Google Cloud / GCP / gcloud / Cloud Console / project / GCS /
Compute / GKE ask and no named project id → **skip**. Prefer a connected
Google Cloud MCP (`global-mcp-first`); fall back to authenticated `gcloud`
only when no matching MCP is ready.

Route by surface:

| Surface | Signals |
| --- | --- |
| Projects | project id, `gcloud config`, billing account |
| Compute / GKE | VM, instance, GKE cluster, node pool |
| Storage | GCS bucket, object, storage class |
| IAM / risk | IAM binding, service account key, public ACL, delete |

## Load map

| Need | Rule |
| --- | --- |
| Project / resource inventory | `google-cloud-inventory` |
| Compute Engine / GKE list-describe | `google-cloud-compute` |
| Cloud Storage buckets / objects | `google-cloud-storage` |
| Delete / IAM / public ACL / keys | `google-cloud-safety` |

## Defaults

1. Never invent project id, zone, region, cluster, bucket, or SA email —
   list/resolve first (`gcloud projects list`, MCP equivalents).
2. Read-only inventory is the default. Mutate only with an explicit verb
   naming the resource.
3. Prefer MCP when ready; do not invent a side path while MCP works.
4. Pair with `kubernetes` for in-cluster pod/log triage after GKE context
   is known; this plugin owns GCP control-plane surfaces.
5. Pair with `google-workspace` for Gmail/Drive/Calendar/Docs — not GCP.
6. No service-account keys, OAuth tokens, or full IAM dumps in chat —
   land secrets in `vault` when possible.
