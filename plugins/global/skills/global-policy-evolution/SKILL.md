---
name: global-policy-evolution
description: >-
  Promote verified durable guidance into repo-local project policy for Cursor,
  Claude Code, GitHub Copilot, and OpenAI Codex. Self-manage AGENTS.md and
  .cursor, then sync host mirrors. Use after durable lessons or policy fixes.
---

# Global Policy Evolution

Repo-local project management for agent guidance. Scope is the **open git
repository root only** — never user-home trees (`~/.cursor`, `~/.claude`,
`~/.codex`, `~/.agents`).

## Model

| Layer | Role |
| --- | --- |
| `AGENTS.md` | Cross-host standing posture (Cursor, Copilot, Codex; Claude via import) |
| `.cursor/` | **Canonical** rich assets — rules, skills, agents, hooks |
| `.claude/`, `.github/…`, `.agents/` | **Mirrors** refreshed by sync (do not hand-edit generated files) |

Self-managing loop after verified durable guidance:

1. Patch the narrowest canonical owner (`AGENTS.md` and/or `.cursor/…`).
2. Replace contradictory guidance; reject secrets and speculation.
3. Sync host mirrors.
4. Validate the full repository.
5. Revert on validation failure.

## Host map

| Host | Standing | Rules | Skills | Agents |
| --- | --- | --- | --- | --- |
| Cursor | `AGENTS.md` | `.cursor/rules/*.mdc` | `.cursor/skills/` | `.cursor/agents/` |
| Claude Code | `CLAUDE.md` → `@AGENTS.md` | `.claude/rules/*.md` | `.claude/skills/` | `.claude/agents/` |
| GitHub Copilot | `AGENTS.md` + `.github/copilot-instructions.md` | `.github/instructions/*.instructions.md` | (plugins / AGENTS pointers) | — |
| OpenAI Codex | `AGENTS.md` | (via `AGENTS.md`) | `.agents/skills/` | — |

Cursor hooks (`.cursor/hooks/`) and MCP enablement stay host/user-specific —
do **not** sync them. MCP is user-level editor config, not project policy.

## Overlay schema

Optional ``.cursor/policy-config.json`` keys (defaults shown):

- `forbiddenPolicyNames`: `[]` — basenames rejected in every host namespace
- `enabledHosts`: `["cursor","claude","copilot","codex"]` — must include `cursor`
- `syncEnabled`: `true` — set `false` only to pause mirroring

## Policy asset naming

Every rule, skill, agent, and hook basename uses exactly one ownership prefix.

**In this marketplace**, the prefix must match the owning plugin directory —
see root `AGENTS.md`. Homelab prefixes belong in **marketplace-private**.

When promoting into a **consuming project**, prefer plugin prefixes for
portable craft, plus `<project>-*` / `<component>-*` for local ownership.

Prefer path `globs` over `alwaysApply: true` when the guidance is path-specific.

## Workflow

Resolve the skill directory from the installed plugin or
`.cursor/skills/global-policy-evolution/`, then:

```bash
python3 <skill>/scripts/sync_policy.py .
python3 <skill>/scripts/validate_policy.py .
```

Useful flags:

- `sync_policy.py --dry-run` — show planned writes
- `sync_policy.py --check` — fail when mirrors drift
- `validate_policy.py --changed <path>` — iteration only; **not** final promotion

Unmanaged existing `CLAUDE.md` / `.github/copilot-instructions.md` (no
`policy-sync: managed` marker) are left alone. To adopt sync, delete or
replace them with managed stubs, then re-run sync.

See [promotion-contract.md](references/promotion-contract.md) and
[EVALS.md](EVALS.md).
