---
name: framework
description: >-
  Load framework monorepo craft (isolation, substrate, Docker, git/Jira overlays).
---

# /framework

1. Confirm marketplace plugins are available (`framework` + `global` + `code` at minimum).
2. Load the `framework` skill index and the matching `framework-*` rule/skill for the ask.
3. For Jira creates, use `jira-*` plus `framework-jira-issues` overlay.
4. Do not invent project-level `.cursor` policy copies.
