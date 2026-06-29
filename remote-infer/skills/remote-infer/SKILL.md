---
name: remote-infer
description: 在内网找空闲 AX 板子，通过可审计的选板、连通性、任务分类、远程执行和验证流程完成推理、命令、传输或挂载任务
---

# remote-infer

Find an available AX board on the internal dashboard and run the user's board task through an auditable workflow.

## Workflow Contract

Use [workflows/remote-infer.yaml](../../workflows/remote-infer.yaml) as the durable protocol for state, gates, retries, failure handling, observability, and completion. Treat the YAML as authoritative when step ordering or failure handling is unclear.

## Trigger Conditions

Use this skill when the user mentions 板子, 找板子, 上板子, 跑一下, remote board, AX board, deploy on board, infer, ssh, scp, mount, or wants to run a task on an AX board.

## Usage

```
$remote-infer [--chip AX650N|AX630C|AX650C] <任务描述>
```

任务举例：
- 跑 axmodel 推理：`$remote-infer model.axmodel [--input data.npy]`
- 部署服务：`$remote-infer 部署 my-server`
- 挂载本地目录：`$remote-infer mount /local/path`
- 执行任意命令：`$remote-infer 执行 echo hello`

## Required Inputs

Collect or infer these fields before remote side effects:

- `task_description`: command, model path, transfer, mount, deploy, or other board task.
- `chip`: optional chip filter such as `AX650N`, `AX630C`, or `AX650C`.
- `auth`: SSH key or approved password path. Use existing SSH config when available.
- `local_paths`: required for model, input, upload, or mount tasks.
- `remote_paths`: required for upload, download, mount, deploy, or command tasks when not inferable.

Ask the user only when the missing value affects safety, credentials, destructive remote operations, filesystem mounts, or task correctness.

## Hard Constraints

- Do not guess credentials beyond existing SSH agent/config or an explicitly approved credential.
- Do not run destructive remote commands, format disks, kill unrelated services, overwrite files, or mount over non-empty paths without explicit user approval.
- Do not deploy, expose network services, or change long-running board state unless the task explicitly requires it.
- Prefer least-risk execution: inspect paths and connectivity before mutation.
- Record selected board IP, chip, hostname, task class, commands run, and validation result.

## Execution

1. Run `hidden/classify-task` to identify the task class and required inputs.
2. Run `hidden/select-board` to choose an available AX board, optionally filtered by chip.
3. Run the task path:
   - `axmodel_inference`: run `hidden/ensure-daemon`, then `hidden/run-model`.
   - `remote_command` or `deploy`: run `hidden/execute-ssh`.
   - `upload` or `download`: run `hidden/transfer-file`.
   - `mount_local_to_board` or `mount_board_to_local`: run `hidden/mount-path`.
4. Validate the task-specific result and report board information plus command/model output.

## Progress Reporting

Keep user-facing updates concise:

- Task class and required inputs.
- Selected board IP, chip, and hostname.
- Connectivity or daemon status.
- Remote command, transfer, mount, or inference status.
- Final output, artifacts, assumptions, and limitations.

## Completion

Finish only when one of these conditions is true:

- The requested task completes and task-specific validation passes.
- The workflow is blocked by no available board, missing credentials, missing files, unsafe command, unavailable dashboard, or unavailable dependencies.
- A recoverable failure exhausts the retry budget and any partial remote side effects are reported.
