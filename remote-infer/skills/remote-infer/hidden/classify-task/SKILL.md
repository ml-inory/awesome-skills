---
name: classify-task
description: 解析 remote-infer 用户任务，输出任务类型、所需输入、风险等级和验证方式
---

# classify-task（内部工序）

Classify the user's board task before selecting an execution path.

## Inputs

- `task_description`
- Optional `chip`
- Optional local or remote paths

## Task Classes

- `axmodel_inference`: `.axmodel` path or explicit inference request.
- `remote_command`: explicit command to run over SSH.
- `deploy`: copy files and start or update a service/process on the board.
- `upload`: local file or directory to remote board path.
- `download`: remote board file or directory to local path.
- `mount_local_to_board`: expose a local path to the board.
- `mount_board_to_local`: mount a board path locally.
- `unknown`: intent is unclear or unsafe to infer.

## Procedure

1. Parse the task description and extract paths, command text, chip filter, and validation hints.
2. Check whether required local paths exist for model, input, upload, or local mount tasks.
3. Mark risk as:
   - `low`: read-only command, inference, or non-overwriting transfer.
   - `medium`: deploy, long-running process, or filesystem mount.
   - `high`: destructive command, overwrite, privileged mount, service replacement, or unclear production exposure.
4. For `high` or `unknown`, ask the user before remote execution.
5. Output the task class, required inputs, validation method, and whether approval is needed.

## Outputs

- `task_class`
- `required_inputs`
- `risk_level`
- `approval_required`
- `validation_method`
