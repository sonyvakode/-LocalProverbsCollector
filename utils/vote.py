import json
import os

DATA_FILE = "data/stats.json"

def _load_stats():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_stats(stats):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=4, ensure_ascii=False)

def like_proverb(proverb):
    stats = _load_stats()
    if proverb not in stats:
        stats[proverb] = {"likes": 0, "views": 0, "saves": 0}
    stats[proverb]["likes"] += 1
    _save_stats(stats)

def view_proverb(proverb):
    stats = _load_stats()
    if proverb not in stats:
        stats[proverb] = {"likes": 0, "views": 0, "saves": 0}
    stats[proverb]["views"] += 1
    _save_stats(stats)

def save_proverb_stat(proverb):
    stats = _load_stats()
    if proverb not in stats:
        stats[proverb] = {"likes": 0, "views": 0, "saves": 0}
    stats[proverb]["saves"] += 1
    _save_stats(stats)

def get_all():
    return _load_stats()
