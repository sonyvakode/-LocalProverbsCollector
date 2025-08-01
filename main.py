import streamlit as st
from utils import core, translate, vote, audio
import random
import time

st.set_page_config(page_title="Indian Wisdom", layout="wide")

# Background CSS with transparency
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://images.unsplash.com/photo-1503264116251-35a269479413?auto=format&fit=crop&w=1470&q=80");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        font-family: 'Segoe UI', sans-serif;
        color: #000000;
    }
    .proverb-box {
        background-color: rgba(255, 255, 255, 0.8);
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .heart-button {
        color: red;
        font-size: 24px;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Navigation")
    selected = st.radio("Choose Page", ["Submit", "Translate", "Stats", "Proverb of the Day"])

# Pages
if selected == "Submit":
    st.header("🪔 Submit a Local Proverb")
    proverb = st.text_area("Enter the proverb in your language")

    audio_file = st.file_uploader("Or upload audio (MP3/WAV)", type=["mp3", "wav"])
    if audio_file:
        proverb = audio.transcribe_audio(audio_file)

    region = st.selectbox("Choose your region", [
        "Andhra Pradesh", "Telangana", "Maharashtra", "Karnataka",
        "Tamil Nadu", "Kerala", "Punjab", "Gujarat", "West Bengal"
    ])

    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("⚠️ Please provide a proverb first.")

elif selected == "Translate":
    st.header("🌐 Translate a Proverb")
    text = st.text_input("Enter the proverb to translate")

    lang_map = {
        "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn",
        "Marathi": "mr", "Gujarati": "gu", "Punjabi": "pa", "Bengali": "bn",
        "Malayalam": "ml", "Odia": "or", "Urdu": "ur", "English": "en"
    }

    lang = st.selectbox("Choose language", list(lang_map.keys()))
    if st.button("Translate"):
        if text.strip():
            result = translate.translate(text, lang_map[lang])
            st.success(result)
        else:
            st.warning("Enter some text to translate.")

elif selected == "Stats":
    st.header("📊 Region-wise Contribution")
    stats = core.load_stats()
    if stats:
        st.bar_chart(stats)
    else:
        st.info("No data available yet.")

elif selected == "Proverb of the Day":
    st.header("🌟 Proverb of the Day")

    proverbs = vote.get_all()
    if proverbs:
        item = random.choice(proverbs)
        proverb = item.get("proverb")
        region = item.get("region", "Unknown")
        views = item.get("views", 0)
        likes = item.get("likes", 0)

        st.markdown(f"""
        <div class='proverb-box'>
            <h3>{proverb}</h3>
            <p><strong>Region:</strong> {region}</p>
            <p>❤️ Likes: {likes}</p>
            <form action='#' method='post'>
                <button name='like_button' class='heart-button'>❤️</button>
            </form>
        </div>
        """, unsafe_allow_html=True)

        if st.button("❤️ Like"):
            vote.like_proverb(proverb)
            st.experimental_rerun()

        st.caption("Refresh the app or revisit later to see a new proverb.")
    else:
        st.warning("No proverbs found.")
