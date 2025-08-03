import os
import json

PROVERBS_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def save_proverb(proverb, city, language):
    with open(PROVERBS_FILE, "a", encoding="utf-8") as f:
        f.write(proverb.strip() + "\n")
    update_stats(city)

def update_stats(city):
    stats = {}

    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)

    # ✅ Ensure keys exist
    if "total_proverbs" not in stats:
        stats["total_proverbs"] = 0
    if "regions" not in stats:
        stats["regions"] = {}

    stats["total_proverbs"] += 1
    if city in stats["regions"]:
        stats["regions"][city] += 1
    else:
        stats["regions"][city] = 1

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {"total_proverbs": 0, "regions": {}}
