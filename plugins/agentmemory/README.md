# agentmemory

Gated AgentMemory MCP craft. Install when the AgentMemory MCP is (or will be)
connected. AlwaysApply rules stay lean; advanced tools load on demand.

## Rules (Cursor)

| Rule | Apply | Purpose |
| --- | --- | --- |
| `agentmemory-recall` | always | Aggressive scoped recall + hard user isolation |
| `agentmemory-capture` | always | Save lessons/facts with mandatory user (+ repo) stamps |
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

## Identity scope

`skills/agentmemory/scripts/agentmemory_scope.py` resolves:

- **user** — local whoami-equivalent (`getpass` / `USER` / `USERNAME` / `whoami`)
- **repo** — when a `.git` directory is present: normalized `origin` URL path
  (e.g. `owner/repo`) or git toplevel basename

Every save stamps `user:…` (and `repo:…` when in a git tree). Every recall
query includes those stamps and **discards** hits from other users or without a
user stamp, so a shared AgentMemory service cannot cross streams.

## Design notes

Everyday turns use ~4 tools: `memory_lesson_recall`, `memory_smart_search`,
`memory_lesson_save`, `memory_save` (plus occasional `memory_file_history` /
`memory_verify`). Recall early and often on meaningful work; capture verified
durable insights without waiting to be asked. The MCP exposes 50+ tools;
actions/mesh/reflect/export stay out of the always-on path.

## Diagrams

- [`docs/agentmemory-workflow.drawio`](docs/agentmemory-workflow.drawio) — gate → scope → act → evidence
