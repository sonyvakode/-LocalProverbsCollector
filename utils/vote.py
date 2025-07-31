from .core import load_proverbs, save_proverb
import json

DATA_FILE = "proverbs.json"

def increment_vote(selected_proverb):
    data = load_proverbs()
    for p in data:
        if p["proverb"] == selected_proverb:
            p["votes"] += 1
            break
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_random():
    import random
    data = load_proverbs()
    return random.choice(data)["proverb"] if data else None
