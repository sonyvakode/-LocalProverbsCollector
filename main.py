import streamlit as st
import random
import base64
from utils import core, translate, vote, audio, language

# Set page config
st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Set background image with light overlay
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        textarea, input, select {{
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
            border-radius: 5px !important;
        }}
        label, .stSelectbox > div, .stTextInput > div, .stTextArea > div {{
            color: #111 !important;
            font-weight: 500 !important;
        }}
        .solid-box {{
            background-color: #ffffffcc;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
        .center {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("Background.jpg")

# Title with icon
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)

# Load proverbs
all_proverbs = core.load_proverbs()

# Proverb of the Day section
if all_proverbs:
    st.markdown("<h3 style='text-align: center;'>📝 Proverb of the Day</h3>", unsafe_allow_html=True)

    selected_proverb = random.choice(all_proverbs)
    st.markdown(
        f"<div class='solid-box'><h5 style='text-align: center;'>{selected_proverb}</h5></div>",
        unsafe_allow_html=True,
    )

    # Language selection for translation
    lang = st.selectbox("Select Language", language.get_all_languages())
    translated = translate.translate_text(selected_proverb, lang)
    st.markdown(f"**Translated:** {translated}")

    if st.button("Next Proverb"):
        st.experimental_rerun()

# Submit Proverb
st.markdown("<h3>💡 Submit Your Proverb</h3>", unsafe_allow_html=True)
with st.form("submit_form"):
    proverb = st.text_area("Enter a local proverb")
    city = st.text_input("City or Region")
    audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
    submitted = st.form_submit_button("Submit")
    if submitted:
        if audio_file:
            proverb_from_audio = audio.transcribe_audio(audio_file)
            st.write("Transcribed:", proverb_from_audio)
            proverb = proverb or proverb_from_audio
        if proverb and city:
            core.save_proverb(proverb, city)
            st.success("✅ Proverb saved successfully!")
        else:
            st.error("❌ Please provide both proverb and city/region.")

# Translation Section
st.markdown("<h3>🌍 Translate a Proverb</h3>", unsafe_allow_html=True)
to_translate = st.text_input("Enter proverb to translate")
target_lang = st.selectbox("Choose target language", language.get_all_languages(), key="translate_lang")
if st.button("Translate"):
    if to_translate:
        translated = translate.translate_text(to_translate, target_lang)
        st.success(f"Translated: {translated}")
    else:
        st.warning("Enter a proverb to translate.")

# Stats Section
st.markdown("<h3>📊 Proverbs Stats</h3>", unsafe_allow_html=True)
stats = core.load_stats()
st.write(f"Total Proverbs Collected: {stats.get('total_proverbs', 0)}")
