---
name: train-model-export
description: 从 best_model.pt 导出 ONNX 模型并生成可复用导出脚本 export.py。
hidden: true
---

# train-model-export

从 PyTorch checkpoint 导出 ONNX 模型，生成可复用的导出脚本。

## 输入

- best_model.pt: 训练产出的最优 PyTorch 权重
- model_code.py: 模型定义文件
- output_dir: 输出目录

## 输出

- model.onnx: 导出的 ONNX 模型
- export.py: 可独立运行的导出脚本

## 执行流程

### Step 1: 加载模型

从 model_code.py 实例化模型，加载 best_model.pt 权重到 CPU，设置为 eval 模式。

### Step 2: 确定输入规格

根据 task_type 和训练配置确定模型输入 shape。图像分类默认 (1, 3, 224, 224)，目标检测根据数据集图像尺寸，其他从 DataLoader 取一个 batch 确定。创建 example_input 为 torch.randn(input_shape)。

### Step 3: ONNX 导出

使用 torch.onnx.export，input_names 设为 ["input"]，output_names 设为 ["output"]，dynamic_axes 设为 None 优先静态 shape（NPU 友好），opset_version 默认 13（AX NPU 兼容）。若导出失败尝试符号注册、上调 opset 到 17、或 jit.script 预处理。

### Step 4: ONNX 验证

用 onnxruntime 加载 model.onnx 推理。检查 onnx.checker.check_model 通过。对比 PyTorch 和 ONNX 输出确保形状一致、数值误差可接受。

### Step 5: 生成导出脚本

生成 export.py，参数化（--checkpoint, --output），包含模型定义和 torch.onnx.export 调用，包含 onnxruntime 验证逻辑，可独立运行。

## 失败处理

- ONNX 导出失败: 尝试升级 opset，若仍失败报告具体算子和替代方案
- ONNX 推理与 PyTorch 不一致: 检查预处理参数并更新 export.py
