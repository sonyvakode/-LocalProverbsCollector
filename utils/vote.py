import random
import json
import os

PROVERB_FILE = "proverbs.json"

def get_random():
    """Return a random proverb from the file"""
    if not os.path.exists(PROVERB_FILE):
        return None

    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        proverbs = json.load(f)

    if not proverbs:
        return None

    proverb_entry = random.choice(proverbs)
    return proverb_entry.get("text", "No proverb found.")
