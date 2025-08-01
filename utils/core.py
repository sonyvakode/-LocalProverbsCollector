import os
from collections import Counter

PROVERB_FILE = "data/proverbs.txt"

def save_proverb(proverb, author, region, language):
    os.makedirs("data", exist_ok=True)
    with open(PROVERB_FILE, "a", encoding="utf-8") as f:
        f.write(f"{proverb} | {author} | {region} | {language}\n")

def load_stats():
    if not os.path.exists(PROVERB_FILE):
        return {"languages": {}, "regions": {}}
    
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    language_counter = Counter()
    region_counter = Counter()

    for line in lines:
        parts = line.strip().split(" | ")
        if len(parts) == 4:
            _, _, region, language = parts
            region_counter[region] += 1
            language_counter[language] += 1

    return {
        "languages": dict(language_counter),
        "regions": dict(region_counter)
    }
