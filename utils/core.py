import json
import os

DATA_FILE = "data/proverbs.json"

def save_proverb(proverb, region):
    os.makedirs("data", exist_ok=True)
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
    except:
        data = []

    data.append({"proverb": proverb, "region": region, "likes": 0, "views": 0})

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def load_stats():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        region_count = {}
        for entry in data:
            region = entry.get("region", "Unknown")
            region_count[region] = region_count.get(region, 0) + 1
        return region_count
    except:
        return {}
