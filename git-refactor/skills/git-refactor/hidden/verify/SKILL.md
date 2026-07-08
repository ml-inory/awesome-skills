---
name: git-refactor-verify
description: Re-execute the repaired step on the board to confirm the fix works. Update fix_log_entry with verification result.
---

# verify

Re-execute the previously failing README step on the AX board to confirm that the applied fix resolves the issue.

## Required Inputs

- `step`: The original parsed step (with its commands).
- `selected_board`: Board info from select-board.
- `project_dir`: Absolute path to the local project.
- `fix_log_entry`: The fix log entry from the `fix` step, to be updated with verification result.

## Execution

1. Re-run the step on the board using the same execution logic as `execute-step`.
   - If the step required file transfers, re-transfer updated files from `project_dir`.
   - Use the same remote working directory.
2. Compare the result:
   - If `exit_code == 0` and no fatal errors in stderr: verification passes.
   - If the error has changed (different error): the fix resolved the original issue but revealed a new one. Record this and mark verification as "partial". The new error will be diagnosed in the next iteration.
   - If the same error persists: verification fails. Return to diagnosis.
3. Update the fix_log_entry with:
   - `verification_result`: "passed", "partial", or "failed".
   - `verification_output`: key lines from stdout/stderr confirming success.

## Outputs

```json
{
  "verification_result": "passed",
  "step_index": 1,
  "verification_output": "Successfully installed numpy torch ...",
  "fix_log_entry_updated": true
}
```

On partial success:
```json
{
  "verification_result": "partial",
  "step_index": 1,
  "verification_output": "New error: ImportError: cannot import name 'functional' from 'torch'",
  "note": "Original ModuleNotFoundError resolved, but revealed API compatibility issue",
  "fix_log_entry_updated": true
}
```

## Failure Cases

- Board becomes unreachable mid-verification: retry once, then fail.
- Same error persists: mark verification as failed and return control to the step loop for re-diagnosis.
- New error appears: mark as "partial" so the loop handles it as a fresh diagnosis.

## Notes

- Verification should be fast. If the original step is long (e.g., model training), verify only the part that failed.
- Do NOT count a "partial" verification as a full retry against the step's retry budget. It's a new issue.
