---
name: git-refactor-diagnose
description: Analyze a failed step: classify as README error, code bug, or environment issue; identify root cause and file locations.
---

# diagnose

Analyze the output of a failed README step to determine what went wrong and where the fix should be applied.

## Required Inputs

- `step_result`: The failure result from `execute-step` containing `stderr`, `exit_code`, `commands_executed`, `context`.
- `step`: The original parsed step including line numbers and README context.
- `project_dir`: Absolute path to the local project.

## Execution

1. Parse the error from `stderr` (and `stdout` if stderr is empty).
2. Classify the error into one of these categories:
   - **README error**: The README instruction is wrong, misleading, or incomplete (e.g., wrong command, missing flag, incorrect order, confusing wording).
   - **code bug**: The code itself has a bug (e.g., syntax error, missing import, type error, logic error, incorrect API usage).
   - **missing dependency**: A required package, library, or tool is not installed and not mentioned in README.
   - **environment issue**: The board OS/config differs from what the README assumes (e.g., wrong Python version, missing system library).
   - **file reference error**: A file path in the README or code does not exist.
3. Identify root cause by:
   - Searching the project codebase for the referenced command, file, module, or error message.
   - Examining the README context around the step for instructions that may have been missed.
   - Checking the previous step's success to rule out cascade failures.
4. For each category, determine the fix target:
   - README error → fix the README text/command.
   - code bug → fix the source code file.
   - missing dependency → add the dependency installation to README, or fix code to work without it.
   - environment issue → add prerequisite instructions to README, or adapt code.
   - file reference error → fix the path in README or code.
5. If the root cause is ambiguous (could be README OR code), prefer fixing both to ensure consistency.

## Outputs

```json
{
  "error_category": "code_bug",
  "root_cause": "Module 'torch' is imported but PyTorch was not installed as a dependency in requirements.txt.",
  "fix_targets": [
    {
      "type": "code",
      "file": "src/main.py",
      "line": 3,
      "issue": "import torch without declaring it in requirements.txt",
      "suggested_fix": "Add 'torch' to requirements.txt and add pip install line to README if missing"
    },
    {
      "type": "readme",
      "line_start": 42,
      "line_end": 47,
      "issue": "README does not mention installing dependencies before running",
      "suggested_fix": "Add 'pip install -r requirements.txt' step before the build step"
    }
  ],
  "confidence": "high",
  "cascade_from_previous": false
}
```

## Failure Cases

- Cannot determine root cause after searching codebase and error output: set confidence to "low" and flag for user.
- Error is transient / network-related: classify as "transient" and recommend retry without fix.

## Notes

- Prefer searching the codebase with `rg` or `grep` to find where the error originates.
- If the error message contains a file path and line number, start the search there.
- Cascade failures (step N fails because step N-1 wasn't done yet) should be flagged and not double-counted.
