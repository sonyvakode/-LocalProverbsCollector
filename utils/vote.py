# utils/vote.py

import os
import json

VOTE_FILE = "data/votes.json"

def like_proverb(proverb):
    if not os.path.exists(VOTE_FILE):
        data = {}

    else:
        with open(VOTE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

    data[proverb] = data.get(proverb, 0) + 1

    with open(VOTE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f)

def get_all():
    if not os.path.exists(VOTE_FILE):
        return {}
    with open(VOTE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
