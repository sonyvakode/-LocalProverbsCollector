import streamlit as st
import random
import base64
import datetime

from utils import core, vote, translate, audio, language

# Set background using the uploaded background.jpg
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
            background-repeat: no-repeat;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("background.jpg")

# ---------- App Title ----------
st.markdown("<h1 style='text-align: center;'>📚 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 16px; font-style: italic;'>Local proverbs capture the wisdom and humor of Indian communities — share yours by region!</p>", unsafe_allow_html=True)

# ---------- Proverb of the Day ----------
proverbs = core.load_proverbs()
if proverbs:
    # Automatically change daily
    today = datetime.date.today().toordinal()
    proverb_of_the_day = proverbs[today % len(proverbs)]

    st.subheader("📌 Proverb of the Day")
    st.markdown(f"<div style='padding: 10px; font-size: 18px; background-color: #ffffffaa; border-radius: 8px;'>{proverb_of_the_day}</div>", unsafe_allow_html=True)
else:
    st.info("No proverbs available yet. Submit one below!")

# ---------- Submit Section ----------
st.markdown("### 📝 Submit Your Local Proverb")
st.markdown("Share a local saying from your region (city/state) to preserve India's linguistic diversity.", unsafe_allow_html=True)

with st.form("submit_proverb"):
    proverb_text = st.text_area("Enter Proverb", height=80)
    region = st.text_input("Enter Region (City or State)")
    audio_file = st.file_uploader("Or upload audio", type=["wav", "mp3", "m4a"])
    submitted = st.form_submit_button("Submit")

    if submitted:
        if not proverb_text and audio_file:
            proverb_text = audio.transcribe_audio(audio_file)

        if proverb_text and region:
            core.save_proverb(proverb_text.strip())
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("Please enter a proverb and region, or upload audio.")

# ---------- Translate Section ----------
st.markdown("### 🌐 Translate a Proverb")
with st.form("translate_form"):
    to_translate = st.text_input("Enter proverb to translate")
    lang = st.selectbox("Select Language", language.languages())
    translated_text = ""
    if st.form_submit_button("Translate"):
        if to_translate:
            translated_text = translate.translate_text(to_translate, lang)
            st.success(f"Translation: {translated_text}")
        else:
            st.warning("Please enter a proverb to translate.")

# ---------- Stats Section ----------
st.markdown("### 📊 Submission Stats")
stats = core.load_stats()
total = stats.get("total", 0)
st.metric("Total Proverbs Submitted", total)
