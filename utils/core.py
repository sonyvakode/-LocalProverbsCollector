import os
import json

PROVERB_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def save_proverb(text, language, region):
    if not os.path.exists("data"):
        os.makedirs("data")

    # Save proverb
    with open(PROVERB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{text}||{language}||{region}\n")

    # Update stats
    stats = load_stats()
    stats[language] = stats.get(language, 0) + 1
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f)

def load_proverbs():
    if not os.path.exists(PROVERB_FILE):
        return []
    proverbs = []
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("||")
            if len(parts) == 3:
                proverbs.append({
                    "text": parts[0],
                    "language": parts[1],
                    "region": parts[2]
                })
    return proverbs

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
