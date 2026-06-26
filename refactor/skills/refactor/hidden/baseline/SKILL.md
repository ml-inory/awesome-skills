# Baseline Snapshot（隐藏 Skill）

## 职责
在重构开始前，捕获代码库的当前状态作为基线。
此基线是后续所有轮次对比的**唯一真相源**。

## 输入
| 输入 | 来源 | 说明 |
|------|------|------|
| `tech_stack` | Entry skill | 决定使用哪些 test/lint/bench 工具 |
| `scope` | Entry skill | 分析范围 |
| `optimization_target` | Entry skill | 需要 benchmark 的维度（speed/size） |

## 执行步骤

### 1. 发现并运行现有测试
根据 `tech_stack` 检测并执行测试套件：

| 技术栈 | 测试命令 | 检测依据 |
|--------|---------|---------|
| python | `pytest --tb=short -q` | `pytest.ini`, `pyproject.toml` |
| cpp/cuda | `ctest --output-on-failure` 或 `make test` | `CMakeLists.txt` |
| rust | `cargo test` | `Cargo.toml` |
| typescript | `npm test` 或 `npx jest` | `package.json` |

**记录**：测试总数、通过/失败数、完整输出日志。

**关键**：若基线测试有任何失败，立即停止并报告用户，不在破损基线上继续。

### 2. 运行 Lint / Type Check
| 技术栈 | Lint 命令 |
|--------|----------|
| python | `ruff check .` 或 `flake8`；`mypy .` 或 `pyright` |
| cpp | `clang-tidy` |
| rust | `cargo clippy` |
| typescript | `npx eslint .`；`npx tsc --noEmit` |

**记录**：当前 warning/error 数量作为基线。

### 3. 运行 Benchmark（若目标含 speed）
- 查找已有 benchmark 文件（`bench_*.py`、`*_benchmark.cpp`、`benches/` 等）
- 若无 benchmark，以测试套件执行时间作为代理指标
- 尽可能按模块/函数记录耗时

### 4. 度量体积（若目标含 size）
- 二进制大小：度量编译产物
- 代码行数：使用 `tokei` 或 `cloc`
- Bundle 大小：对 JS/TS 度量打包产物

## 输出
保存基线快照至 `storage/workflows/<run_id>/baseline.json`：

```json
{
  "run_id": "refactor-20250625-001",
  "timestamp": "2025-06-25T10:00:00Z",
  "tests": { "total": 130, "passed": 130, "failed": 0 },
  "lint": { "errors": 0, "warnings": 12 },
  "benchmark": {
    "total_time_ms": 4500,
    "per_module": { "module_a.process": 340, "module_b.parse": 89 }
  },
  "size": { "binary_bytes": null, "loc": 8500 }
}
```
