import streamlit as st
import random
from utils import core, vote, translate, audio
from streamlit_extras.stylable_container import stylable_container

# Load proverbs and stats
proverbs = core.load_proverbs()
stats = core.load_stats()

# Page setup
st.set_page_config(page_title="Indian Wisdom", page_icon="📜", layout="centered")

# Custom Styling
st.markdown("""
    <style>
        body {
            background-color: #fff9f2;
        }
        .proverb-box {
            padding: 2rem;
            border-radius: 1.5rem;
            background-color: #fff;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            text-align: center;
            margin-top: 2rem;
        }
        .proverb-text {
            font-size: 1.5rem;
            font-style: italic;
            margin-bottom: 1rem;
        }
        .proverb-meta {
            font-size: 0.9rem;
            color: #555;
        }
    </style>
""", unsafe_allow_html=True)

# App Title
st.markdown("### 📜 *Indian Wisdom*")
st.markdown("Discover, submit, and celebrate the timeless wisdom of Indian proverbs.")

# --- Proverb of the Day Section ---
st.markdown("## 🌟 Proverb of the Day")

if proverbs:
    # Session state to rotate proverbs
    if 'current_index' not in st.session_state:
        st.session_state.current_index = random.randint(0, len(proverbs) - 1)

    current_proverb = proverbs[st.session_state.current_index]

    # Proverb Display
    with st.container():
        st.markdown(f"""
        <div class="proverb-box">
            <div class="proverb-text">"{current_proverb['text']}"</div>
            <div class="proverb-meta">🌐 Language: {current_proverb['language']} &nbsp;&nbsp;📍 Region: {current_proverb['region']}</div>
        </div>
        """, unsafe_allow_html=True)

    # Button to load another proverb
    if st.button("🔁 Next Proverb"):
        st.session_state.current_index = random.randint(0, len(proverbs) - 1)
else:
    st.warning("No proverbs yet.")

# --- Submit Proverb Section ---
st.markdown("## ✍️ Submit a Proverb")

with st.form("submit_form"):
    text = st.text_input("Enter the proverb")
    language = st.selectbox("Language", ["Hindi", "Tamil", "Telugu", "Kannada", "Malayalam", "Marathi", "Gujarati", "Punjabi", "Bengali", "Urdu", "Odia", "Other"])
    region = st.text_input("Region")
    audio_file = st.file_uploader("Upload an audio proverb (optional)", type=["mp3", "wav", "m4a"])

    submitted = st.form_submit_button("Submit")

    if submitted:
        if not text and audio_file:
            text = audio.transcribe_audio(audio_file)
        if text:
            core.save_proverb(text, language, region)
            st.success("Proverb submitted successfully!")
        else:
            st.error("Please provide text or audio.")

# --- Translation Section ---
st.markdown("## 🌐 Translate a Proverb")
with st.form("translate_form"):
    text_to_translate = st.text_input("Enter proverb to translate")
    target_lang = st.selectbox("Translate to", ["en", "hi", "ta", "te", "kn", "ml", "mr", "gu", "pa", "bn", "ur", "or"])
    do_translate = st.form_submit_button("Translate")

    if do_translate:
        translated = translate.translate_proverb(text_to_translate, target_lang)
        st.success(f"Translated: {translated}")

# --- Stats Section ---
st.markdown("## 📊 App Stats")

if stats:
    st.metric("Total Proverbs", stats.get("total_proverbs", 0))
    st.metric("Most Common Language", stats.get("most_common_language", "N/A"))
    st.metric("Most Common Region", stats.get("most_common_region", "N/A"))
else:
    st.info("No stats available yet.")
