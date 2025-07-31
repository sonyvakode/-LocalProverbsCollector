import streamlit as st
from utils import core, translate, vote
import base64
import random

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# ---- Custom Background Setup ----
def set_background_base64(image_path):
    with open(image_path, "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set the transparent background using your uploaded image
set_background_base64("streamlit_bg_gradient.png")  # Ensure this image is in your root folder

# ---- Sidebar Navigation ----
st.sidebar.title("📚 Menu")
page = st.sidebar.radio("Go to", ["📥 Submit", "🌐 Translate", "📊 Stats", "🎁 Proverb of the Day", "⚙️ Settings"])

# ---- Pages ----
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

elif page == "📊 Stats":
    st.header("📊 Region-wise Contributions")
    try:
        stats = core.get_stats()
        if stats:
            st.json(stats)
        else:
            st.warning("No statistics available yet.")
    except Exception as e:
        st.error("Unable to load statistics.")

elif page == "🎁 Proverb of the Day":
    st.header("🌞 Proverb of the Day")

    proverbs = core.load_proverbs()
    if proverbs:
        sampled = random.sample(proverbs, min(3, len(proverbs)))  # Show up to 3 randomly
        for p in sampled:
            with st.container():
                st.markdown(f"**🧾 {p['proverb']}**")
                liked = st.button("❤️ Like", key=p["proverb"])
                if liked:
                    vote.increment_vote(p["proverb"])
                    st.success("You liked this proverb!")
                st.markdown("---")
    else:
        st.info("No proverbs available.")

elif page == "⚙️ Settings":
    st.header("⚙️ App Settings")
    st.info("Settings panel coming soon.")
