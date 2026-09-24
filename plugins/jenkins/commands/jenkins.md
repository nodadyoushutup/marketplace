---
name: jenkins
description: >-
  Operate on Jenkins builds, console output, or pipeline definitions with
  agnostic craft (MCP first).
---

# /jenkins

1. If the user did not authorize Jenkins build/console/pipeline work and
   named no job or build, say so and stop.
2. Otherwise load `jenkins` and follow the matching rule
   (`jenkins-builds`, `jenkins-pipeline`, `jenkins-ci-from-main`).
3. Prefer Jenkins MCP tools. Never invent job fullnames or build numbers.
4. Return build result, failing stage/signal, or pipeline path with evidence.
