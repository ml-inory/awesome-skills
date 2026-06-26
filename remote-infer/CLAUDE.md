# remote-infer 工作流

在内网找一块空闲 AX 板子，在上面执行任意任务（部署服务、挂载目录、跑推理等）。

## 入口

```
/remote-infer [--chip AX650N|AX630C|AX650C] <任务描述>
```

参见 [skills/remote-infer/SKILL.md](skills/remote-infer/SKILL.md)。

## 工序流图

```
用户输入
  ↓
[select-board]   查询 http://10.126.35.22:25000/api/devices，选空闲 AX 板
  ↓
[执行任务]       按用户意图选方式：SSH命令 / scp上传 / sshfs挂载 / axmodel推理
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
| `sshpass` | `apt install sshpass` | SSH/SCP（密码认证） |
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
