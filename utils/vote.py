from .core import load_data, save_data

def get_all():
    return load_data()

def like_proverb(text):
    data = load_data()
    for p in data:
        if p["text"] == text:
            p["likes"] += 1
            break
    save_data(data)
