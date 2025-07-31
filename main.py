import streamlit as st
from utils import core, translate, vote
import random

# Page config
st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# Transparent Gradient Background via CSS (no external image)
st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(to bottom right, rgba(255, 245, 204, 0.8), rgba(204, 229, 255, 0.8));
        background-attachment: fixed;
        background-size: cover;
        font-family: 'Segoe UI', sans-serif;
    }
    .proverb-card {
        background: rgba(255, 255, 255, 0.6);
        padding: 1rem;
        border-radius: 12px;
        box-shadow: 0px 4px 8px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("📚 Menu")
page = st.sidebar.radio("Go to", ["📥 Submit", "🌐 Translate", "📊 Stats", "🎁 Proverb of the Day", "⚙️ Settings"])

# ---- Submit Page ----
if page == "📥 Submit":
    st.header("🪔 Indian Wisdom: Local Proverbs Collector")
    st.subheader("📝 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")
    audio = st.file_uploader("Or upload an audio file (WAV/MP3)", type=["mp3", "wav"])
    region = st.text_input("Enter your location or region")

    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("Proverb submitted successfully!")
        else:
            st.warning("Please enter a proverb before submitting.")

# ---- Translate Page ----
elif page == "🌐 Translate":
    st.header("🌐 Translate a Proverb")
    text = st.text_input("Enter proverb to translate")

    lang_map = {
        "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn",
        "Marathi": "mr", "Malayalam": "ml", "Gujarati": "gu", "Punjabi": "pa", "Urdu": "ur",
        "Assamese": "as", "Odia": "or", "Sanskrit": "sa", "English": "en", "Arabic": "ar",
        "French": "fr", "Spanish": "es", "German": "de", "Chinese": "zh-CN", "Japanese": "ja",
        "Russian": "ru", "Korean": "ko", "Portuguese": "pt", "Italian": "it", "Turkish": "tr"
    }

    chosen_lang = st.selectbox("🎯 Target language", list(lang_map.keys()))

    if st.button("Translate"):
        if text.strip():
            lang_code = lang_map[chosen_lang]
            result = translate.translate(text, lang_code)
            st.success(result)
        else:
            st.warning("Please enter a proverb to translate.")

# ---- Stats Page ----
elif page == "📊 Stats":
    st.header("📊 Region-wise Contributions")
    try:
        stats = core.get_stats()
        if stats:
            st.json(stats)
        else:
            st.info("No statistics available yet.")
    except Exception as e:
        st.error("Unable to load statistics.")

# ---- Proverb of the Day Page ----
elif page == "🎁 Proverb of the Day":
    st.header("🌞 Proverb of the Day")

    proverbs = core.load_proverbs()
    if proverbs:
        sampled = random.sample(proverbs, min(3, len(proverbs)))
        for p in sampled:
            with st.container():
                st.markdown(f"<div class='proverb-card'><strong>🧾 {p['proverb']}</strong></div>", unsafe_allow_html=True)
                if st.button("❤️ Like", key=p["proverb"]):
                    vote.increment_vote(p["proverb"])
                    st.success("You liked this proverb!")
    else:
        st.info("No proverbs available.")

# ---- Settings Page ----
elif page == "⚙️ Settings":
    st.header("⚙️ App Settings")
    st.info("Settings panel coming soon.")
