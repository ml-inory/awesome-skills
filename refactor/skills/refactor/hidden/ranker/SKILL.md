---
name: ranker
description: Rank scanned refactoring opportunities by expected return, confidence, risk, dependency order, and validation clarity to produce the execution queue for the refactor workflow.
---

# Ranker

Create a small, dependency-aware queue that starts with high-confidence, low-risk work.

## Inputs

- `run_id`
- `optimization_target`
- `opportunities_path`
- `max_rounds`

## Scoring

Calculate a score for each opportunity:

```text
score = improvement_midpoint * confidence_weight * validation_weight / (risk_weight + dependency_penalty)
```

Weights:

- `confidence`: high `1.0`, medium `0.6`, low `0.3`
- `risk`: low `0.5`, medium `1.0`, high `2.0`
- `validation`: direct metric `1.0`, proxy metric `0.6`, unclear `0.0`
- `dependency_penalty`: `0.2` per unresolved dependency

Reject opportunities with unclear validation, high risk without approval, or missing dependencies.

## Ordering Rules

1. Topologically order dependencies before dependents.
2. Sort independent opportunities by descending score.
3. Prefer smaller diffs when scores are close.
4. Limit the active queue to `max_rounds`, but preserve the full ranked list for audit.

## Output

Write `storage/workflows/<run_id>/execution_queue.json`:

```json
{
  "queue": [
    {
      "rank": 1,
      "id": "OPP-001",
      "score": 42.0,
      "reason": "High confidence, low risk, direct benchmark metric."
    }
  ],
  "deferred": [],
  "rejected": []
}
```

Return the queue path and the first candidate.
