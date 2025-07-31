import random
from utils.core import load_proverbs

def get_random():
    data = load_proverbs()
    if not data:
        return None
    return random.choice(data).get("proverb", None)
