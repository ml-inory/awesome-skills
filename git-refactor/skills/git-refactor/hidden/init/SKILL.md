---
name: git-refactor-init
description: Validate project directory, confirm README.md exists, create feature branch 'fix/run-on-ax-board' from current branch, and record initial state.
---

# init

Validate that the target directory is a real project with a README, then create a feature branch for the refactor work.

## Required Inputs

- `project_dir`: Path to the project directory. Defaults to current working directory.

## Execution

1. Resolve `project_dir` to an absolute path (default to `$CWD`).
2. Verify the directory exists and contains `README.md`.
3. Verify git is available and the directory is a git repository.
4. Record the current branch name as `original_branch`.
5. Create and checkout a new branch: `fix/run-on-ax-board`.
   - If the branch already exists locally, checkout with `git checkout fix/run-on-ax-board`.
   - Do NOT push to remote.
6. Confirm the working tree is clean (no uncommitted changes unrelated to the refactor).

## Outputs

```json
{
  "init_status": "ok",
  "original_branch": "main",
  "project_dir": "/absolute/path/to/project",
  "readme_path": "/absolute/path/to/project/README.md"
}
```

## Failure Cases

- `project_dir` does not exist: report "Project directory not found" and ask user.
- `README.md` not found: report "No README.md found in project root" and ask user.
- Not a git repo: report "Directory is not a git repository" and ask user.
- Working tree is dirty: warn user about uncommitted changes but proceed.

## Hard Constraints

- Do NOT push any branch to remote.
- Do NOT delete or rename any existing files during init.
- Record `original_branch` so the workflow knows where to return if needed.
