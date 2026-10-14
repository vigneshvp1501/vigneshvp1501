from pathlib import Path
from datetime import date
import json
import html

INPUT = Path("data/contributions.json")
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353"]

def main():
    if not INPUT.exists():
        raise SystemExit("Missing data/contributions.json. Run fetch_contributions.py first.")
    data = json.loads(INPUT.read_text(encoding="utf-8"))
    days = data.get("days", [])
    if not days:
        raise SystemExit("No contribution days found.")
    by_date = {x["date"]: x for x in days}
    first = date.fromisoformat(days[0]["date"])
    start = date.fromordinal(first.toordinal() - (first.weekday() + 1) % 7)
    cell, gap, left, top, weeks = 12, 3, 45, 48, 53
    width = left + weeks*(cell+gap) + 10
    height = top + 7*(cell+gap) + 50
    rects, labels, months = [], [], set()
    for offset in range(weeks*7):
        current = date.fromordinal(start.toordinal()+offset)
        week = offset // 7
        dow = (current.weekday()+1) % 7
        item = by_date.get(current.isoformat(), {})
        level = max(0, min(4, int(item.get("level", 0))))
        x, y = left+week*(cell+gap), top+dow*(cell+gap)
        rects.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="3" fill="{PALETTE[level]}"><title>{current.isoformat()}: {int(item.get("count",0))} contributions</title></rect>')
        key = current.strftime("%Y-%m")
        if current.day <= 7 and key not in months:
            labels.append(f'<text x="{x}" y="30" fill="#8b949e" font-size="11" font-family="sans-serif">{html.escape(current.strftime("%b"))}</text>')
            months.add(key)
    total = int(data.get("total_contributions_in_calendar", 0))
    legend = [f'<rect x="{width-130+i*17}" y="{height-25}" width="11" height="11" rx="2" fill="{c}"/>' for i,c in enumerate(PALETTE)]
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
<rect width="100%" height="100%" rx="10" fill="#0d1117"/>
<text x="20" y="24" fill="#c9d1d9" font-family="sans-serif" font-size="14" font-weight="600">{html.escape(data.get("username","GitHub"))}: {total:,} contributions in the displayed calendar</text>
{''.join(labels)}{''.join(rects)}
<text x="45" y="{height-15}" fill="#8b949e" font-family="sans-serif" font-size="11">Less</text>
{''.join(legend)}
<text x="{width-28}" y="{height-15}" fill="#8b949e" font-family="sans-serif" font-size="11">More</text>
</svg>'''
    Path("contrib-heatmap.svg").write_text(svg, encoding="utf-8")
    print("Created contrib-heatmap.svg")

if __name__ == "__main__":
    main()
