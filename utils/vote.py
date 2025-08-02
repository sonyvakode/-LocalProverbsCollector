from .core import load_stats, save_stats

def get_all():
    return load_stats()

def like_proverb(proverb):
    stats = load_stats()
    stats.setdefault(proverb, {"likes": 0, "views": 0, "saves": 0})
    stats[proverb]["likes"] += 1
    save_stats(stats)

def view_proverb(proverb):
    stats = load_stats()
    stats.setdefault(proverb, {"likes": 0, "views": 0, "saves": 0})
    stats[proverb]["views"] += 1
    save_stats(stats)

def save_proverb_stat(proverb):
    stats = load_stats()
    stats.setdefault(proverb, {"likes": 0, "views": 0, "saves": 0})
    stats[proverb]["saves"] += 1
    save_stats(stats)
