"""
update_data.py
Reads env vars → writes data.json (with checksum) and appends history.txt
"""
import json, hashlib, os, sys, subprocess


def write_data_json(output_path: str = "data.json") -> dict:
    try:
        d = {
            "temp":      float(os.environ["TEMP"]),
            "wind":      float(os.environ["WIND"]),
            "direction": float(os.environ["DIRECTION"]),
            "is_day":    os.environ.get("IS_DAY", "0") == "1",
            "status":    os.environ["STATUS"],
            "trend":     os.environ["TREND"],
            "score":     int(os.environ["SCORE"]),
            "anomaly":   os.environ.get("ANOMALY", ""),
            "updated":   subprocess.check_output(
                             ["date", "-u", "+%Y-%m-%dT%H:%M:%SZ"]
                         ).decode().strip()
        }
    except (KeyError, ValueError) as e:
        print(f"ERROR: missing env var — {e}", file=sys.stderr)
        sys.exit(1)

    payload      = json.dumps(d, sort_keys=True)
    d["sha256"]  = hashlib.sha256(payload.encode()).hexdigest()[:16]

    with open(output_path, "w") as f:
        json.dump(d, f, indent=2)

    print(f"data.json written: temp={d['temp']} status={d['status']} sha256={d['sha256']}")
    return d


def append_history(timestamp: str, history_path: str = "history.txt") -> None:
    header = "timestamp,temp,wind,status,trend,score,anomaly"

    # init if missing or wrong format
    if not os.path.exists(history_path):
        with open(history_path, "w") as f:
            f.write(header + "\n")

    with open(history_path) as f:
        content = f.read()

    if not content.startswith("timestamp"):
        content = header + "\n" + content

    row = ",".join([
        timestamp,
        os.environ.get("TEMP", ""),
        os.environ.get("WIND", ""),
        os.environ.get("STATUS", ""),
        os.environ.get("TREND", ""),
        os.environ.get("SCORE", ""),
        os.environ.get("ANOMALY", "")
    ])

    lines     = content.strip().splitlines()
    head      = lines[0]
    data_rows = lines[1:]
    data_rows.append(row)
    data_rows = data_rows[-100:]  # keep last 100

    with open(history_path, "w") as f:
        f.write(head + "\n")
        f.write("\n".join(data_rows) + "\n")

    print(f"history.txt updated: {len(data_rows)} rows")


def main():
    write_data_json()
    timestamp = subprocess.check_output(
        ["date", "-u", "+%Y-%m-%dT%H:%M"]
    ).decode().strip()
    append_history(timestamp)


if __name__ == "__main__":
    main()
