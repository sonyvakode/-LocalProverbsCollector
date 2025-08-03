import streamlit as st
import random
import os
import base64
from utils import core, translate, vote, audio, language

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Set background image
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded_string}");
            background-size: cover;
            background-attachment: fixed;
        }}
        .main-box {{
            background-color: rgba(255, 255, 255, 0.85);
            padding: 2rem;
            border-radius: 1rem;
            margin: 1rem auto;
            max-width: 800px;
            box-shadow: 0 0 10px rgba(0,0,0,0.2);
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("background.jpg")

# Navigation bar style
nav = st.radio(
    "Navigate",
    ["Proverb of the Day", "Submit", "Translate", "Stats"],
    horizontal=True,
)

st.markdown("<div class='main-box'>", unsafe_allow_html=True)
st.markdown("## 📜 Indian Wisdom: Local Proverbs Collector")
st.write("Contribute local Indian proverbs, translate them, and explore diverse cultural wisdom!")

# Proverb of the Day
if nav == "Proverb of the Day":
    st.subheader("🌟 Proverb of the Day")
    proverbs = vote.get_all()
    if proverbs:
        selected = random.choice(proverbs)
        st.markdown(f"**🧠 Proverb:** _{selected['text']}_")
        st.markdown(f"📍 Region: {selected.get('region', 'Unknown')} | 🌐 Language: {selected.get('language', 'Unknown')}")
    else:
        st.info("No proverbs available yet.")

# Submit Section
elif nav == "Submit":
    st.subheader("📝 Submit a Proverb")
    region = st.selectbox("Select Region", ["Delhi", "Mumbai", "Kolkata", "Chennai", "Bangalore"])
    lang = st.selectbox("Select Language", language.SUPPORTED_LANGUAGES)
    text = st.text_area("Enter your proverb in local language")
    audio_file = st.file_uploader("🎤 Or upload an audio file (MP3/WAV)", type=["mp3", "wav"])

    if st.button("Submit"):
        final_text = text
        if not final_text and audio_file:
            final_text = audio.transcribe_audio(audio_file)
            st.success("Transcribed: " + final_text)
        if final_text:
            core.save_proverb(final_text, lang, region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("Please enter or upload a proverb.")

# Translate Section
elif nav == "Translate":
    st.subheader("🌐 Translate a Proverb")
    proverbs = vote.get_all()
    if proverbs:
        selected_proverb = st.selectbox("Select a proverb", [p["text"] for p in proverbs])
        display_lang = st.selectbox("Translate to", language.SUPPORTED_LANGUAGES)
        if st.button("Translate"):
            translated = translate.translate_text(selected_proverb, display_lang)
            st.success(f"Translated: {translated}")
    else:
        st.info("No proverbs available to translate.")

# Stats Section
elif nav == "Stats":
    st.subheader("📊 App Stats")
    try:
        stats = core.load_stats()
        st.write(f"📌 Total Proverbs Submitted: **{stats.get('total_proverbs', 0)}**")
    except AttributeError:
        st.warning("Stats file missing or corrupted.")

st.markdown("</div>", unsafe_allow_html=True)
