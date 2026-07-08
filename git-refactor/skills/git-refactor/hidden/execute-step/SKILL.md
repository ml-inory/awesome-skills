---
name: git-refactor-execute-step
description: Execute one parsed README step on the selected AX board, maintaining persistent working directory, handling model downloads, and optionally comparing output against README expectations.
---

# execute-step

Execute a single README step on the AX board using `$remote-infer execute-ssh`. Maintain a persistent working directory across steps so `cd` context is preserved. Handle model downloads, file transfers, and compare actual output against README's expected output.

## Required Inputs

- `step`: Parsed step from `parse-readme` containing `commands`, `index`, `working_dir`, `step_type`, `expected_output_hint`.
- `selected_board`: Board info from `select-board` (IP, hostname, chip).
- `project_dir`: Absolute path to the local project.

## Execution

### 1. Determine working directory

- Use `step.working_dir` as the remote working directory for this step.
- If this is the first step and `working_dir` doesn't exist on board yet, create it:
  ```
  mkdir -p /tmp/git-refactor/<project_name>/
  ```
- If the step contains `cd <path>`, the changed directory only affects THIS step's execution context on the board. The next step will use its own `working_dir` as parsed.

### 2. Handle step_type

- **download**: Execute `git clone`, `wget`, `huggingface-cli download`, etc. directly on the board. These may take longer.
- **must_pass**: Standard execution. Failure triggers diagnosis.
- **informational**: Execute but don't fail the workflow on non-zero exit. Record output for context.

### 3. Handle model files

- If the step references `.axmodel` files, check if they exist in `project_dir` and need transferring.
- Use `$remote-infer transfer-file` to upload model files to `/tmp/git-refactor/<project>/model/` on the board.
- If model files are expected to be downloaded (huggingface, git lfs), execute the download on board directly.

### 4. Execute on board

- Run `step.commands` via `$remote-infer execute-ssh` with `working_dir` prepended:
  ```
  cd <working_dir> && <commands>
  ```
- For multi-line commands within a single step, execute as a shell script block.
- Capture: `stdout`, `stderr`, `exit_code`.

### 5. Compare output

- If `expected_output_hint` is set, check if key phrases from it appear in `stdout` or `stderr`.
- This is a fuzzy match — look for key tokens (e.g., "Built target", "Transcription:", "100%").
- Record the comparison as `output_matches_expectation`: `true`, `partial`, or `false`.

### 6. Update state

- Record the effective `working_dir` for audit trail.
- If the step was a `cd` step without other commands, update the board-side working directory pointer.

## Outputs

```json
{
  "index": 2,
  "commands_executed": "cd /tmp/git-refactor/whisper/cpp/ax650/build && cmake .. && make -j4",
  "exit_code": 0,
  "stdout": "[100%] Built target ax_whisper",
  "stderr": "",
  "success": true,
  "step_type": "must_pass",
  "working_dir": "/tmp/git-refactor/whisper/cpp/ax650/build",
  "output_matches_expectation": true,
  "expectation_keywords_found": ["Built target", "ax_whisper"],
  "transferred_files": [],
  "remote_duration_seconds": 45.2
}
```

## Failure Cases

- SSH timeout / network failure: retry once, then fail.
- `must_pass` exits non-zero: return the failure result for diagnosis.
- `download` step fails (e.g., huggingface unreachable, git clone failed): treat as `must_pass` failure.
- `informational` step fails: record but don't block progress.
- File transfer fails: report and fail.

## Hard Constraints

- Do NOT execute destructive commands (rm -rf /, format, etc.) without user approval.
- Do NOT overwrite files on the board outside `/tmp/git-refactor/` without approval.
- All board-side work goes under `/tmp/git-refactor/<project_name>/`.
