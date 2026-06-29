---
name: build-project-commit
description: Commit one validated build-project iteration without staging unrelated files.
---

# build-project-commit

Create one reviewable commit for the current iteration.

## Inputs

- `issue_number`
- `issue_title`
- `changed_files`
- `test_status`
- Current iteration number `N`

## Preconditions

Run this step only when `test_status=pass`, or when the user explicitly chose `force_commit` at the review gate.

## Procedure

1. Inspect `git status --short`.
2. Stage only files listed in `changed_files`. Do not use `git add .`.
3. Commit with a Conventional Commit message:
   ```bash
   git commit -m "feat(iter-N): <issue title> (<issue_number>)"
   ```
4. Update the issue acceptance checklist when supported by the available GitHub tooling.
5. Comment on the issue with commit hash, branch, and test status.
6. Append the round summary to `.build-state.json`.

## Outputs

- `commit_hash`
- Updated `.build-state.json`
