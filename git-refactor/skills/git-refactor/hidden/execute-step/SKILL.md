---
name: git-refactor-execute-step
description: Execute one parsed README step on the selected AX board via remote-infer. Transfer required files if the step references local paths. Capture stdout, stderr, exit code.
---

# execute-step

Execute a single README step on the AX board using `$remote-infer`, handling file transfers when the step references local files.

## Required Inputs

- `step`: A parsed step object from `parse-readme` containing `commands`, `index`, `context`.
- `selected_board`: Board info from `select-board` (IP, hostname, chip).
- `project_dir`: Absolute path to the local project.

## Execution

1. Analyze the `commands` string for local file references:
   - Paths starting with `./`, `../`, or bare filenames that exist in `project_dir`.
   - Commands like `scp`, `cp`, `rsync` that reference local files.
2. If local files are referenced and need to be on the board:
   - Use `$remote-infer transfer-file` to upload the referenced files/directories to the board.
   - Place them in a reasonable remote path (e.g., `/tmp/git-refactor/<project_name>/`).
   - Adjust the commands to use the remote paths instead of local ones.
3. Execute the (possibly adjusted) commands on the board via `$remote-infer execute-ssh`.
   - Set a working directory on the board (e.g., `/tmp/git-refactor/<project_name>/`).
4. Capture and return: `stdout`, `stderr`, `exit_code`.

## Outputs

```json
{
  "index": 0,
  "commands_executed": "pip install -r requirements.txt",
  "exit_code": 0,
  "stdout": "Successfully installed numpy torch ...",
  "stderr": "",
  "success": true,
  "remote_workdir": "/tmp/git-refactor/project-name/",
  "transferred_files": []
}
```

On failure:
```json
{
  "index": 0,
  "commands_executed": "python setup.py build",
  "exit_code": 1,
  "stdout": "",
  "stderr": "ModuleNotFoundError: No module named 'torch'",
  "success": false,
  "remote_workdir": "/tmp/git-refactor/project-name/",
  "transferred_files": []
}
```

## Failure Cases

- SSH timeout / network failure: retry once, then fail.
- Command exits non-zero: return the failure result for diagnosis (this is expected behavior, not a workflow failure).
- File transfer fails: report and fail.

## Hard Constraints

- Do NOT execute destructive commands (rm -rf /, format, etc.) without user approval.
- Do NOT overwrite files on the board at non-temporary paths without approval.
- Use `/tmp/git-refactor/` as the default remote working base to avoid polluting the board.
