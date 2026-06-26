# hidden/commit — 提交到 feature 分支

## 输入
- `ISSUE_NUMBER`：Issue 编号（用于关联提交）
- `N`：迭代号

## 前置条件
仅在 `TEST_STATUS=pass` 时执行。若测试未通过，跳过本步骤。

## 执行

1. 仅 stage 本轮实际修改的文件（**不用 `git add .`**）：
   ```
   git add <修改的文件列表>
   ```
2. 提交，消息格式遵循 Conventional Commits：
   ```
   git commit -m "feat(iter-N): <Issue 标题> (<ISSUE_NUMBER>)"
   ```
3. 关闭 Issue 验收标准的 checkbox（用 `gh issue edit` 更新 body）。
4. 在 Issue 评论中记录提交信息：
   ```
   gh issue comment <ISSUE_NUMBER> --body "## 提交记录\ncommit: $(git rev-parse --short HEAD)\nbranch: $(git branch --show-current)"
   ```

## 输出
`COMMIT_HASH`（短 hash）
