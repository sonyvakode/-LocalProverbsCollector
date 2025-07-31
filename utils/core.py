import os
from collections import Counter

def save_proverb(text, region):
    os.makedirs("data", exist_ok=True)
    with open("data/proverbs.txt", "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")

def get_stats():
    path = "data/proverbs.txt"
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    lang_counts = Counter([detect_lang(l) for l in lines])
    return dict(lang_counts)

def detect_lang(text):
    if "।" in text: return "Hindi"
    if "తె" in text or "డు" in text: return "Telugu"
    if "அ" in text: return "Tamil"
    if "ಕ" in text: return "Kannada"
    if "স" in text: return "Bengali"
    return "Unknown"
