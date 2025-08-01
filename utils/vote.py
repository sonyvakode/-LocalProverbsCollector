import json

DATA_FILE = "data/proverbs.json"

def get_all():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def like_proverb(target_proverb):
    data = get_all()
    for item in data:
        if item["proverb"] == target_proverb:
            item["likes"] = item.get("likes", 0) + 1
            break
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
