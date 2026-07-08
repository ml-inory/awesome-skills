---
name: git-refactor-diagnose
description: Analyze a failed step: classify as README error, code bug, environment issue, cd context error, or output mismatch. Identify root cause and file locations.
---

# diagnose

Analyze the output of a failed README step to determine what went wrong and where the fix should be applied.

## Required Inputs

- `step_result`: The failure result from `execute-step` containing `stderr`, `stdout`, `exit_code`, `commands_executed`, `working_dir`, `output_matches_expectation`, `step_type`.
- `step`: The original parsed step including `context`, `expected_output_hint`, `working_dir`.
- `project_dir`: Absolute path to the local project.

## Execution

1. Parse the error from `stderr` (and `stdout` if stderr is empty).
2. If `output_matches_expectation` is `false` even with `exit_code == 0`:
   - The output doesn't match what README shows. The code might produce different output, or README example is stale.
   - Classify as `output_mismatch`.
3. Otherwise classify the error:
   - **README error**: Wrong command, missing flag, incorrect order, misleading wording, wrong working_dir described.
   - **code bug**: Syntax error, missing import, type error, logic error, incorrect API usage.
   - **cd context error**: Command failed because the README assumed a different current directory. Check if `step.working_dir` matches what the command needs.
   - **missing dependency**: Package/library/tool not installed and not in README.
   - **environment issue**: Board OS/config differs from README assumptions (Python version, system lib).
   - **file reference error**: Path in README or code doesn't exist.
   - **download failure**: git clone, wget, huggingface download failed (network, auth, URL wrong).
4. Identify root cause by searching the project codebase and matching error messages to source files.
5. Determine fix targets:
   - README error → fix README text/command/working_dir.
   - code bug → fix source file.
   - cd context error → fix README's cd instructions or add explicit cd to the step.
   - missing dependency → add to requirements.txt or README.
   - environment issue → add prerequisite instructions to README, or adapt code.
   - file reference error → fix path in README or code.
   - download failure → fix URL, add auth note, or suggest alternative source.

## Outputs

```json
{
  "error_category": "cd_context_error",
  "root_cause": "Step executes 'make -j4' but README's preceding cd command entered 'cpp/ax650' while CMakeLists.txt is in 'cpp/ax650/build'. The mkdir + cd build step should change the working_dir to build/ before cmake.",
  "fix_targets": [
    {
      "type": "readme",
      "line_start": 95,
      "line_end": 98,
      "issue": "cd build after mkdir is described but not reflected in subsequent step's context",
      "suggested_fix": "Explicitly note that all build commands run from cpp/ax650/build/"
    }
  ],
  "confidence": "high",
  "output_expected": "Built target ax_whisper",
  "output_actual": "make: *** No targets specified and no makefile found.  Stop.",
  "cascade_from_previous": false
}
```

## Failure Cases

- Cannot determine root cause: set confidence to "low" and flag for user.
- Error is transient / network-related: classify as "transient" and recommend retry without fix.
- Output mismatch but behavior is correct (output format changed): suggest updating README's expected output example.
