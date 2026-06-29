---
name: build-project-init
description: Initialize a build-project run by collecting the goal, detecting stack and validation commands, creating a feature branch, and writing .build-state.json.
---

# build-project-init

Initialize one auditable build-project run before code changes start.

## Inputs

- `goal`: overall development goal.
- `stack`: optional primary technology stack.
- `base_branch`: optional PR target branch.
- `validation_command`: optional user-supplied validation command.

## Procedure

1. Confirm `goal` is known. Ask the user only if it cannot be extracted from the request.
2. Inspect repository metadata in this order to infer `stack` and default validation:
   - `pyproject.toml` or `pytest.ini`: `python -m pytest -x -q`
   - `package.json` with `scripts.test`: `npm test -- --passWithNoTests`
   - `go.mod`: `go test ./...`
   - `Makefile` with a `test` target: `make test`
3. If no stack or validation command can be inferred, ask the user for the missing field.
4. Inspect `git status --short` and record pre-existing changes. Do not overwrite, stage, or revert unrelated work.
5. Create a feature branch named `feat/build-YYYYMMDD-HHMM` from the current branch unless already on a suitable feature branch.
6. Write `.build-state.json` with:
   - `goal`
   - `stack`
   - `base_branch`
   - `branch`
   - `iteration: 1`
   - `validation_command`
   - `issues: []`
   - `rounds: []`
   - `pre_existing_changes`
   - `assumptions`

## Outputs

- `build_state`: path to `.build-state.json`.
- `branch`: active feature branch.
- `stack`: detected or supplied stack.
- `validation_command`: detected or supplied command.
