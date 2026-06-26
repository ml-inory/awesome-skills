# run-model（内部工序）

通过 pyaxengine RemoteAXExecutionProvider 在选定板子上运行 axmodel。

## 前提

- `axengine` 已安装（`pip install axengine-*.whl`，wheel 在 ax-remote-infer release zip 的 `client/` 目录）
- daemon 已在目标板子的 18500 端口监听

## 执行

```bash
python core/infer.py <MODEL_PATH> --host <BOARD_IP> [--input <INPUT_FILE>]
```

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
