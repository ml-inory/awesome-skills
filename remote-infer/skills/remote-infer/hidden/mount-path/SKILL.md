---
name: mount-path
description: 在本机和 AX 板之间建立挂载路径，要求显式路径、权限和安全检查
---

# mount-path（内部工序）

Mount a local path to the board or a board path to the local machine.

## Inputs

- `mount_direction`: `local_to_board` or `board_to_local`
- `local_path`
- `remote_path`
- `board`
- Approved SSH credential source

## Procedure

1. Treat all mount tasks as at least `medium` risk.
2. Validate local and remote paths before mounting.
3. Refuse to mount over a non-empty destination unless the user explicitly approves it.
4. For `board_to_local`, prefer `sshfs`:
   ```bash
   sshfs root@<BOARD_IP>:<remote_path> <local_path>
   ```
5. For `local_to_board`, require an explicit method from the user or environment, such as NFS export details. Do not invent local network export settings.
6. Verify the mount is visible with `mount` or a read-only directory listing.

## Outputs

- `mount_status`
- `mount_point`
- `verification_summary`
