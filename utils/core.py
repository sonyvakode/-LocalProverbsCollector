# utils/core.py

import os
import json

DATA_FILE = "data/proverbs.json"

def load_proverbs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_proverb(text, meaning, language):
    proverbs = load_proverbs()
    proverbs.append({
        "text": text,
        "meaning": meaning,
        "language": language,
        "votes": 0
    })
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(proverbs, f, indent=2, ensure_ascii=False)
