---
name: train-model-validate
description: 对比 ONNX 与 PyTorch 模型推理精度，生成独立可运行的精度验证脚本 validate.py。
hidden: true
---

# train-model-validate

对比 ONNX 与 PyTorch 模型推理精度，生成独立验证脚本。

## 输入

model.onnx, best_model.pt, model_code.py, validation_dataset, output_dir

## 输出

validate.py（独立可运行的精度验证脚本）, accuracy_report.json（精度对比报告）

## 执行流程

### Step 1: 加载双模型

分别加载 PyTorch 模型（best_model.pt, eval 模式）和 ONNX 模型（onnxruntime.InferenceSession）。确保输入预处理一致。

### Step 2: 逐样本推理对比

在验证集遍历所有样本，PyTorch 和 ONNX 分别推理。计算相对误差，记录误差分布（均值、最大值、超阈值比例）。

### Step 3: 精度指标计算

根据 task_type 计算 ONNX 模型验证集精度，与 training_log.json 中 PyTorch 的 best_metrics 对比，确认精度无明显退化。输出 accuracy_report.json。

### Step 4: 生成验证脚本

生成 validate.py：参数化接受 onnx path、checkpoint path、data dir、output path。包含模型定义、onnxruntime 推理、PyTorch 推理、精度指标计算。输出 JSON 格式的精度对比报告。可独立运行。

## 失败处理

相对误差超过 1e-5：标注为精度不一致，产出详细差异分布，标记 degraded 但仍交付。精度退化超过 1%：警告用户，建议使用更高精度数据类型导出。
