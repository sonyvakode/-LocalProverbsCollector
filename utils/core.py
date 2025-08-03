import os
import json

PROVERBS_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def save_proverb(proverb, city, language):
    """Save a proverb with metadata."""
    os.makedirs("data", exist_ok=True)

    with open(PROVERBS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{proverb} [{city}] ({language})\n")

    update_stats(city)

def get_all_proverbs():
    """Load all saved proverbs."""
    if not os.path.exists(PROVERBS_FILE):
        return []
    with open(PROVERBS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def update_stats(city):
    """Update total and regional stats."""
    if not os.path.exists(STATS_FILE):
        stats = {"total_submitted": 0, "regions": {}}
    else:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)

    stats["total_submitted"] = stats.get("total_submitted", 0) + 1
    if city in stats["regions"]:
        stats["regions"][city] += 1
    else:
        stats["regions"][city] = 1

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

def load_stats():
    """Load stats data."""
    if not os.path.exists(STATS_FILE):
        return {"total_submitted": 0, "regions": {}}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
