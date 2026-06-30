---
name: build-project
description: 先通过 $grill-me 与用户对齐需求，再小步迭代地把开发目标拆成初始化、需求切片、编码、测试、提交、评审和 PR 交付循环，适用于用户要求开始开发、build 或提出新的开发目标时
---

# build-project

小步迭代的需求切片 -> 编码 -> 测试 -> 提交 -> 评审循环，直到目标达成并创建 PR。

## Workflow Contract

Use [workflows/build-project.yaml](../../workflows/build-project.yaml) as the durable protocol for state, gates, retries, rollback, observability, and completion. Treat the YAML as authoritative when step ordering or failure handling is unclear.

## Trigger Conditions

Use this skill when the user says "开始开发", "build", `$build-project`, `/build-project`, or gives a new development goal that should be implemented in small, reviewable iterations.

## Required Inputs

Before starting side effects, use the `$grill-me` skill to reach shared understanding with the user. Ask one question at a time, provide the recommended answer for each question, and explore the codebase instead of asking when the answer can be discovered locally.

Resolve at least these decisions before `hidden/init` runs:

- goal and non-goals
- expected user-visible behavior
- constraints, risks, and external side effects
- acceptance checks and validation command
- first iteration scope and likely follow-up iterations

Collect or infer these fields during that alignment:

- `goal`: the overall development goal.
- `stack`: primary language or build ecosystem. Infer from `pyproject.toml`, `package.json`, `go.mod`, or `Makefile` when safe.
- `base_branch`: target branch for the PR, defaulting to the repository default branch or `main`.
- `validation_command`: test command, inferred from repository metadata when safe.

Ask the user whenever the `$grill-me` alignment has not resolved a decision that materially affects correctness, safety, credentials, external side effects, or destructive operations. Record resolved assumptions and remaining open questions in `.build-state.json` and the final response.

## Hard Constraints

- Preserve unrelated user changes in the worktree.
- Keep each iteration small enough for a single reviewable commit.
- Do not run deployment, publishing, paid, or production operations.
- Do not force-commit failed tests unless the user explicitly chooses that path at the review gate.
- Do not automatically merge the PR.
- Do not guess missing GitHub credentials, repository permissions, or private service access.

## Execution

1. Use `$grill-me` to complete requirement alignment before any branch creation, file edits, issue creation, or `.build-state.json` writes.
2. Run `hidden/init` to validate prerequisites, create a feature branch, and initialize `.build-state.json`.
3. For each iteration:
   - Run `hidden/spec` to create or record one small issue with acceptance checks.
   - Run `hidden/code` to implement the minimum scoped change.
   - Run `hidden/test` to execute the inferred or supplied validation command.
   - Run `hidden/commit` only when tests pass or the user explicitly approves a force commit.
   - Run `hidden/review-gate` to decide whether to continue, repair, redesign the iteration, force commit, or finish.
4. When the review gate returns `done`, run `hidden/merge` to create a PR and stop before merging.
5. If an iteration must be abandoned, run `hidden/rollback` to remove only that iteration's uncommitted or explicitly tracked changes while preserving unrelated work.

## Progress Reporting

Keep user-facing updates concise:

- Initialization result, branch name, and detected stack.
- Current iteration number, issue title, and acceptance checks.
- Files changed and implementation summary.
- Test command and pass/fail status.
- Commit hash, review-gate decision, and PR URL.

## Completion

Finish only when one of these conditions is true:

- A PR is created and all retained commits are represented in `.build-state.json`.
- The workflow is blocked by missing goal, stack, test command, GitHub access, repository permission, or unsafe scope.
- The retry budget is exhausted and rollback has completed or requires user intervention.

Return a summary with the branch, issues, commits, validation status, PR URL when available, assumptions, and remaining risks.
