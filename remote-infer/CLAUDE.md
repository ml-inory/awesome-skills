# remote-infer 工作流

在内网找一块空闲 AX 板子，在上面执行任意任务（部署服务、挂载目录、跑推理等）。

权威协议见 [workflows/remote-infer.yaml](workflows/remote-infer.yaml)。当步骤顺序、gate、重试或失败处理不明确时，以 YAML 为准。

## 入口

```
/remote-infer [--chip AX650N|AX630C|AX650C] <任务描述>
```

参见 [skills/remote-infer/SKILL.md](skills/remote-infer/SKILL.md)。

## 工序流图

```
用户输入
  ↓
[classify-task]  解析任务类型、风险、输入和验证方式
  ↓
[select-board]   查询 http://10.126.35.22:25000/api/devices，选空闲 AX 板
  ↓
[执行任务]       按分类选择一种路径：SSH命令 / scp上传下载 / sshfs挂载 / axmodel推理
  ↓（推理场景额外步骤）
[ensure-daemon]  检查 <ip>:18500，不通则安装 daemon
[run-model]      pyaxengine 推理，返回输出张量
  ↓
展示结果（板子信息 + 任务输出）
```

## 依赖

| 工具 | 安装方式 | 场景 |
|------|---------|------|
| `requests` | `pip install requests` | 选板 |
| `ssh` / `scp` | 系统包或 OpenSSH | SSH/SCP |
| `sshpass` | `apt install sshpass` | 仅在用户明确批准密码认证时使用 |
| `sshfs` | `apt install sshfs` | 挂载板子目录到本地 |
| `axengine` | `pip install ax-remote-infer-*/client/axengine-*.whl` | axmodel 推理 |

## 核心模块

- `core/board_client.py` — 查询 dashboard，选板
- `core/infer.py` — 运行推理

## 内网 AX 板（当前在线）

| IP | 芯片 | 主机名 |
|----|------|--------|
| 10.126.35.86  | AX650N | ax650 |
| 10.126.35.114 | AX650N | ax650 |
| 10.126.35.203 | AX650C | pyramid-openclaw |
| 10.126.35.148 | AX630C | ax630c |
