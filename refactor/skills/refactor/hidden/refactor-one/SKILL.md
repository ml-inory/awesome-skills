---
name: refactor-one
description: 针对单个优化机会执行最小化且 API 兼容的代码重构，适用于 refactor 工作流逐个处理执行队列项时
---

# Refactor One（隐藏 Skill）

## 职责
执行**单个**优化机会的代码重构。每次只改一个点，保持变更最小化和可追溯性。

## 输入
| 输入 | 来源 | 说明 |
|------|------|------|
| `opportunity` | Ranker 产出的队列当前项 | 要执行的优化机会 |
| `tech_stack` | Entry | 目标语言 |
| `baseline` | Baseline | 用于理解上下文 |

## 执行步骤

### 1. 创建 Git 分支
```
git checkout -b refactor/<run_id>/<opportunity_id>
```
每个优化点在独立分支上操作，便于回滚。

### 2. 分析上下文
- 读取目标文件及其直接依赖
- 理解函数签名、调用链、数据流
- 确认修改不会破坏公共 API 契约

### 3. 执行重构
根据 opportunity 的 `category` 选择对应的重构手法：

| 类别 | 重构手法 |
|------|---------|
| `algorithm_complexity` | 替换算法（如排序、查找），引入更优数据结构 |
| `redundant_computation` | 添加缓存/memoization，提取循环不变量 |
| `io_bottleneck` | 改为批量读取、异步 I/O、使用缓冲区 |
| `data_structure` | 替换容器类型（list->set, dict->defaultdict 等） |
| `unnecessary_copy` | 改为引用传递、使用 view/slice |
| `dead_code` | 删除未引用代码 |
| `duplicate_code` | 提取公共函数/基类 |
| `over_abstraction` | 内联或简化不必要的抽象层 |

### 4. 保持 API 兼容
**硬约束**：
- 不改变任何公共函数/方法的签名（名称、参数、返回类型）
- 不改变任何现有测试文件
- 不改变模块的导入路径

若优化必须改变 API，标记为 `blocked` 并跳过，报告给用户。

## 输出
- 修改后的源文件（在 git 分支上）
- 变更摘要记录至 `storage/workflows/<run_id>/rounds/<round_N>/changes.json`：

```json
{
  "opportunity_id": "OPP-001",
  "files_modified": ["src/module_a.py"],
  "lines_changed": { "added": 12, "removed": 25 },
  "technique": "algorithm_complexity -> 将 O(n^2) 嵌套循环替换为 dict 查找",
  "api_compatible": true
}
```
