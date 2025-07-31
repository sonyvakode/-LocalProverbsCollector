import os
import hashlib

AUDIO_DIR = "data/audio"

def save_audio_file(uploaded_file, proverb_text):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    hash_id = hashlib.md5(proverb_text.encode('utf-8')).hexdigest()
    filename = f"{hash_id}_{uploaded_file.name}"
    filepath = os.path.join(AUDIO_DIR, filename)

    with open(filepath, "wb") as f:
        f.write(uploaded_file.read())
