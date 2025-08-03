import json
import os

DATA_PATH = "data/stats.json"

def _load_data():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_data(data):
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def like_proverb(proverb_text):
    data = _load_data()
    for item in data:
        if item["proverb"] == proverb_text:
            item["likes"] += 1
            break
    else:
        data.append({"proverb": proverb_text, "likes": 1, "views": 1})
    _save_data(data)

def view_proverb(proverb_text):
    data = _load_data()
    for item in data:
        if item["proverb"] == proverb_text:
            item["views"] += 1
            break
    else:
        data.append({"proverb": proverb_text, "likes": 0, "views": 1})
    _save_data(data)

def get_all():
    return _load_data()
