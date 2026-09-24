# framework

Homelab **framework** monorepo plugin. Install alongside `global`, `code`,
`business-analyst`, `jira`, and other stacks. This plugin is the only place
framework-specific Cursor craft should live — not under the repo’s
`.cursor/rules` / `skills` / `agents`.

## Rules (Cursor)

Includes addon isolation/structure/hygiene, runtimes/GUI, cache, auth,
git workflow, thin Jira overlays, parity porting, ceremony budget, and more
(`framework-*.mdc`).

Language baselines (`code-python`, `code-javascript`, …) come from the
**`code`** plugin — not duplicated here. React GUI patterns stay in
`framework-react`.

## Skills

| Skill | Purpose |
| --- | --- |
| `framework` | Index / gate |
| `framework-addon-isolation` | Stranger-test / purpose leakage |
| `framework-addon-substrate` | Substrate Check |
| `framework-addon-modularity` | Removability / soft edges |
| `framework-docker` | Host Docker/Compose CLI |
| `framework-docker-ops` | Framework compose/runtime overlay |
| `framework-parity-porting` | Foreign → custom-addon ports |

## Agents

| Agent | Purpose |
| --- | --- |
| `framework-impact-researcher` | Pre-edit blast radius |
| `framework-contract-reviewer` | Post-edit contracts/boundaries |
| `framework-verification-runner` | Checks beyond the stop hook |
| `framework-runtime-observer` | After restart/migrate/seed |
| `framework-parity-assessor` | Parity assess/plan (read-only) |

## Hooks (Cursor)

Plugin hooks (`hooks/hooks.json`) using `${CURSOR_PLUGIN_ROOT}`:

- `afterFileEdit` → `framework-record-edit.py`
- `afterAgentResponse` → `framework-record-response.py`
- `stop` → `framework-workflow-gate.py` (owner pytest / GUI vitest floor)

## Commands

- `/framework` → index skill
