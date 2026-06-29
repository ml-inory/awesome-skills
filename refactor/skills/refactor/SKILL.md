---
name: refactor
description: Safely refactor legacy or performance-sensitive codebases toward speed, size, or speed+size goals through an auditable baseline, scan, rank, one-change-at-a-time implementation, test augmentation, validation, and rollback workflow. Use when Codex is asked to improve runtime performance, reduce code or binary size, remove dead or duplicate code, simplify legacy code, or run an incremental refactoring campaign with measurable acceptance checks.
---

# Refactor

Run a conservative, measurable refactoring workflow. Optimize only toward the user's stated target and keep each round small enough to validate and roll back independently.

## Workflow Contract

Use [workflows/refactor.yaml](../../workflows/refactor.yaml) as the durable protocol for state, gates, retries, rollback, and completion. Treat the YAML as authoritative when step ordering or failure handling is unclear.

## Required Inputs

Collect or infer these fields before starting side effects:

- `optimization_target`: `speed`, `size`, or `speed+size`
- `tech_stack`: primary language or build ecosystem
- `scope`: target path, defaulting to the repository root
- `max_rounds`: maximum successful or attempted refactor rounds, defaulting to `10`
- `main_branch`: branch to return to after each round, inferred from the current git branch when safe

Ask the user only when a missing field materially affects correctness, safety, credentials, cost, or destructive operations. Record low-risk assumptions in the run summary.

## Hard Constraints

- Do not modify existing tests. Add new test files only.
- Do not change public APIs unless the user explicitly approves that scope.
- Do not continue if the baseline test suite fails.
- Do not keep a round unless all validation gates pass.
- Do not guess credentials, private services, deployment targets, or production permissions.
- Preserve unrelated user changes in the worktree.

## Execution

1. Run `hidden/baseline` to capture tests, lint/type status, benchmarks, and size metrics.
2. Run `hidden/scanner` in read-only mode to identify optimization opportunities.
3. Run `hidden/ranker` to create a dependency-aware execution queue.
4. For each queued opportunity until `max_rounds` or completion:
   - Run `hidden/refactor-one` for one minimal, API-compatible change.
   - Run `hidden/test-augment` to add isolated tests for that change.
   - Run `hidden/validator` to compare against the current baseline.
   - If validation fails, run `hidden/rollback` and continue only when the failure policy allows it.
   - If validation passes, preserve the round and update the baseline for the next round.

## Progress Reporting

Keep user-facing updates concise:

- Baseline status and blocking failures
- Number and type of opportunities found
- Current round, target file/function, and result
- Rollbacks with the gate that failed
- Final improvement, tests, lint/type status, and files changed

## Completion

Finish only when one of these conditions is true:

- At least one round passed and all final validation checks pass.
- No viable opportunities remain after scan/ranking.
- The workflow is blocked by missing user input, credentials, broken baseline, unsafe scope, or exhausted retry budget.

Return a summary with applied rounds, skipped or rolled-back rounds, measured improvements, new tests, assumptions, and remaining risks.
