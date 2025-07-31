import streamlit as st
from utils import core, translate, vote
import os

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# ---- Sidebar Theme & Navigation ----
with st.sidebar:
    st.title("Choose Mode")
    theme = st.radio("Choose Theme", ["Light", "Dark", "Colorful"])
    page = st.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# ---- Inject Theme Styling ----
if theme == "Dark":
    st.markdown("""
        <style>
        body { background-color: #1e1e1e; color: white; }
        .stApp { font-family: 'Segoe UI'; }
        </style>
    """, unsafe_allow_html=True)
elif theme == "Colorful":
    st.markdown("""
        <style>
        body {
            background: linear-gradient(to right, #f9d423, #ff4e50);
            color: white;
        }
        .stApp { font-family: 'Segoe UI'; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
        body {
            background: linear-gradient(to right, #e3ffe7, #d9e7ff);
            color: black;
        }
        .stApp { font-family: 'Segoe UI'; }
        .category-btn {
            background-color: #fff7e6;
            padding: 10px 18px;
            border-radius: 8px;
            margin: 8px;
            display: inline-block;
            font-size: 16px;
            font-weight: 500;
            border: 1px solid #ccc;
        }
        </style>
    """, unsafe_allow_html=True)

# ---- PAGE: Submit ----
if page == "Submit":
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

# ---- PAGE: Translate ----
elif page == "Translate":
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

# ---- PAGE: Stats ----
elif page == "Stats":
    st.header("📊 Region-wise Contributions")
    stats = core.get_stats()
    if stats:
        st.json(stats)
    else:
        st.warning("No statistics available yet.")

# ---- PAGE: Proverb of the Day ----
elif page == "Proverb of the Day":
    st.markdown("### 🎁 Proverb of the Day")

    proverb = vote.get_random()
    if proverb:
        st.markdown("""
            <div style="background-color: #fff2cc; border-left: 6px solid orange;
                        padding: 16px; border-radius: 12px; margin-bottom: 10px;">
                <h3 style="color: #333;">📜 {}</h3>
                <em style="color: #555;">Brought from the heart of Indian villages.</em>
                <hr style="margin-top: 10px; margin-bottom: 10px;">
                <div style="display: flex; justify-content: space-between; font-size: 14px;">
                    <span>❤️ 997</span>
                    <span>👁 309</span>
                    <span>⏱ 1 min read</span>
                </div>
            </div>
        """.format(proverb), unsafe_allow_html=True)
    else:
        st.warning("No proverb found.")

    st.markdown("### 🧾 Read by category:")
    categories = [
        ("❤️ Love", "Love"), ("🏃 Motivation", "Motivation"),
        ("🧠 Wisdom", "Wisdom"), ("💼 Work", "Work"),
        ("👑 Philosophy", "Philosophy"), ("🫀 Ethics & Morals", "Ethics & Morals")
    ]
    for i in range(0, len(categories), 2):
        cols = st.columns(2)
        for j in range(2):
            if i + j < len(categories):
                label, name = categories[i + j]
                with cols[j]:
                    st.markdown(f'<div class="category-btn">{label}</div>', unsafe_allow_html=True)

# ---- PAGE: Settings ----
elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More app configuration settings coming soon.")
