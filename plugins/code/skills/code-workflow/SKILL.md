---
name: code-workflow
description: >-
  Run software changes through a scalable workflow: intake, issue context,
  scope gate, internal approach, parallel research, execution notes, execute,
  verify, bounded repair, deslop and review gates, then finish with evidence.
  Use at the start of any feature, bug fix, refactor, or multi-file coding
  task. Do not switch the editor to Plan mode.
---

# Coding Workflow

Apply the same engineering discipline in every repository without making small
changes bureaucratic. The workflow is independently maintained; project-specific
automation may inspire it but does not define or synchronize it.

Repository instructions always win for project-specific commands, safety
boundaries, quality standards, and deployment behavior.

## 1. Pick a tier

Ceremony is a cost paid from the user's time and tokens. Choose the smallest
tier the risk justifies — most requests are Direct. Escalate on evidence that
the work is larger or riskier, never out of habit.

| Tier | Use when | Required phases |
|---|---|---|
| **Direct** | A localized change with an obvious shape: bug fix, small feature, config, docs, or a handful of edits inside one module | Intake, execute, verify, finish |
| **Standard** | A focused change spanning several files in one subsystem, or one carrying a repository risk trigger | Intake, scope, approach, execute, verify, repair if red, finish |
| **Full** | Cross-subsystem work, major refactor, new capability, hard cut, or user-requested plan | All phases |

Direct work needs no todo list, no written plan, and no research fan-out.
Standard and Full work should track the active phase and remaining gates with
the available task mechanism. Stay in Agent mode for every tier. Switch the
editor to Plan only when the user explicitly asked for a plan this turn.

Direct is already the default. "quick", "just do it", "no ceremony", or
"execute" is a reminder, not a gate: keep Direct for the rest of the session
until they ask for depth again.

## Phase 0 — Intake

1. Restate the requested outcome in one sentence.
2. Classify the request:
   - **Explain:** the user asked why/how/walk-through with no implied fix. Inspect and report.
   - **Change:** a feature, bug report, "I think X is broken", or "can we address this". Implement it. Do not wait for "please fix it".
3. Declare the tier.
4. Read repository instructions before choosing an implementation.

Explain requests use the investigation or debugging workflow appropriate to the
repository and stop after an evidence-backed report.

## Phase 1 — Issue context

Default: **no tracker**. Implement on the **current branch**.

Use an issue tracker only when this turn’s user text **names an existing
issue key** or **explicitly says to create/file** a ticket/story/bug/task
(for example “make a Jira”, “file a Story”). Fetch that issue and treat its
body and acceptance criteria as requirements evidence.

Do **not** create a new tracker issue to “cover” ordinary feature or fix work,
and do not invent an issue so issue-keyed branching can run. Repository how-to
rules for filing tickets are procedures for when creation is already
authorized — they are not a mandate to invent tickets. Ambiguity → no create.

### Isolation (before execute)

When isolation applies per `code-worktrees` (user asked for a worktree, or
host rules require issue-keyed isolation, and the user did not opt out),
**load `code-worktrees` and establish the checkout before Phase 6**.
Create-only tracker asks never open a worktree.

When isolation is off, stay on the current branch / open checkout.

## Phase 2 — Scope gate

Resolve only ambiguities that would materially change the implementation.

- Read the repository instead of asking. Existing code is the default.
- Do not stop to ask which approach to use. Pick the reversible option that
  matches nearby patterns and state the assumption in the handoff.
- Stop only for irreversible data loss, a missing secret, two incompatible
  user-visible outcomes with no reversible default, or a **broad** feature
  ask with no success criteria (scope grill per `global-action-first` —
  one question or one frontier round with recommended defaults, then act).
- Never call `AskQuestion` or `SwitchMode` for approach selection, missing
  polish details, or "requirements unclear" when a reversible default exists.

## Phase 3 — Approach

For Standard and Full work, sketch internally and then edit in the same turn.
Do not switch the editor to Plan mode. Do not present a plan and wait.

1. Recall relevant project memory when a memory system and project policy are
   available. Treat recalled material as leads and verify it against current
   evidence. Continue normally when memory is unavailable. Recalled planner
   guidance never authorizes a question loop.
2. Inspect the smallest set of files that establishes existing behavior,
   boundaries, tests, and repository conventions.
3. Define intended behavior and explicit acceptance criteria.
4. Identify independent unknowns suitable for parallel research.

Keep any approach notes to one short paragraph in the conversation unless the
user asked for a durable plan artifact. Then execute.

## Project subagent routing

When repository instructions define project subagents (see `AGENTS.md`),
**auto-launch** them on Standard and Full work from that repo’s launch matrix.
Do not ask the user which agents to run or wait for “launch the reviewer.”
Trivia / Direct one-file fixes still launch none. Escape-hatch phrases
(`quick`, `no ceremony`) skip remaining launches for the session.

Each subagent re-reads the codebase — give sharp standalone prompts and
parallelize independent roles. For **readonly** advisory agents (BA, tech lead, code reviewer), the parent
**must** embed evidence in the Task prompt: changed paths plus a diff or status
summary. Those agents must not run Shell/`git` (Cursor sandboxes readonly
subagent shells as `workspace_readonly`). Subagent reports are advisory;
repository hooks remain the enforcement layer for required owner tests. The
parent must not claim a check from an agent report unless the report includes
the exact successful command or probe.

Typical routing when the repo provides these roles:

1. Before edits: `business-analyst` / `code-technical-lead` /
   `business-analyst-researcher` on Standard/Full when acceptance or approach
   is unclear (`business-analyst` + `code` plugins).

