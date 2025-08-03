import streamlit as st
import random
import datetime
import base64
from utils import core, translate, vote, audio

# -------------------- Background Setup --------------------
def set_background(image_path):
    try:
        with open(image_path, "rb") as image_file:
            bg_data = image_file.read()
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
            font-size: 18px;
        }}
        </style>
        """
        st.markdown(page_bg, unsafe_allow_html=True)
    except FileNotFoundError:
        st.error("⚠️ Background image not found. Please ensure 'Background.jpg' is present.")

set_background("Background.jpg")  # Make sure case matches your file exactly

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
    try:
        translated = translate.translate_text(selected_proverb, display_lang)
        st.success(f"**Translated:** {translated}")
    except Exception as e:
        st.error(f"Translation failed: {e}")
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

# -------------------- Leaderboard Section --------------------
st.subheader("🏆 Leaderboard")
all_votes = vote.get_all()

if all_votes:
    sorted_votes = sorted(all_votes, key=lambda x: (x.get("likes", 0), x.get("views", 0)), reverse=True)
    for idx, item in enumerate(sorted_votes[:5], start=1):
        st.markdown(
            f"""
            <div style='padding:10px; background-color:#f9f9f9; border-radius:10px; margin-bottom:10px;'>
                <b>#{idx}</b> — {item.get("proverb", "No text")}
                <br>❤️ {item.get("likes", 0)} &nbsp;&nbsp; 👁️ {item.get("views", 0)}
            </div>
            """, unsafe_allow_html=True
        )
else:
    st.info("No leaderboard data available yet.")
