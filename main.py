import streamlit as st
import random
import time
import base64
from utils import core, translate, vote, audio

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Background setup
def set_bg(image_path):
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg("background.jpg")

st.markdown("""
    <h1 style='text-align: center; font-family: Arial;'>📜 Indian Wisdom</h1>
    <p style='text-align: center;'>Discover, submit, and celebrate the timeless wisdom of Indian proverbs.</p>
""", unsafe_allow_html=True)

# Load data
all_proverbs = core.load_proverbs()

# --- Proverb of the Day ---
st.markdown("### 🌟 Proverb of the Day")
proverb_slot = st.empty()

def rotate_proverb():
    for _ in range(1):
        proverb = random.choice(all_proverbs)
        proverb_text = proverb["text"]
        lang = proverb.get("language", "Unknown")
        likes = proverb.get("likes", 0)
        views = proverb.get("views", 0)

        vote.increment_view(proverb_text)
        proverb_slot.markdown(f"""
        <div style="padding:10px; background-color: #ffffffdd; border-radius: 12px;">
            <h4 style="margin-bottom:5px;">🗣️ {proverb_text}</h4>
            <small>📌 Language: {lang}</small><br/>
            ❤️ {likes} &nbsp;&nbsp; 👁️ {views}
            <form action="" method="post">
                <input type="hidden" name="proverb" value="{proverb_text}">
                <button type="submit">Like ❤️</button>
            </form>
        </div>
        """, unsafe_allow_html=True)

rotate_proverb()

# --- Submit New Proverb ---
st.markdown("### ✍️ Submit Your Own Proverb")
with st.form("submit_form"):
    new_proverb = st.text_area("Write a local proverb")
    region = st.selectbox("Region", ["Select", "North", "South", "East", "West", "Central", "Northeast"])
    language = st.text_input("Language (e.g., Hindi, Tamil, Bengali, etc.)")

    audio_file = st.file_uploader("Optional: Upload an audio file", type=["mp3", "wav"])
    if audio_file:
        transcript = audio.transcribe_audio(audio_file)
        st.success(f"Transcription: {transcript}")

    submitted = st.form_submit_button("Submit")
    if submitted and new_proverb and region != "Select" and language:
        core.save_proverb(new_proverb, region, language)
        st.success("Proverb submitted successfully!")
    elif submitted:
        st.error("Please fill all required fields.")

# --- Translate Section ---
st.markdown("### 🌐 Translate a Proverb")
to_translate = st.text_input("Enter proverb to translate")
target_lang = st.selectbox("Translate to", ["hi", "ta", "bn", "gu", "ml", "te", "kn", "ur"])
if st.button("Translate"):
    if to_translate:
        translated = translate.translate_text(to_translate, target_lang)
        st.success(f"Translated: {translated}")
    else:
        st.error("Please enter a proverb to translate.")

# --- Stats Section ---
st.markdown("### 📊 Proverbs Overview")
stats = core.load_stats()
if stats:
    st.json(stats)
else:
    st.info("No stats available yet.")
