import streamlit as st
from utils import core, translate, vote
import random

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# Set a nice subtle background using base64
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://images.unsplash.com/photo-1601597111158-3d91a9c2d0b3?ixlib=rb-4.0.3&auto=format&fit=crop&w=1950&q=80");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
        .like-button {
            display: inline-block;
            font-size: 24px;
            color: red;
            cursor: pointer;
            user-select: none;
            margin-top: 10px;
        }
        .like-count {
            display: inline-block;
            margin-left: 8px;
            font-weight: bold;
            color: #333;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    page = st.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# Pages
if page == "Submit":
    st.header("🪔 Indian Wisdom: Local Proverbs Collector")
    st.subheader("📝 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")
    audio = st.file_uploader("Or upload an audio file (WAV/MP3)", type=["mp3", "wav"])
    region = st.selectbox("Enter your location or region", ["Delhi", "Mumbai", "Hyderabad", "Bangalore", "Kolkata", "Other"])
    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("Proverb submitted successfully!")
        else:
            st.warning("Please enter a proverb before submitting.")

elif page == "Translate":
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

elif page == "Stats":
    st.header("📊 Region-wise Contributions")
    stats = core.get_stats()
    if stats:
        st.bar_chart(stats)
    else:
        st.warning("No statistics available yet.")

elif page == "Proverb of the Day":
    st.header("🎁 Proverb of the Day")
    proverbs = vote.get_all_proverbs()  # Ensure this returns a list of dicts like {"proverb": "...", "region": "..."}
    if proverbs:
        if 'liked_proverbs' not in st.session_state:
            st.session_state.liked_proverbs = {}

        random_index = random.randint(0, len(proverbs) - 1)
        item = proverbs[random_index]
        proverb_text = item.get("proverb", "No proverb found.")
        region = item.get("region", "Unknown region")

        # Randomly translate to a language
        display_langs = ["hi", "te", "ta", "kn", "ml", "gu", "pa", "ur", "bn"]
        target_lang = random.choice(display_langs)
        translated = translate.translate(proverb_text, target_lang)

        st.subheader(f"📍 From: {region}")
        st.markdown(f"<div style='font-size: 22px; font-style: italic;'>“{translated}”</div>", unsafe_allow_html=True)

        # Like button
        if proverb_text not in st.session_state.liked_proverbs:
            st.session_state.liked_proverbs[proverb_text] = 0

        if st.button("❤️ Like"):
            st.session_state.liked_proverbs[proverb_text] += 1

        st.markdown(f"<span class='like-count'>Likes: {st.session_state.liked_proverbs[proverb_text]}</span>", unsafe_allow_html=True)
    else:
        st.warning("No proverb available today.")

elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More configuration options coming soon.")
