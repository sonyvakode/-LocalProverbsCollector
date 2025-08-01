import os

DATA_FILE = "data/proverbs.txt"

def save_proverb(text, language, region):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        f.write(f"{text}|{language}|{region}|0|0\n")

def load_proverbs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
    proverbs = [line.strip().split("|") for line in lines if line.strip()]
    for p in proverbs:
        if len(p) < 5:
            p.extend(["0"] * (5 - len(p)))  # Ensure all fields exist
    return [(p[0], p[1], p[2], int(p[3]), int(p[4])) for p in proverbs]
