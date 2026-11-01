---
name: code-execute-issue
description: >-
  Execute a named tracker issue through an isolated worktree to an open pull
  request. Stop when the pull request is ready — never merge, never mark the
  issue done. Use when the user runs /code-execute-issue or asks to execute
  an issue key through a pull request.
---

# Execute a tracker issue (worktree → pull request)

Own one named issue in the tracker application, from read through an open
pull request on the git host. Hand the merge decision back to the operator.

## Gate

- An issue key is required this turn (slash argument or the key in the
  message). No key → ask once; if it is still missing, stop.
- Prefer a connected tool for the tracker application when reading the
  issue, and a connected tool for the git host when opening the pull
  request. Use the host CLI only after the connected tool is missing or
  has failed.
- Skip when the ask is only to file a new issue, or when there is no key.

## This command authorizes

| Allowed | Forbidden |
| --- | --- |
| Rename the chat title to the issue key | Merge the pull request |
| Worktree isolation (`code-worktrees`) | Force-push or rewrite shared history |
| Commits and push on the issue-key branch | Mark the issue done |
| Open one pull request against the default branch | Pick a different issue |
| Move the issue to in progress when that state exists | Invent a project, board, or parent id |

Follow a host overlay when the repository provides one. Do not invent
product names in this skill.

## Steps

1. **Resolve the key.** Trim whitespace. Use that exact key for the branch
   name, the chat title, and the pull-request text. **Done when** one key
   is fixed.
2. **Read the issue** in the tracker application: description, acceptance
   criteria, comments, and links. Treat the requirements and acceptance
   criteria as the success bar. **Done when** you can list them.
3. **Blocker gate.** If the tracker application shows this issue is blocked
   by another issue that is still open, stop and report that key. Do not
   branch or implement. Issues that this one blocks do not stop the run.
   **Done when** you either stopped or confirmed there is no open blocker.
4. **Rename the chat** to exactly the issue key when the editor supports it.
   **Done when** the title matches the key, or the editor has no rename.
5. **Status.** If the tracker application uses a board, move the issue onto
   a board only when the operator named that board. Then set the state to
   in progress. Do not mark it done. **Done when** the state is in progress
   or the tracker application has no such state.
6. **Isolate.** If the repository forbids git worktrees, branch in the open
   checkout with the issue-key name. Otherwise follow `code-worktrees`.
   **Done when** the live checkout path is recorded.
7. **Implement.** Follow `code-workflow`. Satisfy the requirements and
   acceptance criteria with the smallest reversible change. **Done when**
   the change is in the worktree.
8. **Verify.** Follow `code-verification-before-completion`. Run the tests
   the repo already uses. **Done when** those checks passed or you reported
   the failing command.
9. **Open a pull request. Do not merge.**
   - Commit messages follow `code-commit-messages`.
   - Push the issue-key branch.
   - Open one pull request against the default branch on the git host.
   - Title uses the commit-message shape. Body is short what/why bullets.
   - Add a browse link only when the tracker application already has a
     site URL.
   - Prefer a connected git-host tool.
   **Done when** the pull request URL exists.
10. **Stop.** Reply with a short summary, the pull request URL, and that
    merge is manual. Optionally comment the same summary on the issue. Do
    not mark the issue done. Leave the worktree on disk.

## Done when

- The blocker gate passed, or you stopped with the blocking keys
- The chat title is the issue key when rename exists
- Requirements and acceptance criteria are met, with verify evidence
- The issue-key branch is pushed and the pull request is open
- The operator has the pull request URL

Not done: a merged pull request, or the tracker issue marked done. Those
wait for a later ask after the operator merges.
