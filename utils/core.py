import json
import os
from collections import defaultdict

PROVERB_FILE = "data/proverbs.json"

def save_proverb(proverb, region):
    os.makedirs(os.path.dirname(PROVERB_FILE), exist_ok=True)
    data = load_proverbs()
    entry = {
        "proverb": proverb,
        "region": region,
        "votes": 0,
        "likes": 0,
        "views": 0,
        "saves": 0
    }
    data.append(entry)
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_proverbs():
    if not os.path.exists(PROVERB_FILE):
        return []
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def get_stats():
    stats = defaultdict(int)
    for item in load_proverbs():
        region = item.get("region", "Unknown")
        stats[region] += 1
    return dict(stats)

def update_metric(proverb_text, key):
    data = load_proverbs()
    for item in data:
        if item["proverb"] == proverb_text:
            item[key] = item.get(key, 0) + 1
            break
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
