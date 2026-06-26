# build-project

小步迭代的需求→编码→测试→提交循环，直到目标达成。

## 触发条件
用户说"开始开发"、"build"、`/build-project` 或提出一个新的开发目标。

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

### Step 1 — 需求设计（→ hidden/spec）
调用 `hidden/spec`，传入当前迭代目标。

### Step 2 — 编码（→ hidden/code）
调用 `hidden/code`，传入 Issue 编号。

### Step 3 — 测试（→ hidden/test）
调用 `hidden/test`。

### Step 4 — 提交（→ hidden/commit）
调用 `hidden/commit`，传入 Issue 编号和迭代号。

### Step 5 — 评审门控（→ hidden/review-gate）
调用 `hidden/review-gate`。
- 返回 `continue` → N += 1，更新 `.build-state.json`，回到 Step 1
- 返回 `done` → 进入 Step 6

### Step 6 — 合并（→ hidden/merge）
调用 `hidden/merge`。

## 工作留痕
每次迭代结束后，在 `.build-state.json` 中追加本轮摘要：
```json
{"iteration": N, "issue": "#XX", "commit": "<hash>", "test_status": "pass|fail", "summary": "..."}
```
