import streamlit as st
from utils import core, translate, vote, audio, language
import random
import os
import base64

# Set background from background.jpg
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    bg_img = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }}
    </style>
    """
    st.markdown(bg_img, unsafe_allow_html=True)

# Load background
if os.path.exists("background.jpg"):
    set_background("background.jpg")

# Sidebar-style navigation with st.selectbox
st.title("📜 Indian Wisdom: Local Proverbs Collector")

pages = ["Submit Proverb", "Proverb of the Day", "Translate Proverb", "Stats"]
page = st.selectbox("Choose a section", pages)

# Page 1: Submit Proverb
if page == "Submit Proverb":
    st.header("✍️ Share Your Local Proverb")

    lang = st.selectbox("Select Language", language.languages())
    region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central"])
    proverb = st.text_area("Write your proverb here")

    audio_file = st.file_uploader("🎙️ Upload an audio file", type=["wav", "mp3", "ogg"])
    if audio_file:
        try:
            transcribed = audio.transcribe_audio(audio_file)
            st.success(f"Transcribed: {transcribed}")
            proverb = transcribed
        except Exception as e:
            st.error(f"Transcription failed: {e}")

    if st.button("Submit"):
        if proverb.strip():
            core.save_proverb(proverb, lang, region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("Please enter or upload a proverb first.")

# Page 2: Proverb of the Day
elif page == "Proverb of the Day":
    st.header("🌞 Proverb of the Day")
    proverbs = core.load_proverbs()
    if proverbs:
        selected = random.choice(proverbs)
        st.markdown(f"""
            <div style="padding:20px; background-color:#ffffffcc; border-radius:12px; margin-top:10px;">
                <h3 style="text-align:center;">“{selected['text']}”</h3>
                <p style="text-align:center; font-style:italic;">Language: {selected['language']}</p>
            </div>
        """, unsafe_allow_html=True)
        st.info("Refresh the page to see a new proverb.")
    else:
        st.warning("No proverbs available yet. Please add some!")

# Page 3: Translate
elif page == "Translate Proverb":
    st.header("🌐 Translate a Proverb")
    text = st.text_input("Enter a proverb to translate")
    target_lang = st.selectbox("Translate to", language.languages())
    if st.button("Translate"):
        if text.strip():
            translated = translate.translate_text(text, target_lang)
            st.success(f"Translated: {translated}")
        else:
            st.warning("Please enter a proverb to translate.")

# Page 4: Stats
elif page == "Stats":
    st.header("📊 Proverb Submission Stats")
    stats = core.load_stats()
    if stats:
        total = sum(stats.values())
        st.write(f"Total Proverbs Submitted: **{total}**")
        st.bar_chart(stats)
    else:
        st.info("No data available yet.")
