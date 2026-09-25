---
name: jira
description: >-
  File or shape a Jira issue using the atlassian plugin (create-only by
  default; Overview/Requirements/AC for Stories and Bugs).
---

# Jira

Short slash UX for Atlassian tracker work (`/jira`).

1. Prefer a ready Jira / Atlassian MCP when tracker work is in play.
2. Load `atlassian` and follow `atlassian-jira-create` + the matching type
   rule.
3. Stories and Bugs: write expand-wrapped Overview + **ordered** Requirements
   + matching ordered AC per `atlassian-jira-description` (AC 1:1).
4. Create-only unless the user also asked to implement.
