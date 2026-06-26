---
name: build-project
description: 小步迭代地把开发目标拆成需求设计、编码、测试、提交、评审和合并循环，适用于用户要求开始开发、build 或提出新的开发目标时
---

# build-project

小步迭代的需求→编码→测试→提交循环，直到目标达成。

## 重要：自主执行规则
**不得在步骤之间停下来等待用户确认。** 每完成一步，立即执行下一步。唯一可以暂停的情况：
- Step 0 中确实缺少 `GOAL` 或无法自动检测技术栈
- 编码过程中发现需求模糊无法继续
- Step 5 评审门控判断为 `done`

## 触发条件
用户说"开始开发"、"build"、`$build-project`、`/build-project` 或提出一个新的开发目标。

## 入口参数
从用户消息中提取（可选，未提供时主动询问）：
- `GOAL`：本次开发的总目标（一句话描述）
- `STACK`：技术栈（如 python/node/go，若能从项目文件自动检测则无需询问）

## 执行步骤

### Step 0 — 初始化
1. 若 `GOAL` 未提供，询问用户："本次开发的目标是什么？"
2. 检测技术栈：按优先级查找 `pyproject.toml` / `package.json` / `go.mod` / `Makefile`；若无则询问。
3. 创建 feature 分支：
   ```
   git checkout -b feat/build-$(date +%Y%m%d-%H%M)
   ```
4. 记录迭代计数器 `N=1`，保存到 `.build-state.json`：
   ```json
   {"goal": "<GOAL>", "stack": "<STACK>", "branch": "<branch>", "iteration": 1, "issues": []}
   ```
5. **完成后立即执行 Step 1，不要停。**

### Step 1 — 需求设计
读取 `hidden/spec.md`，按其中全部步骤执行，传入当前迭代目标和 N。
**完成后立即执行 Step 2，不要停。**

### Step 2 — 编码
读取 `hidden/code.md`，按其中全部步骤执行，传入 ISSUE_NUMBER 和 STACK。
**完成后立即执行 Step 3，不要停。**

### Step 3 — 测试
读取 `hidden/test.md`，按其中全部步骤执行。
**完成后立即执行 Step 4，不要停。**

### Step 4 — 提交
读取 `hidden/commit.md`，按其中全部步骤执行，传入 ISSUE_NUMBER 和 N。
**完成后立即执行 Step 5，不要停。**

### Step 5 — 评审门控
读取 `hidden/review-gate.md`，按其中全部步骤执行。
- 结果为 `continue` → N += 1，更新 `.build-state.json`，**立即回到 Step 1**
- 结果为 `done` → 执行 Step 6

### Step 6 — 合并
读取 `hidden/merge.md`，按其中全部步骤执行。

## 工作留痕
每次迭代结束后，在 `.build-state.json` 中追加本轮摘要：
```json
{"iteration": N, "issue": "#XX", "commit": "<hash>", "test_status": "pass|fail", "summary": "..."}
```
