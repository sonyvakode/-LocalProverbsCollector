import streamlit as st
import random
import base64
import time
from utils import core, translate, vote
from utils.audio import transcribe_audio

# --- Background Setup ---
def set_background():
    image_url = "https://t4.ftcdn.net/jpg/08/04/67/63/360_F_804676330_hVxnVs6vGpu1uL6WmNL6qxSApym3zxUF.jpg"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.6)), url("{image_url}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        .card {{
            background-color: white;
            padding: 1rem;
            border-radius: 15px;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            margin-bottom: 1rem;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background()

# --- App Title ---
st.markdown("<h1>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Proverb of the Day ---
st.subheader("🌟 Proverb of the Day")

proverbs = core.load_proverbs()
if not proverbs:
    st.info("No proverbs yet. Add one below!")
else:
    samples = random.sample(proverbs, min(3, len(proverbs)))
    for p in samples:
        views = vote.get_views(p["text"])
        likes = vote.get_likes(p["text"])
        with st.container():
            st.markdown(f"""
            <div class='card'>
                <b>📜 Proverb:</b> {p["text"]}<br>
                🌐 <b>Language:</b> {p["language"]} &nbsp;&nbsp;📍 <b>Region:</b> {p["region"]}<br>
                👁️ <b>Views:</b> {views} &nbsp;&nbsp;❤️ <b>Likes:</b> {likes}
            </div>
            """, unsafe_allow_html=True)
            col1, col2 = st.columns([1, 1])
            with col1:
                if st.button(f"❤️ Like", key=f"like_{p['text']}"):
                    vote.like_proverb(p["text"])
            with col2:
                vote.increment_view(p["text"])

# --- Submit a Proverb ---
st.subheader("➕ Submit a New Proverb")
with st.form("submit_form"):
    text = st.text_input("Enter a proverb")
    region = st.selectbox("Select region", ["Kerala", "Maharashtra", "Punjab", "Tamil Nadu", "West Bengal"])
    language = st.selectbox("Language", ["English", "Hindi", "Tamil", "Bengali", "Malayalam"])
    submitted = st.form_submit_button("Submit")
    if submitted and text:
        core.save_proverb(text, region, language)
        st.success("Proverb submitted successfully!")

# --- Translate Tool ---
st.subheader("🌐 Translate a Proverb")
input_text = st.text_input("Enter text to translate")
target_lang = st.selectbox("Translate to", ["Hindi", "English", "Tamil", "Bengali"])
if st.button("Translate"):
    if input_text:
        result = translate.translate_text(input_text, target_lang)
        st.success(f"Translated: {result}")
    else:
        st.warning("Please enter text to translate.")

# --- Audio Upload ---
st.subheader("🎙️ Upload Voice")
audio_file = st.file_uploader("Upload an audio file (WAV/MP3)", type=["wav", "mp3"])
if audio_file:
    with st.spinner("Transcribing..."):
        result = transcribe_audio(audio_file)
        st.success(f"Transcribed Text: {result}")

# --- Top Contributors Leaderboard ---
st.subheader("🏆 Top Proverbs by Likes")
stats = vote.get_all()
if stats:
    top = sorted(stats.items(), key=lambda x: x[1]["likes"], reverse=True)[:5]
    for proverb, data in top:
        st.markdown(f"🔹 **{proverb}** — ❤️ {data['likes']} Likes, 👁️ {data['views']} Views")
else:
    st.info("No votes yet.")
