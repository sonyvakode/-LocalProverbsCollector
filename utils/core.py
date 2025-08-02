import os
import json

PROVERB_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def load_proverbs():
    if not os.path.exists(PROVERB_FILE):
        return []
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def save_proverb(proverb):
    with open(PROVERB_FILE, "a", encoding="utf-8") as f:
        f.write(proverb.strip() + "\n")

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_stats(stats):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
