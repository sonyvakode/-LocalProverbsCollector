import streamlit as st
import random
import os
from utils import core, translate, vote, audio, language

st.set_page_config(page_title="Indian Wisdom", layout="wide")

# Remove background
st.markdown(
    """
    <style>
    .stApp {
        background: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Navigation
page = st.sidebar.radio("Navigate", ["Submit Proverb", "Proverb of the Day", "Translate", "Stats"])

# Page 1: Submit Proverb
if page == "Submit Proverb":
    st.title("📝 Submit a Local Proverb")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central"])
        lang = st.selectbox("Select Language", language.languages())
        proverb = st.text_area("Write your proverb here")
        if st.button("Submit Proverb"):
            if proverb:
                core.save_proverb(proverb, lang, region)
                st.success("Proverb submitted successfully!")
            else:
                st.error("Please enter a proverb before submitting.")
    
    with col2:
        st.markdown("#### 🎤 Upload Audio")
        audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3", "m4a"])
        if audio_file:
            text = audio.transcribe_audio(audio_file)
            if text:
                st.info("Transcribed Proverb:")
                st.write(text)

# Page 2: Proverb of the Day
elif page == "Proverb of the Day":
    st.title("🌞 Proverb of the Day")
    proverbs = core.load_proverbs()
    if proverbs:
        random_proverb = random.choice(proverbs)
        st.markdown(f"""
            <div style='
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 20px;
                margin: 20px 0;
                background-color: #f9f9f9;
                font-size: 22px;
                text-align: center;'>
                {random_proverb['text']}<br>
                <small><i>{random_proverb['lang'].capitalize()} — {random_proverb['region']}</i></small>
            </div>
        """, unsafe_allow_html=True)
        if st.button("Next Proverb"):
            st.rerun()
    else:
        st.warning("No proverbs found yet. Submit one first!")

# Page 3: Translate
elif page == "Translate":
    st.title("🌍 Translate a Proverb")
    text_to_translate = st.text_input("Enter proverb to translate")
    target_language = st.selectbox("Translate to", language.languages())
    if st.button("Translate"):
        if text_to_translate:
            translated = translate.translate_text(text_to_translate, target_language)
            st.success(f"Translated: {translated}")
        else:
            st.error("Please enter a proverb to translate.")

# Page 4: Stats
elif page == "Stats":
    st.title("📊 App Statistics")
    stats = core.load_stats()
    total = stats.get("total_proverbs", 0)
    st.metric(label="Total Proverbs Submitted", value=str(total))
