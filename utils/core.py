# utils/core.py

import os
import json

PROVERBS_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def save_proverb(proverb, language, region):
    with open(PROVERBS_FILE, "a", encoding="utf-8") as f:
        f.write(f"{proverb} | {language} | {region}\n")

    if not os.path.exists(STATS_FILE):
        stats = {"total_proverbs": 0}
    else:
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            stats = json.load(f)

    stats["total_proverbs"] = stats.get("total_proverbs", 0) + 1

    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f)

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_proverbs": 0}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def load_proverbs():
    if not os.path.exists(PROVERBS_FILE):
        return []
    with open(PROVERBS_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]
