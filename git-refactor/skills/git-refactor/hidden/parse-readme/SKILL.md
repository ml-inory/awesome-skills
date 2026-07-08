---
name: git-refactor-parse-readme
description: Parse README.md into an ordered list of executable bash code blocks with line numbers and surrounding context.
---

# parse-readme

Extract all bash code blocks from README.md, preserving order and annotating with line numbers and the text immediately preceding each block for context.

## Required Inputs

- `readme_path`: Absolute path to README.md.

## Execution

1. Read README.md.
2. Find all fenced code blocks marked as ` ```bash ` or ` ```sh ` or simply ` ``` ` (when context suggests shell commands).
3. For each block:
   - Record: `index` (0-based order), `start_line`, `end_line`, `commands` (the raw text inside the block), `context` (the 1-3 lines of text immediately before the block in README).
4. Skip empty code blocks.
5. Return the ordered list.

## Outputs

```json
{
  "parsed_steps": [
    {
      "index": 0,
      "start_line": 42,
      "end_line": 47,
      "commands": "pip install -r requirements.txt",
      "context": "First, install the Python dependencies:"
    },
    {
      "index": 1,
      "start_line": 55,
      "end_line": 60,
      "commands": "python setup.py build",
      "context": "Then build the project:"
    }
  ],
  "total_steps": 2
}
```

## Failure Cases

- README.md has no fenced code blocks: report "No executable steps found in README" and fail.
- README.md cannot be read: report file read error and fail.

## Notes

- Multi-line commands within a single block are treated as one step (execute them as a single shell script).
- If a code block has no language tag but its content looks like shell commands (starts with `$`, contains `apt`, `pip`, `make`, `cmake`, etc.), include it as a bash block.
