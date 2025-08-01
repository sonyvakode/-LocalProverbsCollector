import streamlit as st
from utils import core, translate, vote, audio
import random
import base64
import time

st.set_page_config(page_title="Indian Wisdom", layout="centered", initial_sidebar_state="expanded")

# Set transparent background using base64 image
def set_background_base64(image_path):
    try:
        with open(image_path, "rb") as f:
            encoded_string = base64.b64encode(f.read()).decode()
        css = f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-attachment: fixed;
                background-repeat: no-repeat;
            }}
            </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Background image not found. Please check path.")

# Change this to any image in your root project folder
set_background_base64("streamlit_bg_gradient.png")

# Sidebar navigation
st.sidebar.title("📌 Navigate")
page = st.sidebar.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# ---------------- SUBMIT SECTION ----------------
if page == "Submit":
    st.header("📝 Submit a Local Proverb")

    proverb = st.text_area("Type your proverb in any language")

    region = st.selectbox("Select your region", [
        "Andhra Pradesh", "Telangana", "Tamil Nadu", "Karnataka", "Kerala",
        "Maharashtra", "Gujarat", "Punjab", "West Bengal", "Uttar Pradesh", "Other"
    ])

    audio_file = st.file_uploader("Or upload an audio file (MP3/WAV)", type=["mp3", "wav"])

    if audio_file is not None:
        with st.spinner("Transcribing audio..."):
            try:
                transcribed = audio.transcribe_audio(audio_file)
                st.text_area("Transcribed Text", transcribed, height=100)
                proverb = transcribed
            except Exception as e:
                st.error(f"Transcription failed: {e}")

    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("Please enter a proverb before submitting.")

# ---------------- TRANSLATE SECTION ----------------
elif page == "Translate":
    st.header("🌐 Translate a Proverb")

    text = st.text_input("Enter proverb to translate")

    lang_map = {
        "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn",
        "Marathi": "mr", "Malayalam": "ml", "Gujarati": "gu", "Punjabi": "pa", "Urdu": "ur",
        "Assamese": "as", "Odia": "or", "Sanskrit": "sa", "English": "en"
    }

    chosen_lang = st.selectbox("Translate to", list(lang_map.keys()))

    if st.button("Translate"):
        if text.strip():
            translated = translate.translate(text, lang_map[chosen_lang])
            st.success(translated)
        else:
            st.warning("Please enter a proverb first.")

# ---------------- STATS SECTION ----------------
elif page == "Stats":
    st.header("📊 Region-wise Contributions")

    try:
        stats = core.load_stats()
        if stats:
            st.bar_chart(stats)
        else:
            st.info("No stats available yet.")
    except Exception as e:
        st.error(f"Error loading stats: {e}")

# ---------------- PROVERB OF THE DAY ----------------
elif page == "Proverb of the Day":
    st.header("🎁 Proverb of the Day")

    all_proverbs = vote.get_all()
    if all_proverbs:
        random.shuffle(all_proverbs)
        for item in all_proverbs[:3]:
            proverb_text = item["proverb"]
            likes = item.get("likes", 0)

            st.markdown(f"""
                <div style='background: rgba(255, 255, 255, 0.75); padding: 20px; border-radius: 10px; margin-bottom: 10px;'>
                    <h4>{proverb_text}</h4>
                    <form action="" method="post">
                        <button type="submit" name="like" style='background:none;border:none;'>
                            ❤️ {likes}
                        </button>
                    </form>
                </div>
            """, unsafe_allow_html=True)

            if st.button(f"Like '{proverb_text[:10]}...'"):
                vote.like_proverb(proverb_text)
                st.experimental_rerun()
    else:
        st.info("No proverbs available yet.")

# ---------------- SETTINGS ----------------
elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More configuration options coming soon...")
