---
name: docker-ops
description: >-
  Operate Docker/Compose from the host CLI for the current change.
---

# Docker ops

1. Load `docker-ops` and respect `docker-dev` (local mounts vs deployed images).
2. Prefer the project's existing compose/Dockerfile patterns.
3. Keep secrets out of images and committed compose overlays.
