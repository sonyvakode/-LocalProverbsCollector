import streamlit as st
import os
import base64
import random
from utils import core, translate, vote, audio

# === Set Page Config ===
st.set_page_config(page_title="Indian Wisdom", layout="centered")

# === Set Background ===
def set_background(image_file):
    with open(image_file, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("background.jpg")

# === Sidebar Navigation ===
page = st.sidebar.radio("Navigate", ["🏠 Home", "📝 Submit", "🌐 Translate", "📊 Stats"])

# === HOME PAGE ===
if page == "🏠 Home":
    st.title("🪔 Indian Wisdom: Local Proverbs Collector")

    if not os.path.exists("data/proverbs.txt"):
        open("data/proverbs.txt", "w", encoding="utf-8").close()

    with open("data/proverbs.txt", "r", encoding="utf-8") as f:
        proverbs = [line.strip().split(" | ")[0] for line in f if line.strip()]

    if proverbs:
        proverb = random.choice(proverbs)
        st.markdown(f"### 🌟 Proverb of the Day:\n> *{proverb}*")

        if st.button("❤️ Like this proverb"):
            vote.like_proverb(proverb)

        likes = vote.get_all().get(proverb, 0)
        st.caption(f"👍 Likes: {likes}")
    else:
        st.info("No proverbs submitted yet.")

# === SUBMIT PAGE ===
elif page == "📝 Submit":
    st.header("📥 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")
    region = st.text_input("Enter your location or region")
    audio_file = st.file_uploader("🎙️ Or upload an audio file", type=["mp3", "wav"])

    if audio_file:
        proverb = audio.transcribe_audio(audio_file)
        st.success(f"Transcribed Proverb: {proverb}")

    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("Proverb submitted successfully!")
        else:
            st.warning("Please enter a proverb before submitting.")

# === TRANSLATE PAGE ===
elif page == "🌐 Translate":
    st.header("🌐 Translate a Proverb")
    text = st.text_input("Enter proverb to translate")
    target = st.selectbox("Choose language", ["Hindi", "Tamil", "Telugu", "Kannada", "Bengali"])

    if st.button("Translate"):
        if text:
            translated = translate.translate_proverb(text, target)
            st.success(f"Translation ({target}): {translated}")
        else:
            st.warning("Enter some text to translate.")

# === STATS PAGE ===
elif page == "📊 Stats":
    st.header("📊 Proverbs by Region")
    stats = core.load_stats()
    if stats["regions"]:
        st.bar_chart(stats["regions"])
    else:
        st.info("No data yet. Submit some proverbs to see stats.")
