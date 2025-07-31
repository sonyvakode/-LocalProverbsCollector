import json
import os

DATA_FILE = "proverbs.json"

def load_proverbs():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_proverb(proverb, language):
    proverbs = load_proverbs()
    proverbs.append({"proverb": proverb, "language": language})
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(proverbs, f, ensure_ascii=False, indent=2)

def get_language_code(lang_display):
    lang_map = {
        "en": "en", "hi": "hi", "ta": "ta", "te": "te", "ml": "ml", "bn": "bn", "gu": "gu", "kn": "kn", "mr": "mr", "or": "or", "pa": "pa"
    }
    return lang_map.get(lang_display, "en")
