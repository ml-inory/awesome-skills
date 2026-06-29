---
name: build-project-review-gate
description: Decide whether a build-project iteration should repair, redesign, force commit, continue, or finish with a PR.
---

# build-project-review-gate

Gate each iteration with explicit user-visible decisions.

## Inputs

- `.build-state.json`
- `test_status`
- `commit_hash`
- Current iteration number `N`
- `goal`

## Procedure

1. If `test_status=fail`, show the failure summary and ask the user to choose:
   - `retry_code`: repair the implementation and rerun tests.
   - `retry_spec`: abandon the current slice and create a smaller or clearer issue.
   - `force_commit`: commit despite failing tests.
   - `rollback`: abandon current uncommitted iteration changes.
2. If `test_status=blocked`, ask the user for the missing validation command or permission.
3. If `test_status=pass`, summarize the issue, commit hash, tests, and remaining goal scope.
4. Ask whether to:
   - `continue`: increment `N` and start another iteration.
   - `done`: create a PR and stop.
5. Update `.build-state.json` with the gate decision and rationale.

## Outputs

- `gate_result`: `continue`, `done`, `retry_code`, `retry_spec`, `force_commit`, `rollback`, or `blocked`
- Updated `.build-state.json`
