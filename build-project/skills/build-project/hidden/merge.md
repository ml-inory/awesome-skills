# hidden/merge — 开 PR 合并到 main

## 执行

1. 读取 `.build-state.json`，汇总所有迭代的 Issue 和 commit。
2. 生成 PR 描述：
   ```
   ## 目标
   <GOAL>

   ## 迭代记录
   | 迭代 | Issue | Commit | 状态 |
   |------|-------|--------|------|
   | 1 | #XX | abc1234 | pass |
   | 2 | #YY | def5678 | pass |
   ...

   ## 测试
   全部通过（最终运行结果见最后一轮 Issue 评论）

   ## 关联 Issues
   Closes #XX, #YY, ...
   ```
3. 创建 PR：
   ```
   gh pr create \
     --base main \
     --title "feat: <GOAL>" \
     --body "<上述描述>"
   ```
4. 输出 PR URL，提示用户 review 后手动合并（**不自动 merge**）。
5. 删除 `.build-state.json`（工作流结束，状态文件清理）。

## 输出
PR URL
