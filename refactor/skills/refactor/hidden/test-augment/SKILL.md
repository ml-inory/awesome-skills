---
name: test-augment
description: Add isolated tests for a completed refactor round without modifying existing test files, covering equivalence, edge cases, regression behavior, and measurable performance or size assumptions where practical.
---

# Test Augment

Add tests that protect the refactor. Existing tests are read-only.

## Inputs

- `run_id`
- `round_id`
- `opportunity`
- `changes_path`
- `tech_stack`

## Procedure

1. Inspect existing test layout and naming conventions.
2. Create a new test file near related tests. Do not edit existing test files.
3. Cover:
   - Behavior equivalence for representative inputs
   - Boundary cases affected by the refactor
   - Regression cases tied to the original inefficiency or bloat
   - API compatibility when the public surface is touched
4. Add performance or size assertions only when they are stable enough for the project environment. Prefer functional tests plus benchmark validation when timing is noisy.
5. Run the new test file when a local command is discoverable.
6. If the new test fails because the refactor is wrong, mark the round `needs_repair`.

## Output

Write `storage/workflows/<run_id>/rounds/<round_id>/new_tests.json`:

```json
{
  "opportunity_id": "OPP-001",
  "test_files": [],
  "test_count": 0,
  "categories": ["equivalence", "boundary"],
  "command": null,
  "passed": null,
  "needs_repair": false
}
```

Return created test files, command results, and any uncovered risk.
