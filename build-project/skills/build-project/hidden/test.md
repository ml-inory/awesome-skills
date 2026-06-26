# hidden/test — 测试验证

## 执行

1. 自动检测测试框架（按优先级）：
   | 文件 | 命令 |
   |------|------|
   | `pyproject.toml` / `pytest.ini` | `python -m pytest -x -q` |
   | `package.json` (scripts.test) | `npm test -- --passWithNoTests` |
   | `go.mod` | `go test ./...` |
   | `Makefile` (target: test) | `make test` |
   | 无 | 报告"未检测到测试框架，请手动指定测试命令" |

2. 运行测试，捕获完整输出。

3. 判断结果：
   - **全部通过**：输出 `TEST_STATUS=pass` + 通过数量。
   - **有失败**：输出 `TEST_STATUS=fail` + 失败的测试名称和错误摘要。
     - 将错误摘要写入当前 Issue 的评论：
       ```
       gh issue comment <ISSUE_NUMBER> --body "## 测试失败\n\`\`\`\n<错误输出>\n\`\`\`"
       ```
     - 返回 `TEST_STATUS=fail` 给 review-gate，**不自动修复**，由 review-gate 决定是否重新触发 code。

## 输出
`TEST_STATUS`：`pass` 或 `fail`
