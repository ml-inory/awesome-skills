---
name: git-refactor-parse-readme
description: Parse README.md into an ordered list of executable board-side steps, tracking directory context, expected outputs, and distinguishing x86-only from board steps.
---

# parse-readme

Parse README.md for an AX board project (like whisper.axera or YOLO.axera). Extract executable steps that should run ON THE BOARD, preserve directory context (`cd` commands), capture expected outputs for verification, and skip x86-only steps (model export, ONNX conversion, etc.).

## Required Inputs

- `readme_path`: Absolute path to README.md.

## Execution

1. Read README.md fully.
2. Identify the structural sections of the README. Look for markers like:
   - "## 开发板" / "## Board" / "## Run on Board" / "## 板端" → board steps start here
   - "## x86" / "## PC" / "## Model Export" / "## 模型转换" → x86-only, skip these
   - "## 目录结构" / "## Directory" → helps understand file layout
3. If no explicit board section marker, assume ALL steps are board steps.
4. Extract executable steps from the board section(s):
   - Fenced code blocks: ` ```bash `, ` ```sh `, ` ```shell `, or untagged ` ``` ` when content is clearly shell commands.
   - Inline commands: commands in body text that appear as standalone lines like `cd xxx`, `./build.sh`, `make -j4`.
   - Commands like `tree`, `cat`, `echo` used to show directory structure or config preview → include as informational (non-critical).
5. Track **directory context** across steps:
   - If a step contains `cd <path>`, record the new `working_dir` for subsequent steps.
   - The initial `working_dir` starts at the project root on the board (e.g., `/tmp/git-refactor/<project>/`).
   - When `cd ..` or absolute paths appear, update accordingly.
6. Capture **expected output** when README shows example terminal output after a command:
   - Look for text blocks immediately following a command that look like terminal output (pid, timestamps, metrics, formatted tables).
   - Record as `expected_output_hint` for each step.
7. Classify each step:
   - `must_pass`: critical for functionality (build, run, inference).
   - `informational`: nice-to-have (tree, cat config, echo).
   - `download`: git clone, wget, huggingface download.
8. Return the ordered list.

## Outputs

```json
{
  "parsed_steps": [
    {
      "index": 0,
      "start_line": 85,
      "end_line": 87,
      "commands": "git clone https://huggingface.co/xxx/model",
      "context": "First, download the model weights:",
      "working_dir": "/tmp/git-refactor/project/",
      "step_type": "download",
      "expected_output_hint": "Cloning into 'model'..."
    },
    {
      "index": 1,
      "start_line": 92,
      "end_line": 93,
      "commands": "cd cpp/ax650",
      "context": "Enter the C++ build directory:",
      "working_dir": "/tmp/git-refactor/project/cpp/ax650",
      "step_type": "must_pass",
      "expected_output_hint": null
    },
    {
      "index": 2,
      "start_line": 95,
      "end_line": 98,
      "commands": "mkdir build && cd build\ncmake .. -DCMAKE_TOOLCHAIN_FILE=../toolchain.cmake\nmake -j4",
      "context": "Configure and build with CMake:",
      "working_dir": "/tmp/git-refactor/project/cpp/ax650/build",
      "step_type": "must_pass",
      "expected_output_hint": "[100%] Built target ax_whisper"
    },
    {
      "index": 3,
      "start_line": 102,
      "end_line": 103,
      "commands": "./ax_whisper -m ../../model/whisper.axmodel -i ../../audio/test.wav",
      "context": "Run inference with a test audio file:",
      "working_dir": "/tmp/git-refactor/project/cpp/ax650/build",
      "step_type": "must_pass",
      "expected_output_hint": "Transcription: Hello world"
    }
  ],
  "total_steps": 4,
  "board_section_detected": true,
  "initial_working_dir": "/tmp/git-refactor/project/"
}
```

## Failure Cases

- README.md has no executable commands in board section: report "No board-executable steps found" and fail.
- README.md cannot be read: report file read error and fail.
- Cannot determine which section is board vs x86: assume all steps are board steps, record assumption in output.

## Notes

- Whisper.axera pattern: model export/ONNX conversion happens on x86, inference/build happens on board. Parse accordingly.
- `cd` commands are structural — they don't fail but set context for subsequent steps. Each `cd` step should update the persistent `working_dir`.
- Expected output hints are fuzzy — use them for "does this look right?" checks, not exact string matching.
