import os
import json

PROVERB_FILE = "data/proverbs.txt"
STATS_FILE = "data/stats.json"

def save_proverb(text, region=None):
    os.makedirs("data", exist_ok=True)

    # Save the proverb
    with open(PROVERB_FILE, "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")

    # Update stats
    stats = load_stats()

    # Total submission counter
    stats["total_submitted"] = stats.get("total_submitted", 0) + 1

    # Region counter
    if region:
        if "regions" not in stats:
            stats["regions"] = {}
        stats["regions"][region] = stats["regions"].get(region, 0) + 1

    # Save back to stats file
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(stats, f, indent=2)

def load_stats():
    if not os.path.exists(STATS_FILE):
        return {"total_submitted": 0, "regions": {}}
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)
