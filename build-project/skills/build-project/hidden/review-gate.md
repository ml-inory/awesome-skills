# hidden/review-gate — 评审门控（双重终止检查）

## 输入
- `TEST_STATUS`：`pass` 或 `fail`
- `COMMIT_HASH`：本轮提交（如测试失败则为空）
- `N`：当前迭代号
- `GOAL`：总目标

## 执行

### 情况 A：测试失败（TEST_STATUS=fail）
1. 向用户展示失败摘要。
2. 询问用户：
   > "测试未通过，本轮迭代 [N] 的修改未提交。选择：\n1) 重新编码修复（回到 code 步骤）\n2) 跳过测试强制提交\n3) 放弃本轮，回到需求重新设计"
3. 根据用户选择返回：`retry_code` / `force_commit` / `retry_spec`

### 情况 B：测试通过（TEST_STATUS=pass）
1. 展示本轮迭代摘要：
   - Issue 编号 + 标题
   - Commit hash
   - 测试通过数
2. 对照总目标 `GOAL`，列出**尚未完成的部分**（基于 `.build-state.json` 历史）。
3. 询问用户：
   > "迭代 [N] 完成，测试全部通过。\n未完成：<剩余目标列表>\n\n继续下一轮迭代，还是结束并开 PR？"
4. 根据用户回答返回：`continue`（下一轮）或 `done`（开 PR）

## 输出
`GATE_RESULT`：`continue` / `done` / `retry_code` / `retry_spec` / `force_commit`
