# utils/core.py

import json
import os
from collections import defaultdict

PROVERB_FILE = "data/proverbs.json"

def save_proverb(text, region):
    os.makedirs("data", exist_ok=True)
    proverbs = []

    if os.path.exists(PROVERB_FILE):
        with open(PROVERB_FILE, "r", encoding="utf-8") as f:
            try:
                proverbs = json.load(f)
            except json.JSONDecodeError:
                proverbs = []

    proverbs.append({"text": text, "region": region})

    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(proverbs, f, ensure_ascii=False, indent=2)

def get_stats():
    if not os.path.exists(PROVERB_FILE):
        return {}

    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        try:
            proverbs = json.load(f)
        except json.JSONDecodeError:
            return {}

    region_counts = defaultdict(int)
    for p in proverbs:
        region = p.get("region", "Unknown")
        region_counts[region] += 1

    return dict(region_counts)
