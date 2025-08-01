import streamlit as st
import random
import time
from utils import core, vote, translate, audio

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# ---- Background via base64 URL (no assets folder) ----
bg_url = "https://t4.ftcdn.net/jpg/08/04/67/63/360_F_804676330_hVxnVs6vGpu1uL6WmNL6qxSApym3zxUF.jpg"
st.markdown(f"""
    <style>
        .stApp {{
            background-image: url('{bg_url}');
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
        }}
    </style>
""", unsafe_allow_html=True)

# ---- App Title ----
st.markdown("<h1 style='text-align: center;'>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)
st.markdown("---")

# ---- Navigation ----
page = st.sidebar.radio("Go to", ["Proverb of the Day", "Submit", "Translate", "Stats"])

# ---- Proverb of the Day ----
if page == "Proverb of the Day":
    st.subheader("✨ Proverb of the Day")

    all_proverbs = vote.get_all()
    if not all_proverbs:
        st.warning("No proverbs available yet.")
    else:
        proverb = random.choice(all_proverbs)
        proverb_text = proverb.get("proverb", "No proverb text found.")
        likes = proverb.get("likes", 0)

        st.markdown(f"""
            <div style='padding:20px; background-color: rgba(255, 255, 255, 0.8); border-radius: 10px; text-align: center;'>
                <h3>{proverb_text}</h3>
                <form action="" method="post">
                    <button name="like" type="submit">❤️ {likes}</button>
                </form>
            </div>
        """, unsafe_allow_html=True)

        if st.button("❤️ Like this proverb"):
            vote.like_proverb(proverb_text)
            st.experimental_rerun()

        st.info("New proverbs will refresh automatically when you revisit this page.")

# ---- Submit Page ----
elif page == "Submit":
    st.subheader("📝 Submit a Local Proverb")

    proverb = st.text_area("Type the proverb in your local language")
    region = st.selectbox("Choose your region", [
        "Andhra Pradesh", "Bihar", "Gujarat", "Karnataka", "Kerala",
        "Madhya Pradesh", "Maharashtra", "Odisha", "Punjab", "Rajasthan",
        "Tamil Nadu", "Telangana", "Uttar Pradesh", "West Bengal", "Other"
    ])
    audio_file = st.file_uploader("Or upload audio (MP3/WAV)", type=["mp3", "wav"])

    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("✅ Proverb submitted successfully!")
        elif audio_file:
            transcribed = audio.transcribe_audio(audio_file)
            core.save_proverb(transcribed, region)
            st.success("✅ Proverb from audio submitted successfully!")
        else:
            st.warning("Please enter a proverb or upload audio.")

# ---- Translate Page ----
elif page == "Translate":
    st.subheader("🌐 Translate a Proverb")

    proverb_text = st.text_input("Enter a proverb to translate")

    lang_map = {
        "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn",
        "Bengali": "bn", "Marathi": "mr", "Malayalam": "ml", "Gujarati": "gu",
        "Punjabi": "pa", "Urdu": "ur", "Assamese": "as", "Odia": "or",
        "Sanskrit": "sa", "English": "en", "Arabic": "ar", "French": "fr",
        "Spanish": "es", "German": "de", "Chinese": "zh-CN", "Japanese": "ja",
        "Russian": "ru", "Korean": "ko", "Portuguese": "pt", "Italian": "it"
    }

    target_lang = st.selectbox("Translate to", list(lang_map.keys()))
    if st.button("Translate"):
        if proverb_text.strip():
            translated = translate.translate(proverb_text, lang_map[target_lang])
            st.success(f"Translated: {translated}")
        else:
            st.warning("Please enter a proverb first.")

# ---- Stats Page ----
elif page == "Stats":
    st.subheader("📊 Region-wise Proverbs Stats")
    stats = core.load_stats()
    if stats:
        st.bar_chart(stats)
    else:
        st.info("No statistics to display yet.")
