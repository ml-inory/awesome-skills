# Opportunity Scanner（隐藏 Skill）

## 职责
全局扫描代码库，识别所有可优化的机会点。
这是"按收益排序逐个攻克"策略的第一步——先把靶子全部找出来。

## 输入
| 输入 | 来源 | 说明 |
|------|------|------|
| `optimization_target` | Entry | `speed` / `size` / `speed+size` |
| `tech_stack` | Entry | 目标语言 |
| `scope` | Entry | 扫描范围 |
| `baseline` | Baseline skill | 基线数据，用于定位热点 |

## 扫描策略

### 针对 speed 的扫描项
1. **热点函数**：基于 baseline benchmark 数据，标记耗时 top-N 的函数
2. **算法复杂度**：识别 O(n^2) 或更差的循环/嵌套模式
3. **重复计算**：检测可缓存/可记忆化的重复调用
4. **I/O 瓶颈**：识别同步阻塞 I/O、逐行读取大文件等模式
5. **数据结构选型**：检测使用 list 做查找（应为 set/dict）等反模式
6. **不必要的拷贝**：检测可以用引用/视图替代的深拷贝

### 针对 size 的扫描项
1. **死代码**：未引用的函数、类、import
2. **重复代码**：高相似度的代码块，可提取为公共函数
3. **过度抽象**：只有一个实现的 interface/abstract class
4. **冗余依赖**：只使用了极少功能的大型依赖
5. **内联候选**：只被调用一次的小函数

## 输出
每个机会点生成一条结构化记录，保存至 `storage/workflows/<run_id>/opportunities.json`：

```json
[
  {
    "id": "OPP-001",
    "type": "speed",
    "category": "algorithm_complexity",
    "file": "src/module_a.py",
    "line_range": [45, 78],
    "function": "process_data",
    "description": "嵌套循环导致 O(n^2) 复杂度，数据量大时成为瓶颈",
    "estimated_improvement": "60-80%",
    "confidence": "high",
    "risk": "low",
    "dependencies": []
  }
]
```

## 注意事项
- 扫描阶段**只读不写**，不修改任何源代码
- 每个机会点必须标注 `confidence`（high/medium/low）和 `risk`（low/medium/high）
- 存在依赖关系的机会点须通过 `dependencies` 字段声明
