---
name: build-project-spec
description: Slice the overall development goal into one small issue with acceptance checks for the current iteration.
---

# build-project-spec

Create the smallest reviewable unit for the current iteration.

## Inputs

- `.build-state.json`
- Current iteration number `N`
- Previous `rounds` and `issues`

## Procedure

1. Read `.build-state.json` and summarize completed rounds.
2. Choose one minimal deliverable that advances `goal` and can be reviewed as a single commit.
3. Define acceptance checks that are concrete and testable.
4. Prefer creating a GitHub issue with `gh issue create`:
   ```bash
   gh issue create \
     --title "feat[N]: <one-line iteration title>" \
     --body "## Goal\n<description>\n\n## Acceptance\n- [ ] <check 1>\n- [ ] <check 2>\n\n## Notes\nIteration N for: <goal>"
   ```
5. If `gh` or GitHub permissions are unavailable, stop as blocked unless the workflow invocation explicitly allows degraded local issue artifacts.
6. Append the returned issue number, title, and acceptance checks to `.build-state.json`.

## Outputs

- `issue_number`
- `issue_title`
- `acceptance_checks`
