
import json
import os

DATA_FILE = os.path.join("data", "proverbs.json")

def load_proverbs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_proverb(text, region):
    proverbs = load_proverbs()
    proverbs.append({"text": text, "region": region})
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(proverbs, f, ensure_ascii=False, indent=2)

def get_stats():
    proverbs = load_proverbs()
    stats = {}
    for item in proverbs:
        region = item.get("region", "Unknown").strip()
        if region:
            stats[region] = stats.get(region, 0) + 1
    return stats
