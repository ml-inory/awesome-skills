# Refactor

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for **safely and incrementally refactoring legacy codebases** toward a specific optimization target (speed, size, or both).

## Features

- **Goal-driven** - Specify `speed`, `size`, or `speed+size` as your optimization target
- **Multi-language** - Supports Python, C++, CUDA, Rust, TypeScript, Go, Java
- **Test-safe** - Existing tests are **read-only**; only new tests are added
- **Incremental** - One optimization per round, each validated before proceeding
- **Auto-rollback** - Failed rounds are automatically reverted; 3 consecutive failures pause the workflow

## Pipeline

```
baseline --> scanner --> ranker --> [refactor_one --> test_augment --> validator] x N
                                         ^______ rollback on failure ________|
```

| Step | Description |
|------|-------------|
| **baseline** | Capture test results, lint status, benchmarks, and code size as ground truth |
| **scanner** | Identify all optimization opportunities (hot functions, dead code, O(n^2) loops, etc.) |
| **ranker** | Sort opportunities by ROI (high improvement + low risk first) |
| **refactor_one** | Apply a single refactoring on an isolated git branch |
| **test_augment** | Add new tests for the refactored code (never modify existing tests) |
| **validator** | Triple gate: all tests pass + measurable improvement + no new lint errors |
| **rollback** | Clean revert on validation failure |

## Installation

Copy the `skills/` directory into your project's `.claude/skills/`:

```bash
# Clone the repo
git clone https://github.com/user/Refactor.git

# Copy skills into your project
cp -r Refactor/skills/refactor/ /path/to/your-project/.claude/skills/refactor/
```

Your project should look like:

```
your-project/
├── .claude/
│   └── skills/
│       └── refactor/
│           ├── SKILL.md          # Entry point (visible to user)
│           └── hidden/
│               ├── baseline/
│               ├── scanner/
│               ├── ranker/
│               ├── refactor_one/
│               ├── test_augment/
│               ├── validator/
│               └── rollback/
├── src/
│   └── ...
└── tests/
    └── ...
```

## Usage

In Claude Code, run:

```
/refactor
```

Claude will interactively ask you to configure:

| Setting | Description | Options |
|---------|-------------|---------|
| Optimization target | What to optimize for | `speed` / `size` / `speed+size` |
| Tech stack | Target language | `python`, `cpp`, `cuda`, `rust`, `typescript`, `go`, `java` |
| Scope | Limit to subdirectory (optional) | Any path, defaults to entire project |
| Max rounds | Max refactoring iterations (optional) | Defaults to 10 |

You can also pass arguments directly to skip the prompts:

```
/refactor speed python --scope src/ --max-rounds 5
```

## Constraints

These rules are enforced at every round:

1. **Existing tests are read-only.** Never modify any existing test file. Only add new test files.
2. **All existing tests must pass** before proceeding to the next round.
3. **Each round must show quantifiable improvement**, or it gets rolled back.
4. **No new lint/type errors** may be introduced.

## Example Output

```
Refactor Summary
================
Target:       speed
Tech Stack:   python
Rounds:       7/10 (3 rolled back)
Improvements:
  - module_a.process(): 340ms -> 120ms (-65%)
  - module_b.parse():   89ms  ->  41ms (-54%)
  - ...
Tests: 142 passed (12 new)
Lint:  0 new errors
```

## Project Structure

```
skills/
  refactor/
    SKILL.md                # Entry skill (user-facing)
    hidden/                 # Internal pipeline steps (not user-facing)
      baseline/SKILL.md     # Capture baseline snapshot
      scanner/SKILL.md      # Scan for optimization opportunities
      ranker/SKILL.md       # Rank by ROI
      refactor_one/SKILL.md # Execute single-point refactoring
      test_augment/SKILL.md # Add new tests (never modify existing)
      validator/SKILL.md    # Triple validation gate
      rollback/SKILL.md     # Revert on failure
```

## License

MIT
