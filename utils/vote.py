import random
from .core import load_proverbs, update_metric

def increment_vote(proverb_text):
    update_metric(proverb_text, "votes")

def increment_like(proverb_text):
    update_metric(proverb_text, "likes")

def increment_save(proverb_text):
    update_metric(proverb_text, "saves")

def increment_view(proverb_text):
    update_metric(proverb_text, "views")

def get_random():
    proverbs = load_proverbs()
    if not proverbs:
        return None
    selected = random.choice(proverbs)
    increment_view(selected["proverb"])
    return selected["proverb"]
