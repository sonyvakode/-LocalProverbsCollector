import streamlit as st
import pandas as pd
import os
import platform
import speech_recognition as sr
from utils.translate import translate_proverb
from utils.audio import speak_text
from utils.core import load_proverbs, save_proverb, get_language_code

# ---------- CONFIG -----------
st.set_page_config(page_title="Local Proverbs Collector", layout="centered")

# ---------- SESSION STATE -----------
if "theme" not in st.session_state:
    st.session_state.theme = "light"
if "language" not in st.session_state:
    st.session_state.language = "en"

# ---------- HEADER -----------
st.markdown("""
    <h1 style='text-align: center;'>📚 Local Proverbs Collector</h1>
    <p style='text-align: center;'>AI-powered preservation of Indian wisdom.</p>
    """, unsafe_allow_html=True)

# ---------- SIDEBAR -----------
st.sidebar.header("⚙️ Settings")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
lang = st.sidebar.selectbox("Select Language", ["en", "hi", "ta", "te", "bn", "ml", "kn", "gu", "mr"])

st.session_state.theme = theme.lower()
st.session_state.language = lang

# ---------- APPLY THEME -----------
if st.session_state.theme == "dark":
    st.markdown("""
        <style>
        body, .stApp { background-color: #1e1e1e; color: white; }
        </style>
    """, unsafe_allow_html=True)

# ---------- INPUT -----------
st.subheader("📝 Add a New Proverb")
proverb = st.text_area("Or record your proverb:")

# ---------- VOICE INPUT -----------
if st.button("🎙️ Start Voice Input"):
    if "streamlit" in platform.platform().lower():
        st.warning("Voice input is not supported on Streamlit Cloud. Please use text input.")
    else:
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                st.info("Listening... Please speak your proverb.")
                audio = recognizer.listen(source, timeout=5)
                proverb = recognizer.recognize_google(audio, language=lang)
                st.success(f"Captured: {proverb}")
        except Exception as e:
            st.error(f"Voice input failed: {e}")

# ---------- SAVE PROVERB -----------
if st.button("✅ Submit Proverb"):
    if proverb.strip() != "":
        save_proverb(proverb, lang)
        st.success("Proverb submitted!")
    else:
        st.warning("Please enter or record a proverb first.")

# ---------- TTS & TRANSLATION -----------
st.subheader("🧠 Tools for Understanding")
if st.button("🔊 Hear the Proverb"):
    if proverb:
        speak_text(proverb, get_language_code(lang))
    else:
        st.warning("Enter a proverb first.")

if st.button("🌐 Translate to English"):
    if proverb:
        translated = translate_proverb(proverb, lang, "en")
        st.info(f"Translation: {translated}")
    else:
        st.warning("Enter a proverb first.")

# ---------- STATS -----------
st.subheader("📊 Proverbs Collected")
proverbs_data = load_proverbs()
if not proverbs_data.empty:
    st.dataframe(proverbs_data.tail(10))
else:
    st.info("No proverbs collected yet. Be the first to contribute!")
