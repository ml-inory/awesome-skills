# select-board（内部工序）

查询内网设备 dashboard，返回一块空闲 AX 板的连接信息。

## 执行

```bash
python core/board_client.py [--chip <CHIP_TYPE>] [--list]
```

## 选板规则

1. 过滤 `is_ax=true` 且 `is_occupied=false` 的设备
2. 若指定 `--chip`，进一步过滤 `chip_type` 包含该字符串（大小写不敏感）
3. 按 `cmm_used_percent` 升序，选占用最低的板子

## 输出

成功：标准输出一行 JSON
```json
{"ip": "10.126.35.86", "hostname": "ax650", "chip_type": "AX650N_CHIP"}
```

失败：stderr 输出 `ERROR: no available AX board`，exit code 1。

## Dashboard API

`GET http://10.126.35.22:25000/api/devices`
返回字段中关键项：`is_ax`, `is_occupied`, `chip_type`, `ip`, `hostname`, `cmm_used_percent`
