---
name: global-policy-evolution
description: Promote verified durable guidance into canonical Cursor project policy.
---

# Global Policy Evolution

## Ownership

- Rules live in `.cursor/rules`.
- Agents live in `.cursor/agents`.
- Skills live in `.cursor/skills`.
- Hook scripts live in `.cursor/hooks`.
- Optional overlay: `.cursor/policy-config.json`.

## Overlay schema

The optional JSON object (``.cursor/policy-config.json``) accepts only these
keys, each defaulting to `[]`:

- `forbiddenPolicyNames`: unique non-empty strings rejected in canonical rule, agent, and skill namespaces.

MCP servers are **user-level only** (editor MCP settings). Do not put
MCP enablement or approvals in project policy.

Shared Cursor hooks always register `.cursor/hooks/framework-record-edit.py`,
`.cursor/hooks/framework-record-response.py`, and
`.cursor/hooks/framework-workflow-gate.py`.


## Policy asset naming

Every rule, skill, agent, and hook basename uses exactly one ownership prefix:

| Prefix | Use for |
|---|---|
| `global-*` | Portable craft shared across repositories |
| `framework-*` | Base-framework contracts, runtimes, project agents, and repo workflow hooks |
| `<addon>-*` | One addon's guidance. Framework-owned addons may appear in this repo; custom-addon policy stays in that addon's repository |

Prefer path `globs` over `alwaysApply: true` when the guidance is path-specific.

## Workflow

1. Verify durable guidance against current evidence or explicit stable policy.
2. Patch the narrowest canonical owner and replace contradictory guidance.
3. Reject secrets, private data, unsafe links or symlinks, and speculative policy.
4. Run full validation:

```bash
python3 .cursor/skills/global-policy-evolution/scripts/validate_policy.py .
```

Do not use `--changed` as the final promotion check. See [promotion-contract.md](references/promotion-contract.md) and [EVALS.md](EVALS.md).
