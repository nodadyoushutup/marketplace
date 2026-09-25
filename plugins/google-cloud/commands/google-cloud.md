---
name: google-cloud
description: >-
  Operate on Google Cloud projects, Compute/GKE, and GCS with gated craft
  (MCP first, else gcloud).
---

# /google-cloud

1. If the user did not authorize Google Cloud / GCP work and named no
   project or resource, say so and stop.
2. Otherwise load `google-cloud` and follow the matching rule
   (`google-cloud-inventory`, `google-cloud-compute`, `google-cloud-storage`,
   `google-cloud-safety`).
3. Prefer Google Cloud MCP when ready; else authenticated `gcloud`. Never
   invent project ids.
4. Return project / resource names and short evidence — no credentials or
   localhost.
