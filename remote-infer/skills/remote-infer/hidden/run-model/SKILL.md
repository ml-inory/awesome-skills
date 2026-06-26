# run-model（内部工序）

通过 pyaxengine RemoteAXExecutionProvider 在选定板子上运行 axmodel。

## 前提

- `axengine` 已安装（`pip install axengine-*.whl`，wheel 在 ax-remote-infer release zip 的 `client/` 目录）
- daemon 已在目标板子的 18500 端口监听

## 执行

```bash
python3 -c "
import json, sys, numpy as np
try:
    import axengine as axe
except ImportError:
    print('ERROR: axengine not installed. Run: pip install axengine-*.whl', file=sys.stderr); sys.exit(1)
sess = axe.InferenceSession('<MODEL_PATH>',
    providers=['RemoteAXExecutionProvider'],
    provider_options={'host': '<BOARD_IP>', 'port': '18500'})
in_meta = sess.get_inputs()
# 有输入文件时: data = np.load('<INPUT_FILE>', allow_pickle=True)
feeds = {m.name: np.zeros(m.shape, dtype=np.float32) for m in in_meta}
outputs = sess.run(None, feeds)
out_meta = sess.get_outputs()
print(json.dumps({m.name: o.tolist() for m, o in zip(out_meta, outputs)}, indent=2))
"
```

将 `<MODEL_PATH>`、`<BOARD_IP>`（以及可选的 `<INPUT_FILE>`）替换为实际值后执行。

参数说明：
- `MODEL_PATH`：本地 .axmodel 文件，pyaxengine 自动上传到板子
- `--host`：板子 IP
- `--input`：可选，.npy（单输入）或 .npz（多输入命名张量）；省略则用全零张量

## 输出 JSON

```json
{
  "output0": [[0.1, 0.2, ...]],
  ...
}
```

## axengine 安装方式

```bash
# 解压 ax-remote-infer release zip 后
pip install ~/ax-remote-infer-*/client/axengine-*.whl
```

若 wheel 不存在，可从源码构建：
```bash
cd ~/ax-remote-infer-*/third-party/pyaxengine
python -m build --wheel && pip install dist/axengine-*.whl
```
