---
name: git-resolve-merge-conflicts
description: >-
 Resolve an in-progress git merge or rebase conflict: understand both intents,
 preserve behavior, run project checks, finish the merge. Use when git reports
 conflicts or merge/rebase is stopped mid-way.
---

# Resolve merge conflicts

## Gate

Use this skill only when `git status` shows an in-progress merge or rebase
with unmerged paths. Do not start a merge the user did not ask for.

## Procedure

1. **See state.** Run `git status`. Record whether this is a merge or a
 rebase, the branch names, and every unmerged path. **Done when** you can
 list those paths.
2. **Read both intents.** For each conflicting file, read the commits on both
 sides (`git log` for the two parents, and the messages). Open linked pull
 requests or issues when a tool can fetch them. **Done when** you can say
 what each side was trying to change.
3. **Resolve each hunk.** Keep both changes when they touch different
 behavior. When they clash, keep the side that matches the merge's stated
 goal and write down the trade-off. Remove every conflict marker
 (`<<<<<<<`, `=======`, `>>>>>>>`). Do not invent a third behavior.
 **Done when** a search of the worktree finds no conflict markers.
4. **Special files.** For a binary or generated file, take one side whole.
 Do not hand-merge a lockfile by editing lines; regenerate it with the
 project's package tool when the conflict is only in a lockfile and both
 sides changed dependencies. **Done when** those files have a single
 chosen result.
5. **Abort only when blocked.** Continue the merge when you can reconstruct
 both intents. Use `git merge --abort` or `git rebase --abort` only when
 the user asks, the wrong base was used, or continuing would destroy work
 you cannot reconstruct. **Done when** you either continued or aborted
 with that reason stated.
6. **Run project checks.** Discover this repo's typecheck, owner tests, and
 formatter. Run the smallest set that covers the files you touched. Fix
 what the merge broke. **Done when** those checks pass, or you reported
 the failure and the command you ran.
7. **Finish.** Stage the resolutions. Continue with `git merge --continue`
 or `git rebase --continue`. Do not leave the tree mid-conflict. **Done
 when** `git status` shows no unmerged paths.

## Do not

- Do not rerun a check command that just failed unchanged.
- Do not put secrets from either side into the commit message or the reply.
- Do not force-push to finish a rebase unless the user asked.
