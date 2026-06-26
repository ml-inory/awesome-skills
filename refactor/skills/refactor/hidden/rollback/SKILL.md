# Rollback（隐藏 Skill）

## 职责
当 Validator 判定某轮重构失败时，**干净地回滚所有变更**，确保代码库恢复到本轮开始前的状态。

## 输入
| 输入 | 来源 | 说明 |
|------|------|------|
| `opportunity_id` | 当前轮次 | 失败的优化项 |
| `validation_result` | Validator | 失败原因详情 |
| `branch_name` | Refactor One | 本轮使用的 git 分支 |

## 执行步骤

### 1. 切回主分支
```bash
git checkout main  # 或用户指定的主分支
```

### 2. 删除失败分支
```bash
git branch -D refactor/<run_id>/<opportunity_id>
```

### 3. 清理新增的测试文件（若有）
若 Test Augment 已生成测试文件但验证失败，这些测试文件也要清除：
```bash
git checkout -- .  # 恢复所有未提交的变更
git clean -fd      # 清除未跟踪的新文件
```

### 4. 记录失败日志
保存至 `storage/workflows/<run_id>/rounds/<round_N>/rollback.json`：

```json
{
  "opportunity_id": "OPP-001",
  "reason": "Gate 1 failed: 2 existing tests broke",
  "detail": "test_module_a.py::test_edge_case FAILED - AssertionError",
  "action": "full_rollback",
  "branch_deleted": "refactor/refactor-20250625-001/OPP-001",
  "status": "rolled_back"
}
```

### 5. 分类处理
根据失败类型决定后续动作：

| 失败类型 | 动作 |
|---------|------|
| Gate 1（测试失败） | 跳过此机会，继续队列下一项 |
| Gate 2（性能未提升） | 跳过此机会，继续队列下一项 |
| Gate 3（lint 错误） | 可尝试自动修复一次，若仍失败则跳过 |
| 连续 3 次失败 | 暂停工作流，向用户报告情况 |

## 输出
- 代码库恢复至本轮开始前状态
- 失败记录已持久化
- 返回控制权给 Orchestrator，由其决定继续或停止
