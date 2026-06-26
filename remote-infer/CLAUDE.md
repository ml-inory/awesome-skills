# remote-infer 工作流

在内网找一块空闲 AX 板子，运行 axmodel 推理。

## 入口

```
/remote-infer <model.axmodel> [--chip AX650N|AX630C|AX650C] [--input data.npy]
```

参见 [skills/remote-infer/SKILL.md](skills/remote-infer/SKILL.md)。

## 工序流图

```
用户输入
  ↓
[select-board]   查询 http://10.126.35.22:25000/api/devices，选空闲 AX 板
  ↓
[ensure-daemon]  检查 <ip>:18500，不通则 remote_install.sh 安装 daemon
  ↓
[run-model]      pyaxengine RemoteAXExecutionProvider 推理，返回输出张量
  ↓
展示结果（板子信息 + 输出 shape/值 + 推理耗时）
```

## 依赖

| 工具 | 安装方式 |
|------|---------|
| `requests` | `pip install requests` |
| `axengine` | `pip install ax-remote-infer-*/client/axengine-*.whl` |
| `sshpass` | `apt install sshpass`（仅在需要安装 daemon 时） |

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
