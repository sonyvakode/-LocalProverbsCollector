import os
import json

VOTE_FILE = "data/votes.json"

def _load_votes():
    if not os.path.exists(VOTE_FILE):
        return {}
    with open(VOTE_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_votes(votes):
    with open(VOTE_FILE, "w", encoding="utf-8") as f:
        json.dump(votes, f)

def like_proverb(proverb):
    votes = _load_votes()
    votes[proverb] = votes.get(proverb, 0) + 1
    _save_votes(votes)

def get_all():
    return _load_votes()
