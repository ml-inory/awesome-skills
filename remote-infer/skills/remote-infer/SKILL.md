---
description: 在内网找空闲 AX 板子，在上面执行任意任务
---

# remote-infer

TRIGGER when: user mentions 板子, 找板子, 上板子, 跑一下, remote board, AX board, or wants to do anything on a board (deploy, run, mount, infer, ssh, etc.).

在内网找一块空闲 AX 板子，通过 SSH 执行用户指定的任务。

## 用法

```
/remote-infer [--chip AX650N|AX630C|AX650C] <任务描述>
```

任务举例：
- 跑 axmodel 推理：`/remote-infer model.axmodel [--input data.npy]`
- 部署服务：`/remote-infer 部署 my-server`
- 挂载本地目录：`/remote-infer mount /local/path`
- 执行任意命令：`/remote-infer 执行 echo hello`

## 执行步骤

### Step 1 — 选板

```bash
python3 -c "
import json, sys, requests
devices = requests.get('http://10.126.35.22:25000/api/devices', timeout=5).json()['devices']
candidates = [d for d in devices if d['is_ax'] and not d['is_occupied']]
if not candidates:
    print('ERROR: no available AX board', file=sys.stderr); sys.exit(1)
candidates.sort(key=lambda d: d.get('cmm_used_percent') or 100)
d = candidates[0]
print(json.dumps({'ip': d['ip'], 'hostname': d['hostname'], 'chip_type': d['chip_type']}))
"
```

输出 JSON：`{"ip": "...", "hostname": "...", "chip_type": "..."}`
若无可用板子，打印错误并中止。

### Step 2 — 执行任务

根据用户意图选择方式：

| 场景 | 做法 |
|------|------|
| 跑 axmodel 推理 | 先 [ensure-daemon](../hidden/ensure-daemon/SKILL.md)，再 [run-model](../hidden/run-model/SKILL.md) |
| 部署服务 / 执行命令 | `ssh root@<IP> '<command>'` |
| 上传文件 | `scp <local> root@<IP>:<remote>` |
| 挂载本地目录到板子 | `ssh root@<IP> 'mount -t nfs ...'` 或按需选方案 |
| 挂载板子目录到本地 | `sshfs root@<IP>:<remote> <local_mountpoint>` |

默认 SSH 凭据：用户 `root`，密码 `123456`（或 SSH key）。

## 输出

展示选中的板子（IP、芯片型号、主机名）+ 任务执行结果。
