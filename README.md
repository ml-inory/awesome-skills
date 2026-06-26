# awesome-skills

Claude Code 技能集合，通过 `/skill-name` 调用。

## 技能列表

| 技能 | 说明 | 调用方式 |
|------|------|---------|
| [remote-infer](remote-infer/) | 在内网找空闲 AX 板子运行 axmodel 推理 | `/remote-infer model.axmodel [--chip AX650N] [--input data.npy]` |
| [build-project](build-project/) | 需求→编码→测试→提交的小步迭代循环，直到目标达成 | `/build-project` |

## 安装

将技能目录软链到 `~/.claude/skills/`：

```bash
ln -s $(pwd)/remote-infer/skills/remote-infer ~/.claude/skills/remote-infer
```
