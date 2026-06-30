---
name: build-project-init
description: Initialize a build-project run after $grill-me requirement alignment by collecting the goal, detecting stack and validation commands, creating a feature branch, and writing .build-state.json.
---

# build-project-init

Initialize one auditable build-project run before code changes start.

Run this step only after the parent `build-project` skill has used `$grill-me` to align requirements with the user.

## Inputs

- `goal`: overall development goal.
- `stack`: optional primary technology stack.
- `base_branch`: optional PR target branch.
- `validation_command`: optional user-supplied validation command.
- `requirement_alignment`: summary of the `$grill-me` discussion, including resolved assumptions, open questions, acceptance checks, and first iteration scope.

## Procedure

1. Confirm `requirement_alignment` exists and records goal, non-goals, acceptance checks, validation approach, and first iteration scope. If it is missing or unresolved, return to `$grill-me` requirement alignment before creating a branch or writing files.
2. Confirm `goal` is known and matches the aligned requirement. Ask the user only if it cannot be extracted from the request or the alignment.
3. Inspect repository metadata in this order to infer `stack` and default validation:
   - `pyproject.toml` or `pytest.ini`: `python -m pytest -x -q`
   - `package.json` with `scripts.test`: `npm test -- --passWithNoTests`
   - `go.mod`: `go test ./...`
   - `Makefile` with a `test` target: `make test`
4. If no stack or validation command can be inferred, ask the user for the missing field.
5. Inspect `git status --short` and record pre-existing changes. Do not overwrite, stage, or revert unrelated work.
6. Create a feature branch named `feat/build-YYYYMMDD-HHMM` from the current branch unless already on a suitable feature branch.
7. Write `.build-state.json` with:
   - `goal`
   - `stack`
   - `base_branch`
   - `branch`
   - `iteration: 1`
   - `validation_command`
   - `requirement_alignment`
   - `issues: []`
   - `rounds: []`
   - `pre_existing_changes`
   - `assumptions`

## Outputs

- `build_state`: path to `.build-state.json`.
- `branch`: active feature branch.
- `stack`: detected or supplied stack.
- `validation_command`: detected or supplied command.
