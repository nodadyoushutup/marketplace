# git

Host-agnostic git craft for Claude Code and Cursor — worktrees, merge/rebase
conflicts, and Conventional Commits. Install when the project uses git and
you want those conventions. No git-host (GitHub/GitLab) hard-coded.

## Rules (Cursor)

| Rule | Purpose |
| --- | --- |
| `git-commit-messages` | Conventional Commits for git subjects (always on) |

## Skills (both)

| Skill | Purpose |
| --- | --- |
| `git` | Index / gate for Claude + explicit entry |
| `git-worktrees` | Isolate under `~/.cursor/worktrees`; remount lanes; default-branch detect; prune on ask |
| `git-resolve-merge-conflicts` | Finish merge/rebase conflicts safely |

## Commands

- `/git` → worktrees, conflicts, or commit-message craft
- `git-worktree` → `git-worktrees`
- `git-resolve-conflicts` → `git-resolve-merge-conflicts`

## Defaults

- Detect the default remote branch; do not assume `main`.
- Commit and push only when the user asks (unless the consuming project has
 an explicit commit-and-push preference).
- Pull request titles and Actions live in the git-host plugin (for example
 github).

## Diagrams

- [`docs/git-workflow.drawio`](docs/git-workflow.drawio) — gate → act → evidence
