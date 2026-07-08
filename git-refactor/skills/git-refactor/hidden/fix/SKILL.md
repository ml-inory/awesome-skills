---
name: git-refactor-fix
description: Apply the diagnosed fix to code or README, ensure both are consistent, create a git commit, and append entry to fix_log.
---

# fix

Apply the diagnosed fix to the project files, create a git commit with a descriptive message, and update the running fix log.

## Required Inputs

- `diagnosis`: The diagnosis object from `diagnose` containing `fix_targets`, `error_category`, `root_cause`.
- `project_dir`: Absolute path to the local project.

## Execution

1. For each fix_target in the diagnosis:
   a. Read the target file (code or README).
   b. Apply the fix:
      - **Code fix**: Edit the source file to correct the bug. Ensure imports, function calls, types, and logic are correct.
      - **README fix**: Edit README.md to correct misleading instructions, add missing steps, fix command syntax, or reorder steps.
   c. If a code fix changes behavior that the README describes, update the README to match.
   d. If a README fix changes expected behavior, check that the code still matches.
2. After all fixes for this diagnosis are applied:
   a. Stage all changed files: `git add <changed_files>`.
   b. Create a commit with a descriptive message:
      - Format: `fix: <brief description of what was fixed>`
      - Body (optional): Include root cause and files changed if non-obvious.
      - Example: `fix: add missing torch dependency to requirements.txt and README`
   c. Do NOT push.
3. Append a fix_log_entry to the running fix log (in-memory or a temp file):
   - `step_index`: which README step this fix relates to.
   - `error_category`: from diagnosis.
   - `root_cause`: from diagnosis.
   - `files_changed`: list of files modified.
   - `commit_hash`: the git commit SHA.
   - `commit_message`: the commit message.

## Outputs

```json
{
  "fix_commit": {
    "hash": "a1b2c3d",
    "message": "fix: add missing torch dependency to requirements.txt and README",
    "files_changed": ["requirements.txt", "README.md"]
  },
  "fix_log_entry": {
    "step_index": 1,
    "error_category": "code_bug",
    "root_cause": "Module 'torch' is imported but not declared as a dependency",
    "files_changed": ["requirements.txt", "README.md"],
    "commit_hash": "a1b2c3d",
    "commit_message": "fix: add missing torch dependency to requirements.txt and README"
  },
  "total_fixes_so_far": 1
}
```

## Failure Cases

- git conflict during add/commit: retry once with a fresh checkout of the file, then fail.
- File to fix does not exist: re-classify the target (maybe the file was renamed), or flag for user.
- Fix introduces a syntax error or obvious regression: roll back the commit and re-diagnose.

## Hard Constraints

- Do NOT push any commits.
- Do NOT force-push or amend commits already on remote branches.
- Each independent fix must be its own commit. Do not bundle multiple unrelated fixes.
- Keep fix_log entries in order and deduplicated.
