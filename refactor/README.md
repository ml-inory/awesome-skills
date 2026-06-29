# Refactor Skill

A Codex skill for safely improving legacy or performance-sensitive codebases toward `speed`, `size`, or `speed+size` goals.

The skill is designed as an auditable workflow: capture a clean baseline, scan for opportunities, rank them, apply one small change at a time, add isolated tests, validate measurable improvement, and roll back failed rounds.

## Layout

```text
skills/
  refactor/
    SKILL.md
    hidden/
      baseline/SKILL.md
      scanner/SKILL.md
      ranker/SKILL.md
      refactor-one/SKILL.md
      test-augment/SKILL.md
      validator/SKILL.md
      rollback/SKILL.md
workflows/
  refactor.yaml
```

## Workflow

```text
baseline -> scanner -> ranker -> [refactor-one -> test-augment -> validator] x N
                                      |                                  |
                                      +----------- rollback on failure <-+
```

## Guarantees

- Existing tests are read-only. The workflow may add new test files, but must not modify existing tests.
- Every accepted round must pass the full validation gate.
- Each accepted round must show a measurable speed or size improvement, or a documented accepted validation proxy.
- Failed rounds are rolled back without touching unrelated user worktree changes.
- Public APIs remain compatible unless the user explicitly approves otherwise.

## Inputs

- `optimization_target`: `speed`, `size`, or `speed+size`
- `tech_stack`: primary language or build ecosystem
- `scope`: optional path to refactor, defaulting to the repository root
- `max_rounds`: optional round limit, defaulting to `10`
- `user_commands`: optional test, lint, type, benchmark, or build commands

## Outputs

During a run, audit artifacts are written under `storage/workflows/<run_id>/`:

- `baseline.json`
- `opportunities.json`
- `execution_queue.json`
- per-round `changes.json`
- per-round `new_tests.json`
- per-round `validation.json`
- per-round `rollback.json` when rollback is needed

The durable workflow contract is [workflows/refactor.yaml](workflows/refactor.yaml).
