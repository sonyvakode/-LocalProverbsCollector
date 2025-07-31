import os
import json
from collections import Counter

PROVERB_FILE = "proverbs.json"


def save_proverb(text, region):
    """Save a submitted proverb to file"""
    entry = {"text": text, "region": region}
    if os.path.exists(PROVERB_FILE):
        with open(PROVERB_FILE, "r", encoding="utf-8") as f:
            proverbs = json.load(f)
    else:
        proverbs = []
    proverbs.append(entry)
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(proverbs, f, ensure_ascii=False, indent=2)


def get_stats():
    """Returns a count of proverbs submitted by region"""
    if not os.path.exists(PROVERB_FILE):
        return {}

    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        proverbs = json.load(f)

    # Extract region and count
    region_counts = Counter(p.get("region", "Unknown") for p in proverbs if isinstance(p, dict))
    return dict(region_counts)


def load_proverbs():
    """Load all saved proverbs"""
    if os.path.exists(PROVERB_FILE):
        with open(PROVERB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []
