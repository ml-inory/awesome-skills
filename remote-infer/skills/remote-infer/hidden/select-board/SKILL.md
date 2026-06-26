# select-board（内部工序）

查询内网设备 dashboard，返回一块空闲 AX 板的连接信息。

## 执行

```bash
python3 -c "
import json, sys, requests
devices = requests.get('http://10.126.35.22:25000/api/devices', timeout=5).json()['devices']
candidates = [d for d in devices if d['is_ax'] and not d['is_occupied']]
# 若需过滤芯片型号，在此加: candidates = [d for d in candidates if 'AX650N' in d['chip_type'].upper()]
if not candidates:
    print('ERROR: no available AX board', file=sys.stderr); sys.exit(1)
candidates.sort(key=lambda d: d.get('cmm_used_percent') or 100)
d = candidates[0]
print(json.dumps({'ip': d['ip'], 'hostname': d['hostname'], 'chip_type': d['chip_type']}))
"
```

若需查看所有板子状态：

```bash
python3 -c "
import requests
for d in requests.get('http://10.126.35.22:25000/api/devices', timeout=5).json()['devices']:
    if d['is_ax']:
        print(d['ip'], d['chip_type'], 'OCCUPIED' if d['is_occupied'] else 'free')
"
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
