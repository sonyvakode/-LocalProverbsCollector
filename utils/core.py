import os
import json

PROVERB_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def load_proverbs():
    if not os.path.exists(PROVERB_FILE):
        return []
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_proverb(text, region=None, language=None):
    with open(PROVERB_FILE, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")

    # Update stats
    if not os.path.exists(STATS_FILE):
        stats = {"total": 0}
    else:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)

    stats["total"] = stats.get("total", 0) + 1
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f)

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total": 0}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
