from gtts import gTTS
import tempfile
import streamlit as st

def speak_text(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
            tts.save(tmp_file.name)
            st.audio(tmp_file.name)
    except Exception as e:
        st.error(f"TTS error: {e}")
