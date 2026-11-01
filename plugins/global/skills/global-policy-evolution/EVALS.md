# Global Policy Evolution Evaluations

Verify multi-host promotion for Cursor, Claude Code, GitHub Copilot, and OpenAI
Codex:

- Canonical edits under `AGENTS.md` / `.cursor/`
- `sync_policy.py` mirrors (rules, skills, agents, standing stubs)
- Drift detection via `--check`
- Unmanaged standing docs are not overwritten
- `validate_policy.py` across present host trees
- Forbidden names, `--changed`, `--json`, secrets, links, and symlinks

Tests use temporary fixtures and never depend on the host repository overlay.
