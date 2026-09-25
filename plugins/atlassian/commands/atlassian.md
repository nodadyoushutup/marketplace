---
name: atlassian
description: >-
  Route Atlassian work: file or shape a Jira issue, or create/update a
  Confluence page, using the unified atlassian skill and product rules.
---

# Atlassian

1. Load `atlassian`. Prefer a ready Atlassian / Jira / Confluence MCP.
2. Route by product (Jira vs Confluence) using the skill load maps.
3. Jira: follow `atlassian-jira-create` + the matching type rule; Stories and
   Bugs need `atlassian-jira-description` (expand sections; ordered AC 1:1
   with Requirements).
4. Confluence: follow `atlassian-confluence-create` or
   `atlassian-confluence-update`; new pages use Overview + headed sections per
   `atlassian-confluence-structure`.
5. Diagrams: `atlassian-confluence-diagrams` (author with `drawio-author`, then
   attach).