2. After edits: `code-reviewer` on meaningful diffs; run
   `code-verification-before-completion` for checks hooks do **not** already
   run (never duplicate owner pytest/vitest).
3. After an authorized runtime operation: use a host runtime observer **if the
   consuming repo provides one** — never use an observer to authorize the op.

## Phase 4 — Research

Use this phase for Full work or multiple independent unknowns.

- Start impact research before implementation edits, then fan out any remaining
  independent questions in one parallel batch.
- Give each researcher complete standalone context and a non-overlapping goal.
- Use repository exploration for code questions and primary external sources
  for current library, protocol, security, or compatibility questions.
- Join the results yourself. Resolve contradictions using current code, tests,
  runtime evidence, or primary documentation rather than averaging opinions.

## Phase 5 — Execution notes

Before Full execution, define:

1. **Work packages** — disjoint file ownership for parallel work; order
   dependent packages into later waves.
2. **Verification commands** — exact tests, type checks, linters, builds, and
   runtime checks selected from repository guidance and discovered tooling.
3. **Quality gates**:
   - `needs_deslop`: true for major multi-file or AI-heavy implementation.
   - `needs_security`: true for authentication, authorization, secrets, SQL,
     trust boundaries, network surfaces, filesystem writes, or external input.
   - `needs_code_review`: true for changes whose correctness is not obvious
     from focused verification alone.
4. **Operational action** — whether the affected runtime needs a restart,
   rebuild, migration, or deployment, governed by repository instructions.

## Phase 6 — Execute

Direct and Standard work is normally edited inline.

When Phase 1 turned isolation **on**, the edit root is the worktree from
`code-worktrees` — not the live open checkout. Confirm path /
`working_directory` before writes.

For Full work, parallelize only packages with disjoint files. Never assign two
agents to edit the same file concurrently. Integrate dependent work in waves.

Implement the requested target state:

- Follow repository conventions and architecture.
- Leave no ephemeral `#` / `//` comments; see `code-comments` (docstrings/JSDoc still follow language rules).
- Replace superseded behavior rather than accumulating accidental dual paths.
- Remove code, dependencies, and configuration made obsolete by the change
  when repository policy authorizes that hard cut.
- Do not expand into unrelated cleanup.
- Respect host isolation: keep product-specific logic in product packages;
  shared substrate stays generic.

Perform authorized runtime restarts or rebuilds after the edit batch, once,
using the repository's operational guidance. Follow the operation with
read-only runtime observation when the project agent is available.

## Phase 7 — Verify

Run the checks selected before implementation, narrow to broad, and stop at the
first level that covers the risk:

1. Focused tests for the changed behavior.
2. Static checks such as type checking, linting, or compilation.
3. The owning package or subsystem suite.
4. Integration, build, or runtime smoke checks when contracts cross boundaries.
5. Repository policy validation when rules, skills, hooks, or agent guidance
   changed.

When the repository runs checks automatically at turn end, that run is the
verification floor for Direct work: read the diff, let the gate run the owner
tests, and do not pay for the same targets twice by hand or by subagent. Add
levels only for risk the automated gate does not cover.

Read-only or diagnostic requests verify the conclusion with corroborating code,
configuration, tests, history, or runtime evidence.

Never claim a check ran when it did not. A container being `Up`, a process
starting, or a build completing does not by itself prove the changed behavior.

## Phase 8 — Repair

Classify every failure before editing:

- **Local:** implementation defect, import, assertion, type error, or stale
  expectation. Fix directly.
- **Structural:** the design, ownership boundary, or approach is wrong. Replan
  internally and continue. Do not switch to Plan mode or quiz the user.
- **Environmental:** missing authorization, service, dependency, or external
  prerequisite. Confirm once, then report the blocker rather than changing code
  to hide it.

Budgets:

- At most three local repair attempts for the same verification target.
- The same failure twice triggers a structural reassessment.
- At most one structural replan before reporting blocked.

Every repair that edits files returns to verification.

## Phase 9 — Quality

Direct work skips this phase. Standard and Full work runs only the gates
selected in the execution notes, in this order:

1. **Deslop** — remove dead paths, compatibility residue, pointless
   abstractions, duplicated explanations, and session-only verification code;
   then review the structure of live logic and lasting test coverage. Follow
   the project `code-deslop` skill when available.
2. **Security review** — when the change touches auth, secrets, trust
   boundaries, or untrusted input, use the host security-review workflow if
   present (otherwise apply careful manual review).
3. **Code review** — launch `code-reviewer` for non-obvious changes.
4. **Review fixes** — apply justified findings and return to verification.

Limit review-and-fix to two cycles. Do not churn on stylistic preference after
correctness, clarity, and repository standards are satisfied.

## Phase 10 — Finish

1. Capture only durable, verified lessons when project memory policy requests
   it. Do not save transient task status or guesses.
2. Report the changed behavior and important files.
3. State exactly what was verified and whether anything remains blocked.
4. Do not create commits, push, deploy, or mutate external systems unless the
   user authorized those actions.

Scale the handoff to the change. A Direct edit closes in a few lines: what now
behaves differently, where, and what proved it. Save the phase-by-phase
accounting for Full work.

## Blocked

When a repair budget is exhausted or a dependency is genuinely unavailable,
stop cleanly. Report:

- the failed acceptance criterion,
- the last concrete error or missing prerequisite,
- what was attempted,
- the single action or decision that would unblock the work.

Do not disable failing tests, silently degrade behavior, or invent a fallback to
make the task appear complete.
