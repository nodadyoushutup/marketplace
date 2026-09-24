---
name: code-debug
description: >-
  Root-cause a failure with evidence, minimal fix, and re-verify.
---

# Debug

1. Follow `code-systematic-debugging` (evidence before fix).
2. Launch `code-debugger` when a subagent is useful; otherwise run the skill in-parent.
3. After the fix, re-run the failing check and apply `code-verification-before-completion` before claiming done.
