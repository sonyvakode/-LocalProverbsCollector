import streamlit as st
import random
import datetime
from utils import core, translate, vote, audio

# -------------------- Background Setup --------------------
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        bg_data = img_file.read()
    bg_base64 = base64.b64encode(bg_data).decode()
    page_bg = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/png;base64,{bg_base64}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    .proverb-text {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 1rem;
        border-radius: 1rem;
    }}
    </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

import base64
set_background("Background.jpg")

# -------------------- Title --------------------
st.markdown("<h1 style='text-align: center;'>📜 <b>Indian Wisdom: Local Proverbs Collector</b></h1>", unsafe_allow_html=True)

# -------------------- Load Proverbs --------------------
def load_proverbs():
    try:
        with open("data/proverbs.txt", "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

all_proverbs = load_proverbs()

# -------------------- Proverb of the Day --------------------
st.subheader("📝 Proverb of the day")
if all_proverbs:
    # Deterministic daily rotation using date
    today_index = datetime.datetime.now().timetuple().tm_yday % len(all_proverbs)
    selected_proverb = all_proverbs[today_index]
    st.markdown(f"<div class='proverb-text'>{selected_proverb}</div>", unsafe_allow_html=True)
else:
    selected_proverb = None
    st.warning("No proverbs found.")

# -------------------- Translate Section --------------------
st.subheader("🌐 Translate a Proverb")
display_lang = st.selectbox("Select language", ["en", "hi", "bn", "ta", "te", "gu", "ml", "mr", "pa"])
if selected_proverb:
    translated = translate.translate_text(selected_proverb, display_lang)
    st.success(f"**Translated:** {translated}")
else:
    st.info("No proverb available to translate.")

# -------------------- Submit Section --------------------
st.subheader("✍️ Submit a Proverb")
with st.form("submit_form"):
    new_proverb = st.text_area("Write a local proverb")
    region = st.text_input("Which state or region?")
    audio_file = st.file_uploader("Optional: Upload Audio", type=["wav", "mp3"])
    submitted = st.form_submit_button("Submit")
    if submitted:
        if new_proverb:
            core.save_proverb(new_proverb)
            st.success("Proverb submitted successfully!")
        if audio_file:
            transcription = audio.transcribe_audio(audio_file)
            st.info(f"Transcribed: {transcription}")

# -------------------- Stats Section --------------------
st.subheader("📊 Stats")
stats = core.load_stats()
st.write(f"Total Proverbs: {stats.get('count', 0)}")
