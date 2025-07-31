import os
import json
from datetime import datetime
import shutil

PROVERB_FILE = "data/proverbs.json"
AUDIO_DIR = "data/audio"

def load_proverbs():
    if not os.path.exists(PROVERB_FILE):
        return []
    with open(PROVERB_FILE, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_proverb(proverb, region, audio_file=None):
    data = load_proverbs()
    entry = {
        "proverb": proverb,
        "region": region,
        "timestamp": datetime.now().isoformat(),
        "votes": 0
    }

    if audio_file:
        os.makedirs(AUDIO_DIR, exist_ok=True)
        audio_path = os.path.join(AUDIO_DIR, audio_file.name)
        with open(audio_path, "wb") as out_file:
            shutil.copyfileobj(audio_file, out_file)
        entry["audio"] = audio_path

    os.makedirs("data", exist_ok=True)
    data.append(entry)
    with open(PROVERB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_stats():
    data = load_proverbs()
    stats = {}
    for entry in data:
        region = entry.get("region", "Unknown")
        stats[region] = stats.get(region, 0) + 1
    return stats
