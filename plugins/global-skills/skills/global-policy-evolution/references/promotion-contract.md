# Global Policy Promotion Contract

Rules live in `.cursor/rules`. Agents live in `.cursor/agents`. Skills live in
`.cursor/skills`. Hook scripts live in `.cursor/hooks`.

`.cursor/policy-config.json` accepts only `forbiddenPolicyNames` (unique
strings). Keys default to empty lists. MCP server enablement is user-level
editor config — not project policy. Shared code contains no repository approval
list or bespoke hook command.

Full validation covers frontmatter, uniqueness, configured forbidden names,
secrets, links, path containment, and symlinks. `--changed` is only for
iteration; `--json` emits machine-readable findings. A completed promotion runs
full validation and reverts on failure.

## Policy asset naming

Basenames must use `global-*` (portable), `framework-*` (base framework), or
`<addon>-*` (single-addon ownership). Custom-addon identities must not appear in
tracked framework policy. Prefer `globs` over always-on rules when path scope is
enough.
