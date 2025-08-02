import json
import os

DATA_FILE = "utils/data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def save_proverb(text, language, region):
    data = load_data()
    new_entry = {
        "text": text,
        "language": language,
        "region": region,
        "views": 0,
        "likes": 0
    }
    data.append(new_entry)
    save_data(data)

def load_stats():
    data = load_data()
    stats = {}
    for entry in data:
        lang = entry["language"]
        stats[lang] = stats.get(lang, 0) + 1
    return stats
