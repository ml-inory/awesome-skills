---
name: train-model
description: 根据用户需求找好用的深度学习模型：优先复用开源预训练模型，仅在现成模型不满足指标时才自研训练。入口通过 grill-me 对齐需求，产出 PyTorch 权重、ONNX 模型、导出和验证脚本。
---

# train-model

找好用的深度学习模型：优先复用开源预训练模型，不满足指标才走自研训练管线。

## 触发条件

当用户提出以下需求时使用本 skill：
- "找一个 xxx 任务的模型"
- "调研并训练 xxx 任务模型"
- "需要一个好用的 xxx 模型"
- "导出模型到 ONNX 并在 NPU 上验证"

## 工作流概述

```
需求对齐(grill-me)
    ↓
调研选型 → 预训练模型实测 → 对比报告 → [用户确认]
    ↓
  ┌── 预训练模型达标? ──→ ONNX 导出 → 精度验证 → 交付（快速路径）
  │
  └── 预训练模型不达标 ──→ 数据集验证 + 训练配置
    ↓
训练 + 自动调参 (最多 3 轮)
    ↓
精度门控检查 → [不达标: 重试或用户裁决]
    ↓
ONNX 导出 + 导出脚本
    ↓
精度验证 + 验证脚本
    ↓
产出交付
```

## 入口协议

1. **启动需求对齐**: 调用 `$grill-me`，逐项确认：
   - 任务类型（图像分类 / 目标检测 / 语义分割 / 文本分类 / 其他）
   - 数据集路径（必须包含 train/val 子目录）
   - 精度目标（如 Top-1 Acc ≥ 90%）
   - 效率约束（如推理延迟 < 10ms on NPU、参数量上限）
   - 输出目录

2. **调用调研阶段**: 加载 `hidden/research/SKILL.md`，根据对齐结果搜索候选架构，下载预训练权重在用户验证集上实测精度，生成 `research_report.md`。

3. **路由决策**: 呈现候选对比报告（含实测精度），用户确认后：
   - **快速路径**: 预训练模型已达标 → 跳过训练，直接进入 ONNX 导出
   - **完整路径**: 预训练模型不达标 → 以该模型为起点进入自研训练管线

4. **执行对应管线**:
   - 快速路径: `hidden/export/SKILL.md` → `hidden/validate/SKILL.md`
   - 完整路径: `hidden/setup/SKILL.md` → `hidden/train/SKILL.md` → `hidden/export/SKILL.md` → `hidden/validate/SKILL.md`

5. **交付产出**: 确认所有 acceptance checks 通过后，汇总产出物清单。

## 阶段职责

| 阶段 | Helper Skill | 产出 |
|------|-------------|------|
| 调研+实测 | `hidden/research/SKILL.md` | `research_report.md`（含验证集实测精度） |
| 配置（仅完整路径） | `hidden/setup/SKILL.md` | `training_config.json`, `model_code.py` |
| 训练（仅完整路径） | `hidden/train/SKILL.md` | `best_model.pt`, `training_log.json`, TensorBoard logs |
| 导出 | `hidden/export/SKILL.md` | `model.onnx`, `export.py` |
| 验证 | `hidden/validate/SKILL.md` | `validate.py`, `accuracy_report.json` |

## 失败处理

- **调研阶段未找到达标预训练模型**: 自动进入完整训练路径，以最优候选模型为起点
- **预训练模型达标但 ONNX 导出失败**: 尝试修复（调整输入 shape、opset 版本等），最多 2 次
- **训练精度不达标**: 自动调参重试最多 3 轮，超限后交用户裁决是否接受当前最优结果
- **数据集问题**: 立即中断并报告具体错误
- **精度验证不匹配**: 产出详细差异报告，标注为 degraded 但仍交付

## 工作流规范

完整的机器可读工作流定义见 [train-model.yaml](../../workflows/train-model.yaml)。

## 依赖

- PyTorch >= 1.12, torchvision
- ONNX >= 1.13, onnxruntime
- TensorBoard
- CUDA 环境（本地 GPU）
- `$grill-me` skill（需求对齐）
