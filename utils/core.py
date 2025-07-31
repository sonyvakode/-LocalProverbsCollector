import json
import os

DATA_FILE = "proverbs.json"

def save_proverb(proverb, region):
    data = load_proverbs()
    data.append({"proverb": proverb, "region": region, "votes": 0})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_proverbs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_stats():
    data = load_proverbs()
    stats = {}
    for item in data:
        region = item["region"]
        stats[region] = stats.get(region, 0) + 1
    return stats
