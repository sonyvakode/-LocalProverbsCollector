import os
import json
from collections import Counter

DATA_FILE = "data/proverbs.txt"

def save_proverb(text, region):
    entry = {"text": text, "region": region, "likes": 0, "views": 0, "saves": 0}
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")

def load_proverbs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def load_stats():
    proverbs = load_proverbs()
    regions = [p.get("region", "Unknown") for p in proverbs]
    return dict(Counter(regions))
