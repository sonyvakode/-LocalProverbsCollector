import os
import json

DATA_TXT = "data/proverbs.txt"
DATA_JSON = "data/data.json"

def save_proverb(proverb, city, language, meaning=""):
    # Save plain proverb to proverbs.txt
    with open(DATA_TXT, "a", encoding="utf-8") as f:
        f.write(f"{proverb}\n")

    # Load existing JSON data
    if os.path.exists(DATA_JSON):
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            try:
                all_data = json.load(f)
            except json.JSONDecodeError:
                all_data = []
    else:
        all_data = []

    # Append new entry
    entry = {
        "proverb": proverb,
        "city": city,
        "language": language,
        "meaning": meaning
    }
    all_data.append(entry)

    # Save updated JSON data
    with open(DATA_JSON, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

def load_stats():
    try:
        with open(DATA_JSON, "r", encoding="utf-8") as f:
            data = json.load(f)
        return {"total_proverbs": len(data)}
    except:
        return {"total_proverbs": 0}
