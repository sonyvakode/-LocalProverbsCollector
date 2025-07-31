import random
import os

def get_random():
    path = "data/proverbs.txt"
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if not lines:
        return None
    return random.choice(lines)
