import json
from pathlib import Path
from collections import Counter

DATA_FILE = Path("proverbs.json")

def load_proverbs():
    if DATA_FILE.exists():
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_proverb(proverb, region):
    data = load_proverbs()
    for entry in data:
        if entry["proverb"] == proverb:
            return  # Avoid duplicates
    data.append({"proverb": proverb, "region": region, "votes": 0})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_stats():
    data = load_proverbs()
    counts = Counter(p["region"] for p in data)
    return dict(counts)
