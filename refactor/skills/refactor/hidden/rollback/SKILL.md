---
name: rollback
description: Roll back a failed refactor round by reverting only that round's changes, cleaning newly added tests from the failed branch, preserving unrelated user work, and recording the failure reason.
---

# Rollback

Restore the repository to the state before the failed round without touching unrelated user changes.

## Inputs

- `run_id`
- `round_id`
- `opportunity_id`
- `branch`
- `main_branch`
- `validation_path`
- `changes_path`

## Procedure

1. Read validation and change summaries to identify files touched by the failed round.
2. Inspect git status and separate round changes from unrelated user changes.
3. Revert only the round's tracked changes.
4. Remove newly created test files from the failed round only.
5. Delete the round branch only when it is safe and no unrelated work is present there.
6. Record the rollback result and failure class.
7. Return control to the entry workflow:
   - Continue to the next opportunity after isolated validation failures.
   - Stop after three consecutive failed rounds.
   - Stop immediately for unsafe or blocked failures.

## Prohibited Commands

Do not run destructive broad commands such as `git reset --hard`, `git checkout -- .`, or `git clean -fd` unless the user explicitly approves and unrelated changes have been ruled out.

## Output

Write `storage/workflows/<run_id>/rounds/<round_id>/rollback.json`:

```json
{
  "opportunity_id": "OPP-001",
  "status": "rolled_back",
  "files_reverted": [],
  "test_files_removed": [],
  "branch_deleted": null,
  "failure_class": "recoverable",
  "reason": ""
}
```

Return rollback status and whether the workflow may continue.
