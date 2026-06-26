# ensure-daemon（内部工序）

当 TCP 18500 不通时，在目标板子上安装并启动 ax_remote_infer daemon。

## 前提

- 已下载 ax-remote-infer release zip（从 https://github.com/AXERA-TECH/ax-remote-infer/releases/latest）
- 本地已解压到某目录（含 `remote_install.sh`）

## 执行

若 release zip 不存在，先下载并解压：

```bash
# 查找本地已有的 release 目录
ls ~/ax-remote-infer-* 2>/dev/null || \
  (mkdir -p ~/ax-remote-infer && \
   curl -L https://github.com/AXERA-TECH/ax-remote-infer/releases/latest/download/ax-remote-infer-latest.zip \
     -o /tmp/ax-remote-infer.zip && \
   unzip /tmp/ax-remote-infer.zip -d ~/)
```

然后远程安装 daemon：

```bash
cd ~/ax-remote-infer-*/
./remote_install.sh <BOARD_IP> [--user root] [--pass <PASSWORD>]
```

`install.sh` 会自动识别芯片型号、部署对应二进制、注册服务并启动。

## 验证

安装后再次检查端口：
```bash
python -c "import socket,sys; s=socket.socket(); s.settimeout(5); r=s.connect_ex(('<IP>', 18500)); s.close(); sys.exit(r)"
```

成功则继续；失败则报错并要求用户手动检查板子。

## 注意

- 默认 SSH 用户 `root`，密码 `123456`（或询问用户）
- 需要本机安装 `sshpass`（`apt install sshpass`）或使用 SSH key
