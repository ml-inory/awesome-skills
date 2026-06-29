---
name: refactor-one
description: Apply exactly one minimal, API-compatible refactoring opportunity from the ranked queue, preserving unrelated worktree changes and producing an auditable change summary.
---

# Refactor One

Implement one opportunity per round. Keep the diff focused enough that validation failure can be understood and rolled back.

## Inputs

- `run_id`
- `round_id`
- `opportunity`
- `tech_stack`
- `baseline_path`
- `main_branch`

## Procedure

1. Inspect git status before editing. Preserve unrelated user changes.
2. Create or switch to a round branch when branch operations are safe:
   - `refactor/<run_id>/<opportunity_id>`
3. Read the target code and direct callers/callees needed to protect behavior.
4. Confirm the public API contract:
   - Function, method, class, CLI, file format, and import path compatibility
   - Output semantics and error behavior
5. Apply the smallest useful change for the opportunity.
6. Avoid broad formatting, unrelated cleanup, dependency changes, or generated churn.
7. If the opportunity needs an API change, credentials, production access, or destructive migration, mark the round `blocked` instead of editing.

## Allowed Patterns

- Improve an algorithm or data structure locally.
- Remove demonstrably unused code when validation can prove safety.
- Deduplicate code through a local helper when it reduces complexity without changing API.
- Replace repeated work with caching only when cache lifetime and invalidation are clear.
- Reduce bundle or binary size by removing unused imports, features, or dependencies only when tests/build can validate it.

## Output

Write `storage/workflows/<run_id>/rounds/<round_id>/changes.json`:

```json
{
  "opportunity_id": "OPP-001",
  "branch": "refactor/refactor-YYYYMMDD-HHMMSS/OPP-001",
  "files_modified": [],
  "summary": "",
  "api_compatible": true,
  "blocked_reason": null
}
```

Return changed files and the change summary.
