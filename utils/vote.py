# utils/vote.py

import random
import sys
import os

# Add parent directory to sys.path to allow absolute import of core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.core import load_proverbs

def get_random():
    proverbs = load_proverbs()
    if not proverbs:
        return None
    return random.choice(proverbs)["text"]
