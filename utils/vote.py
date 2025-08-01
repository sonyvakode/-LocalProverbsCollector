from . import core

def get_all():
    return core.load_proverbs()

def like_proverb(text):
    proverbs = core.load_proverbs()
    for p in proverbs:
        if p["text"] == text:
            p["likes"] += 1
            break
    _save_all(proverbs)

def _save_all(proverbs):
    with open("data/proverbs.txt", "w", encoding="utf-8") as f:
        for p in proverbs:
            line = f"{p['text']}|{p['region']}|{p['language']}|{p['likes']}|{p['views']}\n"
            f.write(line)
