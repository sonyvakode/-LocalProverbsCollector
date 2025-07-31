# utils/vote.py

import random
from utils.core import load_proverbs

def get_random():
    proverbs = load_proverbs()
    if not proverbs:
        return None
    return random.choice(proverbs)["text"]
