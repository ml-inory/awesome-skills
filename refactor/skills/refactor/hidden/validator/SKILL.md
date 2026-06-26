# Validator（隐藏 Skill）

## 职责
每轮重构完成后的**三重验证门控**。只有三项全部通过，本轮才算成功。
任何一项失败都会触发回滚。

## 输入
| 输入 | 来源 | 说明 |
|------|------|------|
| `baseline` | Baseline skill | 基线数据，用于对比 |
| `changes` | Refactor One | 本轮变更 |
| `tech_stack` | Entry | 决定验证工具 |
| `optimization_target` | Entry | 决定 benchmark 维度 |

## 三重验证

### Gate 1: 全量测试通过
运行**所有**测试（原有 + 本轮新增）：
```bash
# Python 示例
pytest --tb=short -q
```

**判定标准**：
- 原有测试：必须 100% 通过，0 失败
- 新增测试：必须 100% 通过
- 若有任何失败 -> 本轮 FAIL

### Gate 2: 性能/体积有量化提升
根据 `optimization_target` 运行对应度量：

**speed 模式**：
- 重新运行 benchmark，对比基线
- 本轮修改的函数必须有 >= 5% 的耗时下降
- 若性能反而下降 -> 本轮 FAIL

**size 模式**：
- 重新度量代码行数 / 二进制大小
- 必须有净减少
- 若体积反而增加 -> 本轮 FAIL

### Gate 3: 无新增 Lint/Type 错误
运行 lint 和 type check，对比基线：
- `lint_errors_now <= baseline.lint.errors`
- `lint_warnings_now <= baseline.lint.warnings`（允许减少）
- 若新增了任何 error -> 本轮 FAIL

## 判定逻辑
```
if gate1_pass AND gate2_pass AND gate3_pass:
    status = "PASS"
    -> 将本轮变更合并到主分支
    -> 更新 baseline 为新状态（用于下一轮对比）
else:
    status = "FAIL"
    -> 触发 Rollback skill
    -> 记录失败原因
    -> 继续队列中的下一个机会点
```

## 输出
保存验证结果至 `storage/workflows/<run_id>/rounds/<round_N>/validation.json`：

```json
{
  "opportunity_id": "OPP-001",
  "round": 1,
  "gate1_tests": { "pass": true, "total": 135, "passed": 135, "failed": 0 },
  "gate2_perf": { "pass": true, "metric": "speed", "before_ms": 340, "after_ms": 120, "improvement_pct": 64.7 },
  "gate3_lint": { "pass": true, "errors_delta": 0, "warnings_delta": -2 },
  "overall": "PASS"
}
```
