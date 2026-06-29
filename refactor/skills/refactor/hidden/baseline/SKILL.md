---
name: baseline
description: Capture the pre-refactor ground truth by detecting and running existing tests, lint, type checks, benchmarks, and size metrics before any code changes are made.
---

# Baseline

Create the single source of truth for later validation. Stop the workflow if the project is already failing required checks.

## Inputs

- `run_id`
- `optimization_target`: `speed`, `size`, or `speed+size`
- `tech_stack`
- `scope`
- `user_commands`: optional test, lint, type, benchmark, or build commands supplied by the user

## Procedure

1. Inspect repository metadata to discover commands:
   - Python: `pytest`, `ruff`, `flake8`, `mypy`, `pyright`, `pyproject.toml`
   - C/C++/CUDA: `cmake`, `ctest`, `make test`, `ninja test`, `clang-tidy`
   - Rust: `cargo test`, `cargo clippy`, `cargo bench`
   - TypeScript/JavaScript: `package.json` scripts, `npm test`, `eslint`, `tsc`
   - Go: `go test ./...`, `go test -bench`, `go vet`
   - Java: Maven or Gradle test/check tasks
2. Prefer user-provided commands over inferred commands.
3. Run required baseline checks:
   - Existing tests
   - Lint and type checks when configured
   - Benchmarks when `optimization_target` includes `speed`
   - Size metrics when `optimization_target` includes `size`
4. Record raw command, exit code, duration, and summarized output for each check.
5. If any required existing test fails, return `blocked` and do not proceed.

## Size Metrics

Choose the most relevant available metric:

- Binary or artifact size after the normal build
- Bundle size for web projects
- Source lines or byte count for code-size refactors
- Dependency footprint when the opportunity concerns dependency removal

## Output

Write `storage/workflows/<run_id>/baseline.json`:

```json
{
  "run_id": "refactor-YYYYMMDD-HHMMSS",
  "scope": "src",
  "commands": [],
  "tests": { "passed": true, "total": null, "failed": 0 },
  "lint": { "passed": true, "errors": 0, "warnings": 0 },
  "types": { "passed": true, "errors": 0 },
  "benchmark": { "available": false, "metrics": [] },
  "size": { "available": false, "metrics": [] },
  "blocked_reason": null
}
```

Return the baseline path, detected commands, and any checks that were unavailable.
