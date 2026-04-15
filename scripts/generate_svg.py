"""
generate_svg.py
Reads temp.csv → generates graph.svg (last 20 readings)
"""
import csv, datetime, sys


def read_temps(csv_path: str = "temp.csv", limit: int = 20) -> list:
    rows = []
    try:
        with open(csv_path) as f:
            reader = csv.DictReader(f)
            for row in reader:
                try:
                    rows.append(float(row["temperature"]))
                except (ValueError, KeyError):
                    pass
    except Exception as e:
        print(f"WARNING: could not read {csv_path}: {e}", file=sys.stderr)
    return rows[-limit:] if rows else [0]


def generate_svg(rows: list, output_path: str = "graph.svg") -> None:
    w, h, pad = 500, 215, 20
    min_t = min(rows)
    max_t = max(rows)
    span  = max(max_t - min_t, 1)

    def px(i: int, val: float) -> str:
        x = pad + i * (w - 2 * pad) / max(len(rows) - 1, 1)
        y = h - 25 - (val - min_t) / span * (h - pad - 25)
        return f"{x:.1f},{y:.1f}"

    points  = " ".join(px(i, v) for i, v in enumerate(rows))
    updated = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # moving average (window=3)
    ma_points = ""
    if len(rows) >= 3:
        ma = []
        for i in range(len(rows)):
            window = rows[max(0, i - 1): i + 2]
            ma.append(sum(window) / len(window))
        ma_points = " ".join(px(i, v) for i, v in enumerate(ma))

    svg_parts = [
        f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg">',
        f'<rect width="{w}" height="{h}" fill="#0b1a2a"/>',
        # y-axis labels
        f'<text x="5" y="{pad + 4}" font-size="8" fill="#556">{max_t:.1f}</text>',
        f'<text x="5" y="{h - 25}" font-size="8" fill="#556">{min_t:.1f}</text>',
        # main line
        f'<polyline fill="none" stroke="#00ffcc" stroke-width="2" points="{points}"/>',
    ]

    # moving average line
    if ma_points:
        svg_parts.append(
            f'<polyline fill="none" stroke="#ff9944" stroke-width="1" '
            f'stroke-dasharray="3,2" opacity="0.7" points="{ma_points}"/>'
        )

    svg_parts += [
        f'<text x="10" y="13" font-size="9" fill="#aaa">Temp (°C) — last {len(rows)} readings</text>',
        f'<text x="{w - 5}" y="13" font-size="7" fill="#445" text-anchor="end">— MA3</text>',
        f'<text x="10" y="{h - 3}" font-size="8" fill="#445">Updated: {updated}</text>',
        '</svg>'
    ]

    with open(output_path, "w") as f:
        f.write("\n".join(svg_parts))

    print(f"graph.svg written: {len(rows)} points")


def main():
    rows = read_temps()
    generate_svg(rows)


if __name__ == "__main__":
    main()
