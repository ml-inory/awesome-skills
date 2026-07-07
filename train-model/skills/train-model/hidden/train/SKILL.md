---
name: train-model-train
description: 执行训练循环并自动调参。最多 3 轮重试，不达标后交用户裁决。
hidden: true
---

# train-model-train

执行训练循环，自动调参，记录实验日志。

## 输入

- `training_config.json`: 训练配置（含搜索空间）
- `model_code.py`: 模型定义
- `dataset_path`: 数据集路径
- `output_dir`: 输出目录

## 输出

- `best_model.pt`: 验证集上最优权重
- `training_log.json`: 结构化训练日志
- `tensorboard_logs/`: TensorBoard 事件文件

## 执行流程

每轮训练后验证精度，不达标则调整超参重试，最多 3 轮。

### Round 0: 基线训练

使用 training_config.json 中的默认超参：SGD(lr=0.01, momentum=0.9) 或 AdamW(lr=1e-3)。LR Scheduler 用 CosineAnnealing。Epochs 根据数据集规模和模型复杂度估算（默认 90）。Early Stopping patience=15 监控 val_loss。输出 baseline 精度。

### Round 1: 学习率调优

若 Round 0 精度不达标：分析 loss 曲线，若 loss 下降缓慢则提高 lr（2x-5x），若 loss 震荡则降低 lr（0.1x-0.5x）。尝试 SGD 与 AdamW 互换。调整 scheduler 策略。

### Round 2: 训练策略调优

若 Round 1 仍不达标：调整 batch size（GPU 显存充裕时增大 2-4x）。尝试 warmup 前 5 epoch。调整数据增强强度。尝试 Label Smoothing 和 weight decay 调整。

### 每轮训练

每个 epoch：训练阶段前向→loss→反向→optimizer.step，验证阶段计算 val_metrics。若 val_metrics 为当前最优则保存 best_model.pt。写入 TensorBoard（train_loss, val_loss, val_metrics）和 training_log.json。Early Stopping patience 个 epoch 无提升则提前终止。

### 日志格式

training_log.json 每条记录包含：round 编号、hyperparams（lr, optimizer, batch_size, epochs）、best_epoch、best_metrics、target_met 布尔值。最终字段 final_best_metrics 记录全局最优。

## 失败处理

- 训练发散（loss→NaN）：降低 lr 10x 重试当前轮，不消耗重试预算
- GPU OOM：自动减半 batch size 重试，不消耗重试预算
- 3 轮全部不达标：产出 training_log.json 及每轮分析，询问用户选择：接受当前最优、手动指定超参、或更换模型
