# hidden/code — 编码实现

## 输入
- `ISSUE_NUMBER`：本轮 GitHub Issue 编号
- `STACK`：技术栈

## 执行

1. 用 `gh issue view <ISSUE_NUMBER>` 读取验收标准。
2. 读取相关源文件，理解现有代码结构，**不修改未涉及的文件**。
3. 实现最小改动以满足本轮 Issue 的验收标准：
   - 只写完成任务必须的代码，不提前抽象，不加无关功能。
   - 若发现需求模糊或有阻塞，用 `gh issue comment <ISSUE_NUMBER> --body "..."` 记录问题，然后询问用户。
4. 完成后在 Issue 留下实现摘要：
   ```
   gh issue comment <ISSUE_NUMBER> --body "## 实现摘要\n- 修改了：<文件列表>\n- 核心逻辑：<一句话>"
   ```

## 输出
已修改的文件列表。
