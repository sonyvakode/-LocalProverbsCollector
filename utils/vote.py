from .core import load_proverbs, DATA_FILE
import json

def increment_vote(proverb_text):
    data = load_proverbs()
    for item in data:
        if item["proverb"] == proverb_text:
            item["votes"] += 1
            break
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
