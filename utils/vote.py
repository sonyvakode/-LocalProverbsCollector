from .core import load_proverbs
import json

DATA_FILE = "data/proverbs.txt"

def _update_proverb(target_text, key):
    proverbs = load_proverbs()
    updated = False
    for p in proverbs:
        if p["text"] == target_text:
            p[key] = p.get(key, 0) + 1
            updated = True
            break
    if updated:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            for p in proverbs:
                f.write(json.dumps(p) + "\n")

def like_proverb(text):
    _update_proverb(text, "likes")

def save_proverb(text):
    _update_proverb(text, "saves")
