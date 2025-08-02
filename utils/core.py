import json
import os

PROVERB_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def save_proverb(proverbs, append=False):
    all_proverbs = get_all()
    if append:
        all_proverbs.extend(proverbs)
    else:
        all_proverbs = proverbs
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        for proverb in all_proverbs:
            f.write(json.dumps(proverb) + "\n")
    save_stats(all_proverbs)

def get_all():
    if not os.path.exists(PROVERB_FILE):
        return []
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f if line.strip()]

def save_stats(proverbs):
    language_counts = {}
    for p in proverbs:
        lang = p.get("language", "Unknown")
        language_counts[lang] = language_counts.get(lang, 0) + 1
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(language_counts, f)

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
