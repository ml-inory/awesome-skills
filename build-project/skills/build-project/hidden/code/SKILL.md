---
name: build-project-code
description: Implement one build-project iteration with the minimum scoped code changes required by the current issue.
---

# build-project-code

Implement only the current iteration's acceptance checks.

## Inputs

- `issue_number`
- `stack`
- `.build-state.json`

## Procedure

1. Read the issue with `gh issue view <issue_number>` and extract acceptance checks.
2. Inspect the relevant files and local project conventions before editing.
3. Implement the minimum necessary change.
4. Preserve unrelated user changes. Stage nothing in this step.
5. If the issue is ambiguous or blocked, comment on the issue with the blocker and ask the user.
6. Comment on the issue with a concise implementation summary:
   ```bash
   gh issue comment <issue_number> --body "## Implementation summary\n- Changed: <files>\n- Core logic: <one sentence>"
   ```
7. Update `.build-state.json` with the files intentionally changed during this iteration.

## Outputs

- `changed_files`
- `implementation_summary`
