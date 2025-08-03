import os
import json
from datetime import datetime

DATA_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"


def save_proverb(proverb):
    # Save the proverb to file
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(proverb + "\n")

    # Update stats
    stats = load_stats()
    stats["total_submitted"] = stats.get("total_submitted", 0) + 1

    # Optional: you could enhance this with more detailed region tracking
    region = stats.get("last_region", "Unknown")
    if "regions" not in stats:
        stats["regions"] = {}
    stats["regions"][region] = stats["regions"].get(region, 0) + 1

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)


def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"total_submitted": 0, "regions": {}}


def load_proverbs():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []
