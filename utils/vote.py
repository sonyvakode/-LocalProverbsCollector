import json
from utils.core import load_proverbs

DATA_FILE = "data/proverbs.json"

def record_vote(index):
    proverbs = load_proverbs()
    if 0 <= index < len(proverbs):
        proverbs[index]["votes"] = proverbs[index].get("votes", 0) + 1
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(proverbs, f, ensure_ascii=False, indent=2)
