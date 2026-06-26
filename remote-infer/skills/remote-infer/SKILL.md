---
description: 在内网找空闲 AX 板子运行 axmodel 推理
---

# remote-infer

TRIGGER when: user mentions running/testing axmodel on a board, "找板子", "跑一下", "板子推理", "remote infer", or asks to test a .axmodel file.

在内网找一块空闲 AX 板子，上传并运行 axmodel，返回推理结果。

## 用法

```
/remote-infer <model.axmodel> [--chip AX650N|AX630C|AX650C] [--input data.npy]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `<model.axmodel>` | 是 | 本地 axmodel 文件路径 |
| `--chip` | 否 | 指定芯片型号；不填则选任意空闲 AX 板 |
| `--input` | 否 | 输入数据文件（.npy 或 .npz）；不填则用全零张量做功能验证 |

## 执行步骤

按顺序执行以下工序（对用户透明）：

### Step 1 — 选板

运行 `core/board_client.py`，从内网 dashboard 找空闲 AX 板：

```bash
python core/board_client.py [--chip <CHIP_TYPE>]
```

- 输出 JSON：`{"ip": "...", "hostname": "...", "chip_type": "..."}`
- 若无可用板子：打印错误并中止，提示用户稍后重试

### Step 2 — 检查 daemon

对选中板子的 `<ip>:18500` 做 TCP 连通性测试：

```bash
python -c "import socket,sys; s=socket.socket(); s.settimeout(3); r=s.connect_ex(('<IP>', 18500)); s.close(); sys.exit(r)"
```

- **返回 0**（端口通）→ daemon 已就绪，跳到 Step 3
- **返回非 0**（端口不通）→ 执行 [ensure-daemon](../hidden/ensure-daemon/SKILL.md)

### Step 3 — 运行推理

```bash
python core/infer.py <model.axmodel> --host <IP> [--input <data.npy>]
```

输出 JSON，结构为 `{output_name: [[...]]}` 。

## 输出格式

向用户展示：
1. 选中的板子（IP、芯片型号、主机名）
2. 推理输出（各输出张量的 shape 与前几个值）
3. 如有 `device_inference_us` 字段，显示推理耗时
