# main.py

import streamlit as st
import os
import pandas as pd
import speech_recognition as sr

from utils.core import load_proverbs, save_proverb
from utils.translate import translate_proverb
from utils.vote import record_vote
from utils.audio import speak_text
from utils.language import get_supported_languages

# ------------------------ Setup ------------------------
st.set_page_config(page_title="Local Proverbs Collector", layout="centered")

if "proverbs" not in st.session_state:
    st.session_state.proverbs = load_proverbs()

if "theme" not in st.session_state:
    st.session_state.theme = "Light"

# ------------------------ Title ------------------------
st.title("🌾 Local Proverbs Collector")

# ------------------------ Sidebar ------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    theme = st.radio("Choose Theme", ["Light", "Dark"])
    lang = st.selectbox("Select Language", get_supported_languages())
    st.markdown("---")
    st.write("🧠 AI-powered preservation of Indian wisdom.")

# Apply theme
if theme == "Dark":
    st.markdown("""
        <style>
        body {
            background-color: #0E1117;
            color: #FAFAFA;
        }
        </style>
    """, unsafe_allow_html=True)

# ------------------------ Input Form ------------------------
with st.form("proverb_form"):
    st.subheader("✍️ Add a New Proverb")

    # Voice input
    st.markdown("🎙️ Or record your proverb:")
    if st.form_submit_button("🎤 Start Voice Input"):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("Listening...")
            audio = recognizer.listen(source)
        try:
            recognized_text = recognizer.recognize_google(audio)
            st.session_state.voice_input = recognized_text
            st.success(f"Recognized: {recognized_text}")
        except Exception as e:
            st.error(f"Speech recognition failed: {e}")
            st.session_state.voice_input = ""
    else:
        st.session_state.voice_input = ""

    # Text input field (auto-filled from voice if available)
    proverb = st.text_input("Enter a proverb in your language:", value=st.session_state.voice_input)
    meaning = st.text_area("Optional: Enter its meaning or context")
    submitted = st.form_submit_button("Submit Proverb")

    if submitted and proverb:
        save_proverb(proverb, meaning, lang)
        st.success("✅ Proverb saved successfully!")
        st.session_state.proverbs = load_proverbs()  # Refresh list

# ------------------------ Display Proverbs ------------------------
st.subheader("📜 Collected Proverbs")

if st.session_state.proverbs:
    for i, item in enumerate(st.session_state.proverbs):
        with st.expander(f"{item['text']} [{item['language']}]"):
            st.write(f"**Meaning:** {item.get('meaning', 'N/A')}")
            if not item.get('meaning'):
                st.caption("🧠 Suggested meaning: A timeless piece of folk wisdom.")

            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button(f"🔊 Hear", key=f"tts_{i}"):
                    speak_text(item['text'], item['language'])
            with col2:
                if st.button(f"🌐 Translate", key=f"trans_{i}"):
                    translation = translate_proverb(item['text'], item['language'], 'en')
                    st.info(f"Translation: {translation}")
            with col3:
                if st.button(f"👍 Vote", key=f"vote_{i}"):
                    record_vote(i)
                    st.success("Thank you for your vote!")
else:
    st.warning("No proverbs collected yet. Be the first to contribute!")

# ------------------------ Statistics ------------------------
st.markdown("---")
st.subheader("📊 Proverbs Stats")

df = pd.DataFrame(st.session_state.proverbs)

if not df.empty:
    st.write("🔢 Total Proverbs:", len(df))
    st.bar_chart(df['language'].value_counts())
    st.write("🔥 Top Voted:")
    top_voted = df.sort_values(by='votes', ascending=False).head(5)
    st.table(top_voted[['text', 'language', 'votes']])
else:
    st.info("No data yet. Add some proverbs to see stats.")
