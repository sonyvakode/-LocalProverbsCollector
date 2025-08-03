import json
import os

STATS_FILE = "data/stats.json"

def _load_stats():
    if not os.path.exists(STATS_FILE):
        return []
    with open(STATS_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def _save_stats(data):
    with open(STATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def get_all():
    """Return list of all proverbs with likes/views for leaderboard."""
    return _load_stats()

def like_proverb(proverb_text):
    """Increment like count for a proverb."""
    data = _load_stats()
    for item in data:
        if item.get("proverb") == proverb_text:
            item["likes"] = item.get("likes", 0) + 1
            break
    else:
        data.append({"proverb": proverb_text, "likes": 1, "views": 0})
    _save_stats(data)

def view_proverb(proverb_text):
    """Increment view count for a proverb."""
    data = _load_stats()
    for item in data:
        if item.get("proverb") == proverb_text:
            item["views"] = item.get("views", 0) + 1
            break
    else:
        data.append({"proverb": proverb_text, "likes": 0, "views": 1})
    _save_stats(data)
