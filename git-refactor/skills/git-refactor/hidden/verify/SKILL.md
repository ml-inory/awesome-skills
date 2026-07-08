---
name: git-refactor-verify
description: Re-execute the repaired step on the board at the correct working_dir, compare output against README expectations, and update fix_log_entry.
---

# verify

Re-execute the previously failing README step on the AX board to confirm that the applied fix resolves the issue. Use the correct working directory and compare output against README expectations.

## Required Inputs

- `step`: The original parsed step (with `commands`, `working_dir`, `step_type`, `expected_output_hint`).
- `selected_board`: Board info from select-board.
- `project_dir`: Absolute path to the local project.
- `fix_log_entry`: The fix log entry from the `fix` step, to be updated with verification result.

## Execution

1. Re-run the step on the board using the same logic as `execute-step`:
   - Use `step.working_dir` as the execution context.
   - If the fix changed local files, re-transfer updated files to `/tmp/git-refactor/<project>/` on the board.
   - Execute: `cd <working_dir> && <commands>`.
2. Compare the result:
   - **Pass**: `exit_code == 0`, no fatal errors, and `output_matches_expectation` is `true` or `partial`.
   - **Partial**: The original error is gone, but a new error appeared OR output doesn't match expectations. Mark as "partial" — the new issue will be diagnosed separately.
   - **Fail**: The same error persists. Return to diagnosis.
3. If `step_type` is `informational`, pass on exit_code 0 regardless of output match.
4. Update fix_log_entry with verification status and notes.

## Outputs

```json
{
  "verification_result": "passed",
  "step_index": 3,
  "output_matches_expectation": true,
  "verification_output": "[100%] Built target ax_whisper",
  "fix_log_entry_updated": true
}
```

On partial success:
```json
{
  "verification_result": "partial",
  "step_index": 3,
  "output_matches_expectation": false,
  "verification_output": "Build succeeded but output format differs from README: shows 'Built target whisper' vs expected 'Built target ax_whisper'",
  "note": "Build passes but README expected output example may be stale",
  "fix_log_entry_updated": true
}
```

## Failure Cases

- Board unreachable: retry once, then fail.
- Same error persists: mark as failed, return to diagnosis loop.
- New error: mark as partial, route to fresh diagnosis.

## Notes

- Verification should use the same `working_dir` as the original step.
- If the fix added a dependency (e.g., pip install), the verify step must include installing it first before re-running the failing command.
- Do NOT count "partial" verifications against the step's retry budget — they represent new, distinct issues.
