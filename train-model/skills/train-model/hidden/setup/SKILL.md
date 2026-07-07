---
name: train-model-setup
description: 验证数据集完整性，配置 DataLoader、数据增强、优化器搜索空间，生成初始训练配置文件。
hidden: true
---

# train-model-setup

验证数据集完整性，配置训练基础设施，生成训练配置。

## 输入

- `dataset_path`: 用户指定的数据集目录路径
- `selected_model`: 用户确认的模型架构标识
- `requirement_doc`: 需求对齐结果（task_type, accuracy_target, efficiency_constraints）

## 输出

- `training_config.json`: 完整训练配置
- `model_code.py`: 实例化的模型定义

## 执行流程

### Step 1: 数据集验证

检查数据集路径下是否存在 train/val 子目录，统计每个类别的样本数，验证数据可正常加载，检测图像尺寸分布并确定合理的 resize 策略。

若数据格式异常，报告具体错误信息（文件损坏数、扩展名不一致等）。

### Step 2: 数据增强与预处理

根据 task_type 和数据集规模自动选择增强策略：

| 数据集规模 | 增强策略 |
|-----------|---------|
| < 1000/类 | 强增强: RandomResizedCrop, ColorJitter, RandomHorizontalFlip, RandAugment |
| 1000-10000/类 | 中等增强: RandomResizedCrop, RandomHorizontalFlip |
| > 10000/类 | 轻增强: RandomResizedCrop |

根据图像尺寸分布自动选择 resize 尺寸，确保不裁剪关键内容。

### Step 3: 模型实例化

根据 selected_model 确定模型实现来源：
- timm 模型: `timm.create_model(name, pretrained=True, num_classes=N)`
- torchvision 模型: `torchvision.models.get_model(name, weights='DEFAULT', num_classes=N)`
- 用户自定义: 用户提供 Python 文件或类路径

生成 model_code.py，包含完整的模型定义和 forward 方法。

### Step 4: 生成训练配置

根据 task_type 自动选择：
- 损失函数: classification→CrossEntropyLoss, detection→组合loss, segmentation→CrossEntropy/Dice
- 验证指标: classification→Top1/Top5 Acc, detection→mAP@0.5:0.95, segmentation→mIoU
- 优化器搜索空间: SGD(lr:1e-3~1e-1, momentum:0.9) + AdamW(lr:1e-5~1e-3)
- LR Scheduler: CosineAnnealing, ReduceLROnPlateau
- Batch Size: 根据 GPU 显存自动估算

输出 training_config.json，包含所有初始超参数和搜索空间定义。

## 失败处理

- 数据集路径不存在或不可读: 立即中断，报告具体错误
- train/val 子目录缺失: 询问用户数据目录结构，尝试自动发现
- 模型实例化失败: 检查模型名称拼写，尝试 timm/torchvision 搜索
