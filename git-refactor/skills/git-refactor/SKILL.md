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
2. **Parse**: Parses README.md intelligently:
   - Detects board vs x86 sections (e.g., whisper.axera has model export on x86, inference on board)
   - Tracks `cd` directory context across steps
   - Captures expected output examples for fuzzy verification
   - Classifies steps as `must_pass`, `download`, or `informational`
3. **Board**: Selects an available AX board via the internal dashboard.
4. **Execute Loop**: For each board-relevant README step:
   - Executes it on the selected AX board via `$remote-infer` with correct working directory
   - Compares output against README's expected output
   - If it fails → auto-diagnoses root cause, auto-fixes (code or README), commits, re-verifies
   - Retries up to 3 times per step; after 3 failures, asks user for guidance
5. **End-to-End**: After all individual steps pass, runs the full README path end-to-end on a clean board.
6. **Report**: Generates `README-fix-report.md` with one entry per fix. NOT committed.

## Supported README Patterns

Handles common AX project README structures like:
- **whisper.axera style**: separate x86 (model export) and board (build + inference) sections
- **YOLO.axera style**: model download → compile → run on board
- **Generic style**: single flat list of commands, all assumed board-side

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

## Progress Reporting

Keep user-facing updates concise:
- Selected board IP, chip, and hostname.
- Board section detection result (e.g., "Found x86 and board sections, targeting board only").
- Current step being executed (N of total, with step_type and command shown).
- Step result (pass / fail with error snippet, output vs expectation match).
- Working directory context changes.
- Diagnosis result (README error vs code bug, root cause).
- Fix applied (files changed, commit message).
- Verification result.
- Fix report location.

## Completion

Finish only when one of these conditions is true:
- All board-relevant README steps pass, end-to-end validation passes, report is generated.
- No AX board is available for any chip.
- User declines to provide required input at a blocked gate.
- An unrecoverable step failure occurs and user declines further fixes.
