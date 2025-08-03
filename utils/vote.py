import os

DATA_FILE = "data/proverbs.txt"

def get_all():
    all_data = []
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line:
                    # Fake a structure since file only stores proverbs
                    # You can change this if you store city info too
                    all_data.append({"city": "Unknown", "proverb": line})
    return all_data

def like_proverb(proverb):
    # Placeholder if you plan to implement like/save later
    pass
