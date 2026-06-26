# awesome-skills

Claude Code / Codex 技能集合。Codex CLI 中通过 `$skill-name` 显式调用，Claude Code 中通过 `/skill-name` 调用。

## 技能列表

| 技能 | 说明 | 调用方式 |
|------|------|---------|
| [remote-infer](remote-infer/) | 在内网找空闲 AX 板子运行 axmodel 推理 | Codex: `$remote-infer model.axmodel [--chip AX650N] [--input data.npy]` |
| [build-project](build-project/) | 需求→编码→测试→提交的小步迭代循环，直到目标达成 | Codex: `$build-project` |
| [refactor](refactor/) | 稳步重构遗留代码，向指定目标（速度/体积）优化 | Codex: `$refactor [speed\|size\|speed+size]` |

## 安装

**Claude Code**（安装到 `~/.claude/skills/`）：
```bash
./setup.sh
```

**Codex**（安装到 `~/.agents/skills/`）：
```bash
./setup.sh --codex
```
