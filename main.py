import streamlit as st
from utils import core, vote
from utils.translate import translate_text
import os

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# ---- Theme Styling ----
with st.sidebar:
    st.title("Choose Mode")
    theme = st.radio("Choose Theme", ["Light", "Dark", "Colorful"])
    page = st.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# Inject theme CSS
if theme == "Dark":
    st.markdown(
        "<style>body { background-color: #1e1e1e; color: white; } .stApp { font-family: 'Segoe UI'; }</style>",
        unsafe_allow_html=True,
    )
elif theme == "Colorful":
    st.markdown(
        "<style>body { background: linear-gradient(to right, #f9d423, #ff4e50); color: white; } .stApp { font-family: 'Segoe UI'; }</style>",
        unsafe_allow_html=True,
    )
else:  # Light theme
    st.markdown(
        "<style>body { background: linear-gradient(to right, #e3ffe7, #d9e7ff); color: black; } .stApp { font-family: 'Segoe UI'; }</style>",
        unsafe_allow_html=True,
    )

# ---- Pages ----
if page == "Submit":
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
        if text:
            lang_code = lang_map[chosen_lang]
            result = translate_text(text, lang_code)
            st.success(result)
        else:
            st.warning("Please enter a proverb to translate.")

elif page == "Stats":
    st.header("📊 Region-wise Contributions")
    stats = core.get_stats()
    if stats:
        st.json(stats)
    else:
        st.warning("No statistics available yet.")

elif page == "Proverb of the Day":
    st.header("🎁 Today's Proverb")
    proverb = vote.get_random()
    if proverb:
        st.success(proverb)
    else:
        st.warning("No proverb found.")

elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More app configuration settings coming soon.")
