import streamlit as st
import os
import json
from utils.core import load_proverbs, save_proverb, get_language_code
from utils.audio import speak_text
from utils.translate import translate_text
from utils.theme import set_theme
from utils.stats import display_statistics

# Set up theme
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark"])
set_theme(theme)

# Language selection
languages = ["en", "hi", "ta", "te", "ml", "bn", "kn", "gu", "mr", "pa"]
language = st.sidebar.selectbox("Select Language", languages)
lang_code = get_language_code(language)

st.sidebar.markdown("""
<small>🧠 AI-powered preservation of Indian wisdom.</small>
""", unsafe_allow_html=True)

st.title("🌱 Local Proverbs Collector")

# Add a new proverb
st.header("✍️ Add a New Proverb")
new_proverb = st.text_area("Or record your proverb:")

if st.button("✅ Submit Proverb"):
    if new_proverb.strip():
        save_proverb(new_proverb.strip(), language)
        st.success("Proverb saved!")
    else:
        st.warning("Please enter or record a proverb.")

# Tools for understanding
st.header("🧠 Tools for Understanding")
col1, col2 = st.columns(2)
with col1:
    if st.button("🔊 Hear the Proverb"):
        speak_text(new_proverb, lang_code)

with col2:
    if st.button("🌐 Translate to English"):
        translation = translate_text(new_proverb, lang_code, "en")
        st.info(f"Translation: {translation}")

# Display collected proverbs
st.header("📊 Proverbs Collected")
proverbs_data = load_proverbs()

if proverbs_data:
    for entry in proverbs_data[::-1]:
        st.markdown(f"**[{entry['language'].upper()}]** {entry['text']}")
else:
    st.info("No proverbs submitted yet.")

# Stats page
st.markdown("""---
### 📈 Statistics
""")
display_statistics(proverbs_data)
