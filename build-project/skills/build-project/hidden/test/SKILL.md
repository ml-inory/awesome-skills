---
name: build-project-test
description: Run validation for a build-project iteration and record pass/fail evidence.
---

# build-project-test

Validate the current iteration with the inferred or supplied test command.

## Inputs

- `.build-state.json`
- `issue_number`
- `validation_command`
- `changed_files`

## Procedure

1. Use the `validation_command` from `.build-state.json` unless the user supplied a replacement.
2. Run the command and capture the full output.
3. Classify the result:
   - `pass`: all required checks passed.
   - `fail`: one or more required checks failed.
   - `blocked`: no validation command is known.
4. On failure, comment on the current issue with a concise failure summary and the relevant command output.
5. Update `.build-state.json` with `test_status`, command, and summary.

## Outputs

- `test_status`: `pass`, `fail`, or `blocked`
- `test_command`
- `test_summary`
