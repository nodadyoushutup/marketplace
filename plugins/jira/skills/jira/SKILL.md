---
name: jira
description: >-
  Agnostic Jira craft: create-only filing by default, Overview/Requirements/AC
  bodies for Stories and Bugs, and per-type rules for Story, Bug, Task,
  Sub-task, and Epic. Use when filing, editing, or transitioning Jira issues.
  Skip when the user did not authorize tracker work.
---

# Jira

## Gate

No explicit create/manage/transition ask and no named issue key → **skip** —
stay ticketless. Prefer a connected Jira MCP when tracker work is in play.

## Load map

| Need | Rule / action |
| --- | --- |
| May I create? | `jira-create` |
| Story / Bug body | `jira-description` + `jira-story` / `jira-bug` |
| Task / Sub-task / Epic | `jira-task` / `jira-subtask` / `jira-epic` |
| Board / status | `jira-status` |

## Defaults

1. Create-only unless the user adds an explicit implement verb.
2. Never invent project, board, epic, or assignee.
3. Stories and Bugs always get Overview + numbered Requirements + matching
   numbered Acceptance Criteria (1:1).
4. Create Epic or Sub-task only when the user names that type.
5. Leave new issues on backlog unless asked to board or start them.
