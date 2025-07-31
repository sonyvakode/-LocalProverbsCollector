from utils.core import load_proverbs
import json

PROVERB_FILE = "data/proverbs.json"

def record_vote(index):
    data = load_proverbs()
    if 0 <= index < len(data):
        data[index]["votes"] = data[index].get("votes", 0) + 1
        with open(PROVERB_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
