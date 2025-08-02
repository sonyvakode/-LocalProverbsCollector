import streamlit as st
import random
import time
from utils import core, translate, vote, audio
from utils.language import LANGUAGES
from datetime import datetime

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# ---------- Background Styling ----------
page_bg_img = """
<style>
body {
    background-color: #f7f7f7;
    font-family: 'Segoe UI', sans-serif;
}
h1, h2, h3 {
    color: #333333;
}
.card {
    background: white;
    padding: 1.5rem;
    margin-bottom: 1.2rem;
    border-radius: 16px;
    box-shadow: 0px 2px 12px rgba(0,0,0,0.08);
}
button, .stButton>button {
    border-radius: 10px;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<h1 style='text-align:center;'>🌸 Indian Wisdom 🌸</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align:center; color:gray;'>A Collector of Local Proverbs Across Languages</h4>", unsafe_allow_html=True)
st.markdown("---")

# ---------- Proverb of the Day ----------
proverbs = core.load_proverbs()
stats = core.load_stats()

if proverbs:
    st.subheader("🌟 Proverb of the Day")
    idx = random.randint(0, len(proverbs)-1)
    proverb = proverbs[idx]
    views = stats.get(proverb, {}).get("views", 0)
    likes = stats.get(proverb, {}).get("likes", 0)

    with st.container():
        st.markdown(f"<div class='card'><h3 style='text-align:center;'>{proverb}</h3>", unsafe_allow_html=True)
        cols = st.columns(4)
        with cols[0]:
            if st.button("❤️ Like", key=f"like_{idx}"):
                vote.like_proverb(proverb)
                st.experimental_rerun()
        with cols[1]:
            st.write(f"👍 {likes}")
        with cols[2]:
            st.write(f"👁️ {views + 1}")
        with cols[3]:
            if st.button("🌐 Translate", key=f"translate_{idx}"):
                lang = st.selectbox("Translate to:", list(LANGUAGES.keys()), key=f"lang_{idx}")
                translated = translate.translate_proverb(proverb, LANGUAGES[lang])
                st.success(translated)
        st.markdown("</div>", unsafe_allow_html=True)

    vote.increment_view(proverb)
    st.markdown("---")

# ---------- Submit a Proverb ----------
st.subheader("✍️ Share Your Proverb")
with st.form("submit_proverb_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("Your Name / Nickname")
        region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central"])
    with col2:
        lang = st.selectbox("Language", list(LANGUAGES.keys()))
        audio_file = st.file_uploader("Or Upload an Audio", type=["wav", "mp3", "m4a"])

    text = st.text_area("Enter Proverb (or leave blank if using audio)")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if audio_file:
            proverb = audio.transcribe_audio(audio_file)
        else:
            proverb = text.strip()

        if proverb:
            core.save_proverb(proverb)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("⚠️ Please enter text or upload audio.")

st.markdown("---")

# ---------- Stats ----------
st.subheader("📊 Proverbs Leaderboard")
all_stats = vote.get_all()
if all_stats:
    sorted_stats = sorted(all_stats.items(), key=lambda x: x[1]["likes"], reverse=True)[:5]
    for idx, (prov, s) in enumerate(sorted_stats, 1):
        st.markdown(
            f"<div class='card'><strong>{idx}. {prov}</strong><br>❤️ Likes: {s['likes']} | 👁️ Views: {s['views']}</div>",
            unsafe_allow_html=True,
        )

# ---------- Footer ----------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:gray;'>Made with ❤️ for Indian wisdom | © 2025</p>",
    unsafe_allow_html=True
)
