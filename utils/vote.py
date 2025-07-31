from utils.core import load_proverbs, save_proverb
import json

def vote_proverb(index):
    data = load_proverbs()
    if 0 <= index < len(data):
        data[index]["votes"] = data[index].get("votes", 0) + 1
        with open("data/proverbs.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
