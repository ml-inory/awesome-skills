# Test Augment（隐藏 Skill）

## 职责
为刚刚完成的重构**新增**测试用例，确保重构后的代码行为正确。
**绝不修改任何已有测试文件**，只创建新的测试文件或在新文件中追加用例。

## 输入
| 输入 | 来源 | 说明 |
|------|------|------|
| `changes` | Refactor One | 本轮变更摘要 |
| `tech_stack` | Entry | 决定测试框架 |
| `opportunity` | 当前优化项 | 理解优化的意图 |

## 执行步骤

### 1. 确定新增测试的存放位置
- 新测试文件命名规则：`test_refactor_<opportunity_id>.py`（Python 示例）
- 放置在与被测文件对应的 test 目录下
- **绝不修改**任何已存在的 `test_*.py` / `*_test.go` / `*.test.ts` 等文件

### 2. 生成测试用例
为重构后的代码生成以下类型的测试：

| 测试类型 | 目的 | 优先级 |
|---------|------|--------|
| **等价性测试** | 验证重构前后输出一致 | 必须 |
| **边界测试** | 覆盖边界条件（空输入、大数据量等） | 必须 |
| **性能回归测试** | 断言性能不低于基线 | 建议（若目标含 speed） |
| **类型/契约测试** | 验证返回类型和接口契约 | 建议 |

### 3. 运行新增测试
执行新增的测试文件，确认全部通过：
```bash
# Python 示例
pytest tests/test_refactor_OPP001.py -v
```

若新增测试不通过，说明重构本身有问题，标记本轮为 `needs_fix` 并回退到 Refactor One。

## 输出
- 新增的测试文件
- 记录至 `storage/workflows/<run_id>/rounds/<round_N>/new_tests.json`：

```json
{
  "opportunity_id": "OPP-001",
  "test_file": "tests/test_refactor_OPP001.py",
  "test_count": 5,
  "categories": ["equivalence", "boundary", "performance_regression"],
  "all_passed": true
}
```
