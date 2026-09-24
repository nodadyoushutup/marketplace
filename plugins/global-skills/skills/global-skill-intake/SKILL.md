---
name: global-skill-intake
description: >-
  Audit and install third-party or community Agent Skills into this project.
  Use when pasting a skills.sh URL, running a skills CLI, copying a package
  into .cursor/skills/, or reviewing an untrusted skill before first use.
---

# Skill Intake (supply chain)

Treat community and third-party skill packages as **untrusted code** until
reviewed—especially anything under `scripts/`.

## When to use

- Installing from [skills.sh](https://skills.sh) or similar catalogs
- Pasting a skill URL and asking an LLM to fetch/write files
- Running an external `npx skills add …` (or similar) CLI
- Reviewing a skill someone else dropped into the tree before first execution

## Destination

Install reviewed skills under `.cursor/skills/<name>/` so this repository owns
the exact version agents use. Do not write into a personal directory such as
`~/.cursor/skills`.

## Checklist

1. **List every file** the install would add (`SKILL.md`, `references/`, `scripts/`, hidden files).
2. **Read `SKILL.md`** — tighten triggers, drop steps that do not apply, align paths to this repo.
3. **Audit scripts** — treat as code execution as the IDE user or worker account. Reject or rewrite anything that network-exfiltrates, touches secrets, or runs unbounded shell.
4. **Reject symlinks** — packages must be real files; prefer copy mode if a CLI would symlink.
5. **Validate layout** — run `python3 .cursor/skills/global-policy-evolution/scripts/validate_policy.py .`; keep packages small; no secrets in examples.
6. **Do not execute** scripts or trust the skill in day-to-day work until the audit above is done.
7. **Wire routing** — add a thin pointer in `AGENTS.md` when teammates must discover the skill.
8. **Commit** `.cursor/skills/` changes only when the user asks for a commit.

## Hard stops

- Secrets, tokens, private personal data, or production credentials in package files
- Running community scripts before review
- Promoting community skill text into always-apply `.cursor/rules` without verification
- Installing project skills only under a personal `~/.cursor/skills`

## Related

- Policy promotion: [global-policy-evolution](../global-policy-evolution/SKILL.md)
