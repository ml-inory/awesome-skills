---
name: git-refactor
description: Take a local GitHub project directory, follow its README to set up and run on an AX board via remote-infer, identify and fix all bugs/errors encountered, making the project runnable from scratch on board with minimal mental burden.
---

# git-refactor

Take a local project directory, follow its README step-by-step on an AX board, fix every bug and confusing instruction encountered, and produce a clean, runnable project with an auditable fix report.

## Workflow Contract

Use [workflows/git-refactor.yaml](../../workflows/git-refactor.yaml) as the durable protocol for state, gates, retries, failure handling, observability, and completion. Treat the YAML as authoritative when step ordering or failure handling is unclear.

## Trigger Conditions

Use this skill when the user wants to:
- Make a GitHub project runnable on an AX board from scratch
- Fix README errors or confusing instructions discovered during board execution
- Fix bugs encountered while following README steps on board
- Audit a project's "getting started on AX" experience

## Usage

```
$git-refactor [<project_directory>] [--chip AX650N|AX630C|AX650C]
```

- `project_directory`: Path to the local project. Defaults to current working directory.
- `--chip`: Optional chip filter. Default: auto-select priority AX650N > AX630C > AX650C.

## What It Does

1. **Init**: Creates feature branch `fix/run-on-ax-board` from the current branch.
2. **Parse**: Extracts all bash code blocks from README.md in order.
3. **Board**: Selects an available AX board via the internal dashboard.
4. **Execute Loop**: For each README step:
   - Executes it on the selected AX board via `$remote-infer`
   - If it succeeds → moves to next step
   - If it fails → auto-diagnoses root cause, auto-fixes (code or README), commits, re-verifies on board
   - Retries up to 3 times per step; after 3 failures, asks user for guidance
5. **End-to-End**: After all individual steps pass, runs the full README path end-to-end on a clean board state.
6. **Report**: Generates `README-fix-report.md` with one entry per fix (original issue → root cause → fix → verification). This file is NOT committed.

## Required Inputs

- `project_directory`: Path to a local project containing `README.md`. Defaults to CWD.
- `chip_filter`: Optional chip preference.

## Hard Constraints

- Do NOT push or force-push to any remote.
- Do NOT guess SSH credentials.
- Do NOT run destructive board commands without explicit user approval.
- Do NOT commit `README-fix-report.md`.
- Fix BOTH code and README to keep them consistent.
- Each independent fix must be its own git commit.

## Execution

1. Run `hidden/init` to validate project and create feature branch.
2. Run `hidden/parse-readme` to extract executable steps from README.
3. Run `hidden/select-board` from remote-infer to pick an AX board.
4. For each parsed step:
   a. Run `hidden/execute-step` to execute on board.
   b. If failure: run `hidden/diagnose` to classify and locate root cause.
   c. Run `hidden/fix` to apply the fix and commit.
   d. Run `hidden/verify` to re-execute and confirm the fix.
   e. Retry up to 3 times per step if verification still fails.
5. Run end-to-end validation on a clean board state.
6. Run `hidden/report` to generate `README-fix-report.md`.

## Progress Reporting

Keep user-facing updates concise:
- Selected board IP, chip, and hostname.
- Current step being executed (N of total, with the command shown).
- Step result (pass / fail with error snippet).
- Diagnosis result (README error vs code bug, root cause).
- Fix applied (files changed, commit message).
- Verification result.
- End-to-end result.
- Final report location.

## Completion

Finish only when one of these conditions is true:
- All README steps pass on board, end-to-end validation passes, report is generated.
- No AX board is available for any chip.
- User declines to provide required input at a blocked gate.
- An unrecoverable step failure occurs and user declines further fixes.
