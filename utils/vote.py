from .core import load_proverbs
from pathlib import Path

DATA_FILE = "data/proverbs.txt"

def _write_all(proverbs):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for p in proverbs:
            f.write(f"{p[0]}|{p[1]}|{p[2]}|{p[3]}|{p[4]}\n")

def like_proverb(text):
    proverbs = load_proverbs()
    for i, p in enumerate(proverbs):
        if p[0] == text:
            proverbs[i] = (p[0], p[1], p[2], p[3], p[4] + 1)
            break
    _write_all(proverbs)

def increment_view(text):
    proverbs = load_proverbs()
    for i, p in enumerate(proverbs):
        if p[0] == text:
            proverbs[i] = (p[0], p[1], p[2], p[3] + 1, p[4])
            break
    _write_all(proverbs)

def get_top_liked(n=5):
    proverbs = load_proverbs()
    sorted_proverbs = sorted(proverbs, key=lambda x: x[4], reverse=True)
    return [(p[0], p[4]) for p in sorted_proverbs[:n]]
