# utils/audio.py

from gtts import gTTS
import tempfile
import os
import streamlit as st

def speak_text(text, lang_code):
    """
    Converts the given text to speech using gTTS and plays it in Streamlit.

    Args:
        text (str): The proverb or text to convert to speech.
        lang_code (str): The language code for TTS (e.g., 'en', 'hi', 'ta').
    """
    try:
        # Generate TTS
        tts = gTTS(text=text, lang=lang_code)

        # Save to a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            st.audio(tmp_file.name)  # Play the audio in Streamlit

        # Optionally delete file after playback (uncomment below if needed)
        # os.remove(tmp_file.name)

    except Exception as e:
        st.error(f"🔊 TTS Error: {e}")
