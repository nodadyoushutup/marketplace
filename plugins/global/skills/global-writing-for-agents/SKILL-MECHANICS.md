# Skill mechanics

Skill-only branch of `global-writing-for-agents`. Body craft lives in
[SKILL.md](SKILL.md). This file covers discovery, frontmatter, and routers.

## Discovery choice

| Mode | How it fires | Context cost | Use when |
| --- | --- | --- | --- |
| **Agent-discoverable** | Model may auto-load from `description:`; humans can still type the name | Description stays always-loaded | Agent (or another skill) must find it unprompted |
| **Human-only** | Human types the skill name; other skills cannot auto-fire it | Near-zero | You are the index; agent must not roam into it |

Mechanics:

- Agent-discoverable: write a model-facing `description` with real trigger
  branches (pointer rules in `SKILL.md`). Do not set
  `disable-model-invocation`.
- Human-only: set `disable-model-invocation: true`. Keep `description` as a
  one-line human summary — strip trigger lists so they are not always-loaded
  bait.

Default to human-only unless autonomous reach is required.

Shared reference needed by two human-only skills cannot live as a third skill
with no description either of them can fire. Put it in a plain sibling file and
point at it.

## Split by discovery

Carve out a new agent-discoverable skill when:

- You have a distinct anchor word that should fire it alone, **and** you
  actually use that word in prompts, or
- Another skill must be able to load it.

You pay permanent context for the new description — the independent reach must
be worth that line.

## Router skills

When human-only skills pile up past memory, add one **router** skill: a
human-only index that names the others and when to use each. It can only
*hint*; it cannot auto-fire human-only targets. One thing to remember instead
of many.
