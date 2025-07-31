from utils.core import load_proverbs
import json

PROVERB_FILE = "data/proverbs.json"

def cast_vote(index, upvote=True):
    proverbs = load_proverbs()
    if 0 <= index < len(proverbs):
        proverbs[index]["votes"] = proverbs[index].get("votes", 0) + (1 if upvote else -1)
        with open(PROVERB_FILE, "w", encoding="utf-8") as f:
            json.dump(proverbs, f, ensure_ascii=False, indent=2)
