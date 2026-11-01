---
name: global-asd-ste100
description: >-
  Rewrite English so an agent or downstream system cannot misread it — tool
  descriptions, error messages, inter-agent instructions, system prompts,
  status reports — or when text is dense, hedged, or ambiguous. Triggers:
  disambiguate, STE100, Simplified Technical English, plain-language rewrite,
  controlled-language rewrite, rewrite so an agent cannot misread this. Not
  for creative or marketing copy. Companion to global-action-first (reply
  shape); this skill owns Strict / controlled rewrite jobs.
---

# Controlled plain English (agent-safe)

Rewrite English so a **machine reader** cannot take two meanings from one
sentence. Tool descriptions, error strings, inter-agent instructions, prompts,
and status text pay for ambiguity; humans can ask follow-ups, agents usually
cannot.

The craft borrows rule *categories* from ASD-STE100 (aerospace Simplified
Technical English). It does **not** ship ASD’s approved word dictionary — that
standard is free to obtain but not free to redistribute. Use the official
download when you need dictionary-exact STE for aircraft docs. Here we enforce
structure hard and treat “one approved word” as a direction, not a certified
checklist.

## Pair with `global-action-first`

| Job | Skill |
| --- | --- |
| Normal chat / coding handoff | `global-action-first` — lead with the result; use STE-flavored sentence habits inside that shape |
| Explicit rewrite / “apply STE” on pasted text | **This skill** — Strict or STE-flavored; default output is the rewrite alone |

Do not replace a normal action-first reply with a bare rewrite unless the user
asked only for a rewrite. Do not run Strict on every conversational answer.

## When to use

- Output is dense, jargon-heavy, or ambiguous.
- Another agent, a translator, or a non-native reader will consume the text and
  misparse has a real cost.
- You are drafting a prompt, system message, or tool description and want
  ambiguity gone before a model sees it.
- User wants before/after rule callouts (ask for it — default is rewrite only).

Skip creative and marketing copy. Controlled English is flat on purpose.

## Modes

Pick a mode before rewriting. If the user does not name one, infer from the
text type and keep the choice internal unless they asked for the rule table.

**Strict** — procedures, errors, tool/function descriptions, inter-agent
instructions, safety text. Apply every structural rule below, including length
caps and one-instruction-per-sentence.

**STE-flavored** — READMEs, PR text, changelogs, explanatory prose. Keep
structure (length, voice, no phrasal verbs, no semicolons, no marketing fluff).
Relax one-word-one-meaning lockdown so prose does not become a personality
transplant.

## What this skill can and cannot certify

| Kind | Enforce? | Why |
| --- | --- | --- |
| Structural rules (shape, voice, length, punctuation) | Yes | Self-contained; no dictionary required |
| Lexical rules (approved word list) | Direction only | Dictionary is not in-repo |

Never imply certified STE compliance. Say “agent-safe rewrite” unless the user
is working against the official ASD download.

## Structural rules (apply)

| Rule | Do | Don't |
| --- | --- | --- |
| Active voice | “The agent deletes the file.” | “The file is deleted…” unless the actor is unknown or irrelevant |
| No soft phrasal verbs | “Remove the panel.” / “Start the job.” | “Take off…” / “Spin up…” |
| One instruction per sentence | “Open the file. Read line 3.” | “Open the file and read line 3, then…” |
| Length | ≤20 words for instructions; ≤25 for description | Long compound sentences |
| No semicolons | Split into sentences | Any `;` |
| Noun clusters | ≤3 nouns stacked | “high pressure fuel pump inlet valve assembly” |
| No telegraphic drops | Keep subject/verb/article when dropping them creates ambiguity | “Files not backed up will be lost” |
| Keep modality | “The request **may have** failed.” | Upgrade hedges to facts |
| Paragraphs | One topic; ≤6 sentences | Multi-topic blocks |
| Lists | Number/bullet 3+ steps or conditions | Bury sequences in one sentence |

## Lexical rules (direction only)

| Rule | Do | Don't |
| --- | --- | --- |
| One name per thing | Pick one verb/noun and reuse it | Rotate check / verify / confirm for the same action |
| Prefer noun form when both work | “Apply oil to the valve.” | “Oil the valve.” when both are equal |
| Verb, not noun | “Analyze the log.” | “Perform an analysis of the log.” |
| Domain terms | Keep needed jargon; define once | Undefined slang |

## Tenses

Prefer simple present / past / future / imperative. Keep present perfect only
when it carries **current relevance** the simple past cannot (“the job has
completed” vs “the job completed”). Flag that departure; do not silently
flatten hedges.

## Scan checklist (before rewrite)

1. **Synonym rotation** — one thing, many names → pick one.
2. **Hedge stacking** — “may potentially help to improve” → claim or delete.
3. **Nominalization** — “perform an analysis” → “analyze”.
4. **Marketing adjectives** — seamless, robust, powerful → delete or measure.
5. **Run-ons** — split on `;` / stacked dashes.
6. **Soft phrasals** — spin up, reach out, dive into → start, contact, read.

## Process

1. Choose Strict or STE-flavored.
2. Read for meaning once before rewriting.
3. Flag structural hits (and lexical hits in STE-flavored without enforcing).
   Optional: `scripts/ste-lint.py` (stdin or files; `--json`; `--baseline N`;
   `--disable rule1,rule2`). It never fails on hedges/modality.
4. Rewrite without dropping precision. If length would kill a safety/scope
   hedge, keep the longer line and note it.
5. Default output: rewritten text only (see below).
6. If already clear, say so — do not force edits.

## Output format

**Default:** rewritten text alone. No skill preamble, mode banner, or offer to
explain.

Allowed add-on: one trailing line `Kept as-is: <phrase> — <precision at risk>`
when you refused to shorten.

**On request** (“show the diff”, “which rules”, “before/after”):

```markdown
| Rule violated | Original | Simplified |
| --- | --- | --- |
| Present perfect | "We have received your request." | "We received your request." |

Mode: Strict. N violations found.
```

Then one line on anything you did not simplify, and why.

## Boundaries

**Will:** shorten to remove ambiguity; preserve facts, hedges, and scope;
suggest a one-line glossary entry for sticky domain terms.

**Will not:** claim ASD dictionary compliance; rewrite creative/marketing
voice; silently drop safety/scope to hit a word count; turn “may have failed”
into “failed”; polish empty content into empty clarity; shorten past the point
of understanding.

## Extra files

- `references/writing-rules.md` — paraphrased STE rule categories + citations
- `examples/before-after.md` — worked rewrites
- `scripts/ste-lint.py` — structural linter (stdlib only)
