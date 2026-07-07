---
name: train-model-research
description: 根据 grill-me 对齐的需求，搜索候选模型架构，下载预训练权重在用户验证集上实测精度，产出对比报告并给出快速/完整路径路由建议。
hidden: true
---

# train-model-research

搜索候选模型，预训练权重实测评估，产出对比报告与路由建议。

## 输入

- requirement_doc: 来自 grill-me 的需求对齐结果，必须包含 task_type, accuracy_target, efficiency_constraints, dataset_scale, dataset_path

## 输出

- research_report.md: 候选模型对比报告（含验证集实测精度）
- selected_model: 推荐模型架构标识
- pretrained_weights_path: 下载的预训练权重本地路径
- verdict: fast（预训练达标，跳过训练）或 full（需要自研训练）

## 执行流程

### Step 1: 搜索候选模型

根据 task_type 和效率约束搜索候选架构。CV 任务: timm, torchvision.models。NLP 任务: HuggingFace Transformers。通用: GitHub 开源实现, PapersWithCode 排行榜。

搜索原则：优先选择原生支持 ONNX 导出的架构，优先选择 NPU 有已验证部署案例的架构，参数规模在约束范围内，必须有公开预训练权重可供下载。

### Step 2: 预训练模型实测评估

这是核心步骤。对上一步筛选出的候选模型（通常 2-4 个），逐一执行：

a) 下载预训练权重。优先使用 timm.create_model(pretrained=True) 或 torchvision 标准接口
b) 根据 task_type 调整分类头以匹配用户数据集类别数
c) 在用户验证集上做全量推理，计算精度指标（Top-1 Acc / mAP / mIoU 等）
d) 记录每个候选模型的实际精度、推理耗时

### Step 3: 评估候选模型综合评分

每个候选评估以下维度，每项 1-5 分：

| 维度 | 评估标准 |
|------|---------|
| 实测精度 | 在用户验证集上的实际精度得分 |
| ONNX 兼容性 | 是否包含 ONNX 不支持的算子 |
| NPU 适配性 | 在 AX/NPU 平台上的部署可行性 |
| 推理效率 | 参数量、FLOPs、实测推理耗时 |
| 社区活跃度 | GitHub stars、更新频率、文档质量 |

### Step 4: 生成对比报告

输出 research_report.md，结构包含：任务概述、候选模型实测精度对比表格、各模型详细分析（来源/实测精度/优势/劣势/NPU注意事项）、路由建议及理由。

### Step 5: 路由判定

比较最优候选的实测精度与用户需求目标：
- 实测精度 >= 精度目标：verdict = fast，推荐直接使用该预训练模型
- 实测精度 < 精度目标：verdict = full，推荐以该模型为起点进行微调训练

## 失败处理

- 预训练权重下载失败：尝试备用下载源，最多 2 次
- 实测精度因数据格式问题无法计算：报告错误详情，跳过该候选
- 所有候选实测精度均不达标：verdict = full，选择实测精度最高的作为训练起点
