from pathlib import Path
from datetime import date, datetime, timedelta
import json
import os
import re
import requests
from bs4 import BeautifulSoup

USERNAME = os.getenv("GITHUB_USERNAME", "vigneshvp1501")
URL = f"https://github.com/users/{USERNAME}/contributions"

def main():
    response = requests.get(URL, headers={"User-Agent": "profile-art-generator/1.0"}, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    cells = soup.select("td[data-date][data-level]")
    if not cells:
        raise SystemExit("Could not find contribution cells. GitHub may have changed its HTML or rate-limited this request.")
    days = []
    for cell in cells:
        day = cell.get("data-date")
        level = int(cell.get("data-level", "0"))
        title = cell.get("title", "")
        match = re.search(r"([\d,]+)\s+contribution", title, re.I)
        count = int(match.group(1).replace(",", "")) if match else 0
        days.append({"date": day, "level": level, "count": count})
    count_map = {x["date"]: x["count"] for x in days}
    cursor = date.today()
    streak = 0
    while count_map.get(cursor.isoformat(), 0) > 0:
        streak += 1
        cursor -= timedelta(days=1)
    best = current = 0
    previous = None
    for item in days:
        d = date.fromisoformat(item["date"])
        if item["count"] > 0:
            current = current + 1 if previous and d == previous + timedelta(days=1) else 1
            best = max(best, current)
        else:
            current = 0
        previous = d
    payload = {
        "username": USERNAME,
        "fetched_at": datetime.now().astimezone().isoformat(),
        "total_contributions_in_calendar": sum(x["count"] for x in days),
        "current_streak": streak,
        "longest_streak_in_calendar": best,
        "best_day_count": max((x["count"] for x in days), default=0),
        "days": days,
    }
    Path("data").mkdir(exist_ok=True)
    Path("data/contributions.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {len(days)} days for {USERNAME}")

if __name__ == "__main__":
    main()
