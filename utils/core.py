import os
import json
from datetime import datetime

PROVERB_FILE = "data/proverbs.json"

def load_proverbs():
    if not os.path.exists(PROVERB_FILE):
        return []
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_proverb(proverb, region):
    data = load_proverbs()
    entry = {
        "proverb": proverb,
        "region": region,
        "timestamp": datetime.now().isoformat(),
        "votes": 0
    }
    data.append(entry)
    os.makedirs("data", exist_ok=True)
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_stats():
    data = load_proverbs()
    stats = {}
    for entry in data:
        region = entry.get("region", "Unknown")
        stats[region] = stats.get(region, 0) + 1
    return stats
