---
name: ranker
description: 对扫描出的重构优化机会按 ROI、风险和依赖关系排序，生成高收益低风险优先的执行队列
---

# Opportunity Ranker（隐藏 Skill）

## 职责
对 Scanner 产出的所有优化机会按 ROI（投入产出比）排序，生成执行队列。
核心原则：**高收益、低风险的先做**。

## 输入
| 输入 | 来源 | 说明 |
|------|------|------|
| `opportunities` | Scanner skill | 所有发现的优化机会列表 |
| `optimization_target` | Entry | 用于权重计算 |

## 排序算法

### ROI 打分公式
```
score = (estimated_improvement_pct * confidence_weight) / (risk_weight + dependency_count)
```

权重映射：
| 因子 | high | medium | low |
|------|------|--------|-----|
| confidence_weight | 1.0 | 0.6 | 0.3 |
| risk_weight | 0.3 | 0.6 | 1.0 |

### 排序规则
1. 按 `score` 降序排列
2. 分数相同时，优先选择 `dependency_count = 0` 的独立项
3. 有依赖关系的机会点，被依赖方必须排在依赖方前面（拓扑排序）

## 输出
保存排序后的执行队列至 `storage/workflows/<run_id>/execution_queue.json`：

```json
{
  "queue": [
    { "rank": 1, "id": "OPP-003", "score": 2.67, "reason": "高收益低风险，无依赖" },
    { "rank": 2, "id": "OPP-001", "score": 2.10, "reason": "高收益低风险，无依赖" },
    { "rank": 3, "id": "OPP-007", "score": 1.45, "reason": "中等收益，依赖 OPP-001" }
  ],
  "skipped": [
    { "id": "OPP-012", "reason": "confidence 过低，跳过" }
  ]
}
```
