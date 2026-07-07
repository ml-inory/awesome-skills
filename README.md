# awesome-skills

Claude Code / Codex 技能集合。Codex CLI 中通过 `$skill-name` 显式调用，Claude Code 中通过 `/skill-name` 调用。

每个重建后的工作流包含：

- `skills/<name>/SKILL.md`：用户可见入口 skill。
- `skills/<name>/hidden/*/SKILL.md`：内部 helper skill。
- `workflows/<name>.yaml`：权威 workflow 协议，定义状态机、步骤、gate、失败策略和完成条件。

## 技能列表

| 技能 | 说明 | Workflow | 调用方式 |
|------|------|----------|---------|
| [remote-infer](remote-infer/) | 在内网找空闲 AX 板子，执行推理、SSH 命令、传输、挂载或部署任务 | [remote-infer.yaml](remote-infer/workflows/remote-infer.yaml) | Codex: `$remote-infer model.axmodel [--chip AX650N] [--input data.npy]` |
| [build-project](build-project/) | 初始化→需求切片→编码→测试→提交→评审→PR 的小步开发循环 | [build-project.yaml](build-project/workflows/build-project.yaml) | Codex: `$build-project <开发目标>` |
| [refactor](refactor/) | 稳步重构遗留代码，向指定目标（速度/体积）优化 | [refactor.yaml](refactor/workflows/refactor.yaml) | Codex: `$refactor [speed\|size\|speed+size]` |
| [train-model](train-model/) | 找好用的深度学习模型：优先复用开源预训练模型，不满足指标才自研训练 | [train-model.yaml](train-model/workflows/train-model.yaml) | Codex: `$train-model <训练目标>` |

## 安装

**Claude Code**（安装到 `~/.claude/skills/`）：
```bash
./setup.sh
```

**Codex**（安装到 `${CODEX_HOME:-~/.codex}/skills/`）：
```bash
./setup.sh --codex
```

安装脚本会同时链接 workflow YAML 到目标根目录的 `workflows/`，使入口 skill 中的 `../../workflows/<name>.yaml` 引用保持可用。
