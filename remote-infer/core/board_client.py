"""Query the device dashboard and select an available AX board."""
import json, sys
import requests

DASHBOARD = "http://10.126.35.22:25000/api/devices"

def get_board(chip_type=None):
    devices = requests.get(DASHBOARD, timeout=5).json()["devices"]
    candidates = [d for d in devices if d["is_ax"] and not d["is_occupied"]]
    if chip_type:
        chip = chip_type.upper()
        candidates = [d for d in candidates if chip in d["chip_type"].upper()]
    if not candidates:
        return None
    candidates.sort(key=lambda d: d.get("cmm_used_percent") or 100)
    d = candidates[0]
    return {"ip": d["ip"], "hostname": d["hostname"], "chip_type": d["chip_type"]}

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser()
    p.add_argument("--chip", default=None, help="e.g. AX650N, AX630C")
    p.add_argument("--list", action="store_true", help="list all available AX boards")
    args = p.parse_args()

    if args.list:
        devices = requests.get(DASHBOARD, timeout=5).json()["devices"]
        candidates = [d for d in devices if d["is_ax"]]
        for d in candidates:
            status = "OCCUPIED" if d["is_occupied"] else "free"
            print(f"{d['ip']:16s}  {d['chip_type']:16s}  {d['hostname']:20s}  {status}")
        sys.exit(0)

    board = get_board(args.chip)
    if not board:
        print("ERROR: no available AX board", file=sys.stderr)
        sys.exit(1)
    print(json.dumps(board))
