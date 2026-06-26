# hidden/spec — 需求设计

## 输入
- `GOAL`：总目标（来自 `.build-state.json`）
- `N`：当前迭代号

## 执行

1. 读取 `.build-state.json`，获取总目标和已完成迭代记录。
2. 根据已完成进度，拆解出**本轮迭代的最小可交付单元**（一个功能点或一个修复）。
   - 原则：本轮改动应能在单次 PR 中被理解和审查。
   - 若是第一轮，直接从总目标中提取最高优先级的子任务。
3. 用 `gh issue create` 创建 GitHub Issue：
   ```
   gh issue create \
     --title "feat[N]: <本轮任务一句话标题>" \
     --body "## 目标\n<具体描述>\n\n## 验收标准\n- [ ] <可测试的条件1>\n- [ ] <可测试的条件2>\n\n## 备注\n迭代 N，总目标：<GOAL>"
   ```
4. 将返回的 Issue 编号追加到 `.build-state.json` 的 `issues` 数组。
5. 输出 Issue 编号和标题，供后续步骤引用。

## 输出
`ISSUE_NUMBER`（如 `#42`）
