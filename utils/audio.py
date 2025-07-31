from pathlib import Path

AUDIO_DIR = Path("audio_uploads")
AUDIO_DIR.mkdir(exist_ok=True)

def save_audio_file(uploaded_file):
    file_path = AUDIO_DIR / uploaded_file.name
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return str(file_path)
