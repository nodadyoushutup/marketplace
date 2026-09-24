---
name: jira
description: >-
  File or shape a Jira issue with agnostic Story/Bug/Task/Epic/Sub-task craft.
---

# /jira

1. If the user did not authorize create/manage and named no issue key, say so
   and stop — do not invent a ticket.
2. Otherwise load `jira` and follow `jira-create` + the matching type rule.
3. Stories and Bugs: write Overview / Requirements / Acceptance Criteria per
   `jira-description` (AC numbered 1:1 with Requirements).
4. Prefer Jira MCP tools. Never invent project/epic/board.
5. Create-only unless the user explicitly asked to implement too.
6. Return the issue key (and browse URL when known).
