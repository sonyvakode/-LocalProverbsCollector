import os

AUDIO_DIR = "audio_uploads"

def save_audio_file(file):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    file_path = os.path.join(AUDIO_DIR, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
