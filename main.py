import streamlit as st
import random
import base64
from utils import core, translate, vote, audio, language

st.set_page_config(page_title="Indian Wisdom: Local Proverbs Collector", layout="centered")

# Transparent background setup (uses Baground.jpg)
def set_background(image_path):
    with open(image_path, "rb") as image_file:
        encoded = base64.b64encode(image_file.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}
        .block-container {{
            background-color: rgba(255, 255, 255, 0.88);
            padding: 2rem;
            border-radius: 10px;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("Baground.jpg")

# Load data
all_proverbs = core.load_proverbs()
all_stats = core.load_stats()

# Sidebar Navigation
page = st.sidebar.radio("Navigate", ["Home", "Proverb of the day", "Stats", "Leadership"])

# 🏠 Home Page: Submit a Proverb
if page == "Home":
    st.title("📜 Indian Wisdom: Local Proverbs Collector")

    st.subheader("📝 Submit a Proverb")
    nickname = st.text_input("Enter your nickname")
    proverb = st.text_area("Write a proverb")
    region = st.selectbox("Select region", ["North", "South", "East", "West", "Central"])
    audio_file = st.file_uploader("Or upload audio", type=["wav", "mp3", "m4a"])

    if audio_file:
        transcribed = audio.transcribe_audio(audio_file)
        if transcribed:
            st.success(f"Transcribed: {transcribed}")
            proverb = transcribed

    if st.button("Submit"):
        if nickname and proverb:
            core.save_proverb(nickname, proverb, region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.error("❌ Please enter both nickname and proverb.")

# 🌟 Proverb of the Day
elif page == "Proverb of the day":
    st.title("🌟 Proverb of the Day")
    if all_proverbs:
        selected_proverb = random.choice(all_proverbs)
        proverb_text = selected_proverb.get("proverb", "")
        lang_options = language.language_map.keys()
        display_lang = st.selectbox("Choose language", lang_options)
        translated = translate.translate_text(proverb_text, display_lang)
        st.info(f"💬 {translated}")
    else:
        st.warning("No proverbs found.")

# 📊 Stats Page
elif page == "Stats":
    st.title("📊 Submission Stats")
    if all_stats:
        st.write(f"Total Proverbs: {all_stats.get('total_proverbs', 0)}")
        st.bar_chart(all_stats.get("region_counts", {}))
    else:
        st.warning("No stats available.")

# 🏆 Leadership Page
elif page == "Leadership":
    st.title("🏆 Leadership Board")
    leaderboard = vote.get_all()
    if leaderboard:
        sorted_leaders = sorted(leaderboard.items(), key=lambda x: x[1].get("likes", 0), reverse=True)
        for i, (user, stats) in enumerate(sorted_leaders[:10], start=1):
            st.markdown(f"**{i}. {user}** — 👍 {stats.get('likes', 0)} likes")
    else:
        st.warning("No leadership data found.")
