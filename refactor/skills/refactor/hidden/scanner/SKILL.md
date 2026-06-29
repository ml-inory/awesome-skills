---
name: scanner
description: Read-only scan of the target codebase to identify speed or size refactoring opportunities with location, evidence, risk, confidence, dependencies, and expected validation metric.
---

# Scanner

Find candidate opportunities without changing files. Favor evidence-backed opportunities over broad style cleanup.

## Inputs

- `run_id`
- `optimization_target`
- `tech_stack`
- `scope`
- `baseline_path`

## Procedure

1. Read the baseline summary and inspect only files in `scope`.
2. Identify opportunities relevant to the target:
   - `speed`: hot functions, unnecessary allocations or copies, repeated work, inefficient data structures, avoidable I/O, poor algorithmic complexity
   - `size`: dead code, duplicate code, unused exports/imports, redundant dependencies, over-abstraction, generated or bundled bloat
3. For each opportunity, collect direct evidence:
   - File and line
   - Function, module, class, command, or artifact affected
   - Baseline metric that can validate the change
   - Expected improvement range
4. Assign `risk`, `confidence`, and `dependencies`.
5. Exclude opportunities that require unapproved API changes, production credentials, broad rewrites, or unclear validation.

## Output

Write `storage/workflows/<run_id>/opportunities.json`:

```json
[
  {
    "id": "OPP-001",
    "target": "speed",
    "category": "algorithmic_complexity",
    "file": "src/example.py",
    "line_range": [40, 78],
    "symbol": "process_items",
    "evidence": "Nested lookup inside loop; benchmark shows this path dominates runtime.",
    "expected_metric": "benchmark.process_items.ms",
    "estimated_improvement_pct": [20, 60],
    "risk": "low",
    "confidence": "high",
    "dependencies": [],
    "requires_user_approval": false
  }
]
```

Return the opportunity count, skipped categories, and any validation gaps.
