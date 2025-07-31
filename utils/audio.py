import os

AUDIO_DIR = "data/audio"

def save_audio_file(audio_file):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    file_path = os.path.join(AUDIO_DIR, audio_file.name)
    with open(file_path, "wb") as f:
        f.write(audio_file.read())
