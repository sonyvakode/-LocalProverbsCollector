import json
import os

PROVERB_FILE = "data/proverbs.json"

def load_proverbs():
    if os.path.exists(PROVERB_FILE):
        with open(PROVERB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_proverb(text, meaning, language):
    data = load_proverbs()
    data.append({
        "text": text,
        "meaning": meaning,
        "language": language,
        "votes": 0
    })
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
