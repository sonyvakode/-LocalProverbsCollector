import os
import json

def save_proverb(proverb, city, language):
    os.makedirs("data", exist_ok=True)
    
    # Save to proverbs.txt
    with open("data/proverbs.txt", "a", encoding="utf-8") as f:
        f.write(proverb.strip() + "\n")

    # Save stats to stats.json
    stats_path = "data/stats.json"
    if os.path.exists(stats_path):
        with open(stats_path, "r", encoding="utf-8") as f:
            stats = json.load(f)
    else:
        stats = {"total_submitted": 0, "regions": {}, "languages": {}}

    stats["total_submitted"] = stats.get("total_submitted", 0) + 1
    stats["regions"][city] = stats["regions"].get(city, 0) + 1
    stats["languages"][language] = stats["languages"].get(language, 0) + 1

    with open(stats_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)
