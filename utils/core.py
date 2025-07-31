import json
import os

DATA_FILE = "proverbs.json"

def load_proverbs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_proverb(text, meaning, language):
    proverbs = load_proverbs()
    proverbs.append({
        "text": text,
        "meaning": meaning,
        "language": language,
        "votes": 0
    })
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(proverbs, f, ensure_ascii=False, indent=2)
