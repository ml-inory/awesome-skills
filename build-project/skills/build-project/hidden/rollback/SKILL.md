---
name: build-project-rollback
description: Roll back only the current build-project iteration while preserving unrelated worktree changes.
---

# build-project-rollback

Remove failed or abandoned iteration changes without touching unrelated work.

## Inputs

- `.build-state.json`
- `changed_files`
- Current iteration number `N`
- `gate_result`

## Procedure

1. Read `.build-state.json` and identify files intentionally changed in the current iteration.
2. Inspect `git status --short` and compare it with `pre_existing_changes`.
3. Revert only files that are both tracked in the current iteration and safe to restore.
4. Do not delete or modify files that predated the iteration or are ambiguous.
5. Comment on the issue with the rollback reason when GitHub access is available.
6. Update `.build-state.json` with rollback status and any files requiring user intervention.

## Outputs

- `rollback_status`: `complete`, `partial`, or `blocked`
- `rollback_summary`
