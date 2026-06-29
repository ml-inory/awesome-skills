---
name: transfer-file
description: 在本机和选定 AX 板之间传输文件或目录，避免未批准覆盖并记录传输结果
---

# transfer-file（内部工序）

Upload or download files between the local machine and the selected board.

## Inputs

- `direction`: `upload` or `download`
- `source_path`
- `destination_path`
- `board`
- Approved SSH credential source

## Procedure

1. Validate that the source path exists.
2. Check whether the destination exists.
3. Ask for approval before overwriting an existing destination.
4. Use `scp` or `rsync` when available:
   ```bash
   scp -r <source_path> root@<BOARD_IP>:<destination_path>
   ```
5. Verify the destination exists after transfer using `ssh test -e` for remote destinations or local filesystem checks for downloads.

## Outputs

- `transfer_status`
- `bytes_or_file_count`
- `destination`
