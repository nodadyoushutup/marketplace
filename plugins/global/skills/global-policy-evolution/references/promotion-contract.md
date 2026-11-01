# Global Policy Promotion Contract

Repo-local only: promote and sync inside the open git repository root. Never
write project policy into user-home IDE trees.

## Canonical vs mirrors

| Path | Role |
| --- | --- |
| `AGENTS.md` | Cross-host standing posture |
| `.cursor/rules`, `.cursor/skills`, `.cursor/agents`, `.cursor/hooks` | Canonical rich assets (edit here) |
| `.claude/rules`, `.claude/skills`, `.claude/agents` | Claude mirrors |
| `CLAUDE.md` | Claude standing import of `AGENTS.md` (managed) |
| `.github/copilot-instructions.md` | Copilot standing pointer (managed) |
| `.github/instructions/*.instructions.md` | Copilot path rules (managed) |
| `.agents/skills` | Codex skill mirrors |

Generated mirrors include `policy-sync: managed`. Edit canonical sources, then
run `sync_policy.py`. Do not hand-maintain managed mirrors.

## Overlay

``.cursor/policy-config.json`` accepts:

- `forbiddenPolicyNames` (unique non-empty strings)
- `enabledHosts` (non-empty subset of `cursor`, `claude`, `copilot`, `codex`;
  must include `cursor`)
- `syncEnabled` (boolean; default `true`)

MCP server enablement is user-level editor config — not project policy. Hooks
under `.cursor/hooks/` are Cursor-local and are not synced.

## Promotion gate

A completed promotion:

1. Patches canonical owners only.
2. Runs `sync_policy.py .` when `syncEnabled` is true.
3. Runs full `validate_policy.py .` (not `--changed`).
4. Reverts on validation failure.

Full validation covers frontmatter, uniqueness, forbidden names, secrets,
links, path containment, and symlinks across present host trees. `--json`
emits machine-readable findings.

## Policy asset naming

Basenames must use the owning plugin or project prefix (see marketplace
`AGENTS.md` or the consuming repo’s policy). Prefer `globs` over always-on
rules when path scope is enough.
