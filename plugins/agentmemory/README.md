# agentmemory

Gated AgentMemory MCP craft. Install when the AgentMemory MCP is (or will be)
connected. AlwaysApply rules stay lean; advanced tools load on demand.

## Rules (Cursor)

| Rule | Apply | Purpose |
| --- | --- | --- |
| `agentmemory-recall` | always | Token-efficient recall loop + verify posture |
| `agentmemory-capture` | always | Save lessons/facts + refuse list |
| `agentmemory-tools` | on demand | Full MCP tool routing by job |

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `agentmemory` | Index / gate (Claude + explicit entry) |
| `agentmemory-recall` | Recall playbook |
| `agentmemory-capture` | Capture playbook |
| `agentmemory-ops` | Slots, actions, mesh, diagnose, export |

Claude Code does not load plugin rules — use the skills for the same posture.

## Commands

- `/agentmemory` → gate, then recall and/or capture (ops only when needed)

## Design notes

Everyday turns use ~4 tools: `memory_lesson_recall`, `memory_smart_search`,
`memory_lesson_save`, `memory_save` (plus occasional `memory_file_history` /
`memory_verify`). The MCP exposes 50+ tools; actions/mesh/reflect/export stay
out of the always-on path so they do not waste context.
