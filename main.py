import streamlit as st
import random
import time
import base64
from utils import core, translate, vote, audio

# Set page config
st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            color: #fff;
        }}
        .section {{
            background-color: rgba(0, 0, 0, 0.6);
            padding: 2rem;
            border-radius: 1rem;
            margin-bottom: 1rem;
        }}
        h1, h2, h3, p {{
            color: white !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background.jpg")

# Title
st.markdown("<h1 style='text-align: center;'>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)

# Proverb of the Day
def show_proverb_of_the_day():
    all_proverbs = core.load_proverbs()
    if not all_proverbs:
        st.warning("No proverbs available.")
        return

    proverb = random.choice(all_proverbs)
    text, language, region, views, likes = proverb

    vote.increment_view(text)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🌟 Proverb of the Day")
        st.markdown(f"**📝 Proverb:** {text}")
        st.markdown(f"🌐 **Language:** {language} | 📍 **Region:** {region}")
        st.markdown(f"👁️ Views: {views + 1} | ❤️ Likes: {likes}")
    with col2:
        if st.button("❤️ Like", key="like_btn"):
            vote.like_proverb(text)
            st.experimental_rerun()

show_proverb_of_the_day()

# Submit new proverb
with st.expander("➕ Submit a New Proverb"):
    st.markdown("### ✍️ Add a Proverb")
    proverb = st.text_input("Enter a proverb")
    region = st.selectbox("Select region", ["Maharashtra", "Kerala", "Punjab", "Gujarat", "Assam", "Tamil Nadu"])
    language = st.selectbox("Language", ["Hindi", "Marathi", "Tamil", "Telugu", "Malayalam", "English"])
    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, language, region)
            st.success("Proverb submitted!")
        else:
            st.warning("Please enter a proverb.")

# Translate a proverb
with st.expander("🌐 Translate a Proverb"):
    st.markdown("### 🔁 Translate")
    input_text = st.text_input("Enter proverb to translate")
    from_lang = st.selectbox("From Language", ["en", "hi", "ta", "te", "ml"])
    to_lang = st.selectbox("To Language", ["hi", "en", "ta", "te", "ml"])
    if st.button("Translate"):
        if input_text:
            translated = translate.translate_text(input_text, from_lang, to_lang)
            st.success(f"Translated: {translated}")
        else:
            st.warning("Please enter a proverb to translate.")

# Audio upload + transcription
with st.expander("🎤 Upload an Audio Proverb"):
    st.markdown("### 🗣️ Voice Input")
    uploaded_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])
    if uploaded_file is not None:
        transcription = audio.transcribe_audio(uploaded_file)
        if transcription:
            st.success(f"Transcribed Text: {transcription}")
        else:
            st.error("Could not transcribe audio.")

# Show Stats as top-liked leaderboard
with st.expander("📊 Top Proverbs"):
    st.markdown("### 🏆 Leaderboard (Most Liked)")
    top = vote.get_top_liked()
    for i, p in enumerate(top, 1):
        st.markdown(f"{i}. **{p[0]}** (❤️ {p[1]})")

