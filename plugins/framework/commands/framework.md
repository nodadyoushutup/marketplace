---
name: framework
description: >-
  Load framework monorepo craft (isolation, substrate, Docker, git/Jira host
  overlays). Pair with public code/business-analyst/atlassian/… plugins.
---

# /framework

1. Confirm marketplace plugins are available (`framework` + public `global` +
   `code` at minimum; add `atlassian` / `agentmemory` / `browser` as needed).
2. Load the `framework` skill index and the matching **site** `framework-*`
   rule/skill for the ask.
3. For Jira creates, use public `atlassian-jira-*` plus `framework-jira-issues`
   overlay.
4. For plan/debug/QA, use **public** agents (`business-analyst-planner`,
   `code-technical-lead`, `code-debugger`, `code-quality-assurance`, …).
5. Do not invent project-level `.cursor` copies of public craft.
