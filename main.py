# main.py

import streamlit as st
import random
from utils import core, translate, vote, audio, language

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# ---------- Custom CSS ----------
def set_background():
    st.markdown("""
        <style>
            body {
                background-color: #f6f6f6;
            }
            .main {
                padding: 2rem;
                font-family: 'Segoe UI', sans-serif;
            }
            .title {
                text-align: center;
                font-size: 2rem;
                font-weight: bold;
                color: #333333;
                margin-bottom: 1.5rem;
            }
            .section-header {
                font-size: 1.3rem;
                color: #222222;
                margin-top: 1rem;
                margin-bottom: 0.5rem;
            }
            .proverb-box {
                background-color: #ffffff;
                padding: 1rem;
                border-radius: 12px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                text-align: center;
                margin-bottom: 1rem;
            }
        </style>
    """, unsafe_allow_html=True)

set_background()

# ---------- Sidebar Navigation ----------
st.sidebar.title("📱 Navigate")
page = st.sidebar.radio("Go to", ["🏠 Proverb of the Day", "✍️ Submit", "🌐 Translate", "📊 Stats"])

# ---------- App Title ----------
st.markdown("<div class='title'>🪔 Indian Wisdom: Local Proverbs Collector</div>", unsafe_allow_html=True)

# ---------- PAGE 1: Proverb of the Day ----------
if page == "🏠 Proverb of the Day":
    st.markdown("<div class='section-header'>📜 Proverb of the Day</div>", unsafe_allow_html=True)

    all_proverbs = core.load_proverbs()
    langs = list(language.get_supported_languages().values())
    selected_lang = random.choice(langs)

    if all_proverbs:
        current = random.choice(all_proverbs).split("|")[0].strip()
        translated = translate.translate_text(current, target_lang=selected_lang)
        st.markdown(f"""
            <div class='proverb-box'>
                <div style='font-size: 1.1rem;'>💬 <b>{translated}</b></div>
                <div style='font-size: 0.85rem; color: #777;'>Language: {selected_lang}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.info("No proverbs found yet. Add one from the Submit tab.")

# ---------- PAGE 2: Submit Proverb ----------
elif page == "✍️ Submit":
    st.markdown("<div class='section-header'>✍️ Submit a Proverb</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        proverb_input = st.text_area("Enter a proverb", height=80)
        lang = st.selectbox("Select Language", list(language.get_supported_languages().keys()))
        region = st.text_input("Enter your Region (State/City)")

    with col2:
        st.markdown("#### 🎤 Or Upload Audio")
        audio_file = st.file_uploader("Upload audio file", type=["wav", "mp3"])
        if audio_file:
            with st.spinner("Transcribing..."):
                transcription = audio.transcribe_audio(audio_file)
                st.success("Transcribed Text:")
                st.write(transcription)
                proverb_input = transcription

    if st.button("Submit Proverb"):
        if proverb_input and lang and region:
            core.save_proverb(proverb_input.strip(), lang.strip(), region.strip())
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("Please fill in all fields.")

# ---------- PAGE 3: Translate ----------
elif page == "🌐 Translate":
    st.markdown("<div class='section-header'>🌐 Translate a Proverb</div>", unsafe_allow_html=True)

    to_translate = st.text_input("Enter a proverb to translate")
    target_language = st.selectbox("Translate to", list(language.get_supported_languages().keys()))

    if st.button("Translate"):
        if to_translate:
            result = translate.translate_text(to_translate, language.get_supported_languages()[target_language])
            st.info(f"Translated: {result}")
        else:
            st.warning("Enter a proverb to translate.")

# ---------- PAGE 4: Stats ----------
elif page == "📊 Stats":
    st.markdown("<div class='section-header'>📊 App Stats</div>", unsafe_allow_html=True)
    stats = core.load_stats()
    st.metric(label="Total Proverbs Submitted", value=stats.get("total_proverbs", 0))
