import os
import shutil

def save_audio(uploaded_file, proverb_text):
    os.makedirs("data/audio", exist_ok=True)
    filename = f"{proverb_text[:30].strip().replace(' ', '_')}_{uploaded_file.name}"
    filepath = os.path.join("data/audio", filename)
    with open(filepath, "wb") as f:
        shutil.copyfileobj(uploaded_file, f)
