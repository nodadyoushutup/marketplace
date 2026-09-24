---
name: agentmemory-ops
description: >-
  Advanced AgentMemory MCP ops beyond default recall/capture: slots, actions /
  frontier / leases, checkpoints, signals, mesh/team, commits timeline, graph,
  diagnose/heal, consolidate/reflect, export. Use when coordinating multi-agent
  work, maintaining memory health, or the user asks for these tools.
---

# AgentMemory Ops

## Gate

Not connected/ready → skip. For everyday recall/save use `agentmemory-recall` /
`agentmemory-capture` instead.

Also see rule `agentmemory-tools` for a one-screen routing table.

## Slots (editable working memory)

Pinned / project / global size-limited notes:

- List → `memory_slot_list`; read → `memory_slot_get`
- Write → `memory_slot_create` / `memory_slot_replace` / `memory_slot_append`
- Remove → `memory_slot_delete`

Keep slots compact. On size errors, compress then retry — do not grow a novel.

## Actions & coordination

Use only when tracking multi-step or multi-agent work (not ordinary coding):

1. Optional sketch: `memory_sketch_create` → promote with `memory_sketch_promote`
2. Durable items: `memory_action_create` / `memory_action_update`
3. Pick work: `memory_next` or `memory_frontier`
4. Claim: `memory_lease` (acquire / renew / release)
5. External gates: `memory_checkpoint`; event gates: `memory_sentinel_*`
6. Agent mail: `memory_signal_send` / `memory_signal_read`
7. Peers / team: `memory_mesh_sync`, `memory_team_share`, `memory_team_feed`
8. Finished chains → `memory_crystallize`; routines → `memory_routine_run`

## Search & graph (beyond default)

- Chronology: `memory_timeline`
- Linked commits: `memory_commits` / `memory_commit_lookup`
- Graph: `memory_graph_query`, `memory_relations`
- Insights: `memory_insight_list`; facets: `memory_facet_*`
- Profile: `memory_profile` (stable `project` required)
- Images: `memory_vision_search`

## Maintenance

- Health: `memory_diagnose` then optional `memory_heal` (`dryRun` first if unsure)
- Audit: `memory_audit`
- Tier merge: `memory_consolidate`
- Expensive synthesis: `memory_reflect` (rare, user-justified)
- Backup/export: `memory_snapshot_create`, `memory_export`, `memory_obsidian_export`
- Claude bridge: `memory_claude_bridge_sync`
- Delete: `memory_governance_delete` (needs reason; destructive)
- Markdown shrink: `memory_compress_file` (writes `.original.md` backup)

## Cost posture

Default coding turns should not call this skill’s tools. Prefer recall/capture.
One targeted ops call beats a tour of the catalog.
