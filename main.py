import streamlit as st
from utils import core, translate, vote
import base64
import os

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# ---- Set background via base64 image ----
def set_background(image_path):
    with open(image_path, "rb") as img_file:
        img_data = base64.b64encode(img_file.read()).decode()
    page_bg = f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{img_data}");
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
    """
    st.markdown(page_bg, unsafe_allow_html=True)

# 🔧 Set your own background image here (place your file in the same folder or adjust path)
set_background("utils/assets/streamlit_bg_gradient.png")  # Make sure this image exists

# ---- Sidebar Navigation ----
with st.sidebar:
    st.header("🧭 Navigation")
    page = st.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# ---- Pages ----
if page == "Submit":
    st.title("🪔 Indian Wisdom: Local Proverbs Collector")
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
        st.json(stats)
    else:
        st.warning("No statistics available yet.")

elif page == "Proverb of the Day":
    st.header("🌞 Proverb of the Day")
    all_proverbs = core.load_proverbs()
    if not all_proverbs:
        st.warning("No proverbs found.")
    else:
        for p in all_proverbs[:5]:  # Show top 5 proverbs
            st.markdown(f"#### 📝 {p['proverb']}")
            col1, _ = st.columns([1, 5])
            with col1:
                if st.button("❤️", key=p['proverb']):
                    vote.increment_vote(p['proverb'])
                    st.success("Thanks for liking!")

elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More app configuration options coming soon.")
