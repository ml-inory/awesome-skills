---
name: execute-ssh
description: 在选定 AX 板上通过 SSH 执行命令或部署步骤，并记录命令、输出和退出码
---

# execute-ssh（内部工序）

Run a command or deploy step on the selected board.

## Inputs

- `board`: JSON with `ip`, `hostname`, and `chip_type`
- `command`
- SSH user, defaulting to `root`
- Approved SSH credential source
- `risk_level`

## Procedure

1. Refuse to run commands that are destructive, ambiguous, or unrelated to the requested task without explicit user approval.
2. Test connectivity:
   ```bash
   ssh -o BatchMode=yes root@<BOARD_IP> 'echo ok'
   ```
   If key auth is unavailable, ask for an approved credential path instead of guessing.
3. Run the command with a timeout appropriate to the task.
4. Capture stdout, stderr, and exit code.
5. For deploy tasks, run the declared validation command or a minimal process/port check when supplied.

## Outputs

- `remote_exit_code`
- `remote_stdout`
- `remote_stderr`
- `validation_status`
