---
name: build-project-merge
description: Create a pull request for a completed build-project run and stop before merging.
---

# build-project-merge

Create the final PR handoff. Do not merge automatically.

## Inputs

- `.build-state.json`
- `base_branch`
- Feature branch

## Procedure

1. Read `.build-state.json` and summarize all iterations, issues, commits, and validation results.
2. Confirm there are no unstaged intended changes for the completed run.
3. Build a PR body with:
   - overall goal
   - iteration table
   - validation summary
   - linked issues
   - assumptions and known limitations
4. Create a PR:
   ```bash
   gh pr create \
     --base <base_branch> \
     --title "feat: <goal>" \
     --body "<generated body>"
   ```
5. Record the PR URL in `.build-state.json`.
6. Leave `.build-state.json` until the final response has reported the PR URL and audit summary, then remove it only if no follow-up step needs it.

## Outputs

- `pr_url`
- Final run summary
