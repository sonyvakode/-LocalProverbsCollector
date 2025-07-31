from .core import load_proverbs, save_proverb
import os
import json

PROVERB_FILE = "data/proverbs.json"

def vote_proverb(proverb_text):
    proverbs = load_proverbs()
    for p in proverbs:
        if p["proverb"] == proverb_text:
            p["votes"] = p.get("votes", 0) + 1
            break
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(proverbs, f, ensure_ascii=False, indent=2)
