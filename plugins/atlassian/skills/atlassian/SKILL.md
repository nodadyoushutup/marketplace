---
name: atlassian
description: >-
  Unified Atlassian craft: Jira create-only filing with expand-wrapped
  Overview/Requirements/AC bodies (ordered lists) and Confluence create/update
  with headed sections plus draw.io attach pairing. Use when filing or managing
  Jira issues or Confluence pages. Skip when the user did not authorize tracker
  or docs work.
---

# Atlassian

## Gate

No explicit Jira create/manage/transition ask and no named issue key, **and**
no explicit Confluence create/update/search/comment ask and no named page →
**skip** — stay ticketless and pageless. Prefer a connected Atlassian /
Jira / Confluence MCP when either surface is in play.

Route by product:

| Surface | Signals |
| --- | --- |
| Jira | “Jira”, Story/Bug/Task/Epic/Sub-task, issue key, board/status |
| Confluence | “Confluence”, wiki/page, space key, page id/title |

## Load map — Jira

| Need | Rule / action |
| --- | --- |
| May I create? | `atlassian-jira-create` |
| Story / Bug body | `atlassian-jira-description` + `atlassian-jira-story` / `atlassian-jira-bug` |
| Task / Sub-task / Epic | `atlassian-jira-task` / `atlassian-jira-subtask` / `atlassian-jira-epic` |
| Board / status | `atlassian-jira-status` |

## Load map — Confluence

| Need | Rule / action |
| --- | --- |
| May I create? | `atlassian-confluence-create` |
| Page body shape | `atlassian-confluence-structure` + `atlassian-confluence-page` |
| Edit existing | `atlassian-confluence-update` |
| Architecture / workflow figure | `atlassian-confluence-diagrams` |

## Defaults

1. Create-only / update-only unless the user adds an explicit implement verb.
2. Never invent project, board, epic, assignee, space key, parent page, or
   template id.
3. Stories and Bugs always get `{expand:Overview}` / `{expand:Requirements}` /
   `{expand:Acceptance Criteria}` with **ordered** Requirements and matching
   ordered AC (1:1). See `atlassian-jira-description`.
4. Create Epic or Sub-task only when the user names that type.
5. Leave new issues on backlog unless asked to board or start them.
6. Search Confluence before create — do not mint a near-duplicate title in the
   same space.
7. Prefer `confluence_update_page_section` over full-body rewrites.
8. Diagrams: author a `.drawio` file, then attach it. Do not paste raw XML
   into the page body.

## Procedure

1. Decide the surface from the user's words (Jira issue vs Confluence page).
   **Done when** you can name one surface, or you stopped because neither was
   asked.
2. Resolve ids from the connected tracker tools (project, board, space,
   parent). **Done when** every id you will send was returned by a tool, or
   you stopped instead of inventing one.
3. Follow the load-map rule for that action. **Done when** the body matches
   `atlassian-jira-description` or `atlassian-confluence-structure`, whichever
   applies.
4. Stop after create or update unless the user also used an implement verb.
   **Done when** the reply contains the issue key or page URL and no product
   code was edited on a create-only ask.
