# utils/audio.py

import os
from datetime import datetime

def save_audio(file, region):
    folder = os.path.join("data", "audio")
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{region}_{timestamp}_{file.name}"
    filepath = os.path.join(folder, filename)

    with open(filepath, "wb") as f:
        f.write(file.read())

    return filepath
