import streamlit as st
import random
import base64
from utils import core, translate, vote, audio, language

# Page setup
st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Light background setup
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

# Title
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)

# Sidebar Navigation
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "Stats"])

# Page: Home
if page == "Home":
    st.markdown("<h3>Submit Your Proverb</h3>", unsafe_allow_html=True)
    st.markdown("<p style='color: #444;'>Contribute local wisdom from your region, in your language or dialect. Help preserve India’s cultural voice.</p>", unsafe_allow_html=True)

    with st.form("submit_form"):
        proverb = st.text_area("Enter a local proverb")
        city = st.text_input("City or Region")
        lang = st.selectbox("Language of the proverb", language.get_all_languages(), key="lang_submit")
        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            if audio_file:
                proverb_from_audio = audio.transcribe_audio(audio_file)
                st.write("Transcribed:", proverb_from_audio)
                proverb = proverb or proverb_from_audio
            if proverb and city:
                def save_proverb(proverb, city, language):
                st.success("✅ Proverb saved successfully!")
            else:
                st.error("❌ Please provide both proverb and city/region.")

    st.markdown("<h3>🌍 Translate a Proverb</h3>", unsafe_allow_html=True)
    to_translate = st.text_input("Enter proverb to translate")
    target_lang = st.selectbox("Choose target language", language.get_all_languages(), key="translate_lang")
    if st.button("Translate"):
        if to_translate:
            translated = translate.translate_text(to_translate, target_lang)
            st.success(f"Translated: {translated}")
        else:
            st.warning("Enter a proverb to translate.")

# ========== Proverb of the Day Page ==========
elif page == "Proverb of the day":
    st.subheader("📝 Proverb of the day")

    try:
        with open("data/proverbs.txt", "r", encoding="utf-8") as f:
            all_proverbs = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        all_proverbs = []

    if all_proverbs:
        selected_proverb = random.choice(all_proverbs)
        display_lang = "English"
        translated = translate.translate_text(selected_proverb, display_lang)

        st.markdown(f"""
            <div style='
                background-color: #ffffff;
                padding: 24px;
                border-radius: 10px;
                margin: 30px auto 20px;
                font-size: 18px;
                color: #222;
                width: 90%;
                max-width: 700px;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            '>
                <div><strong>Original:</strong> {selected_proverb}</div>
                <div style='margin-top: 12px;'><strong>Translated:</strong> {translated}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No proverbs available in the file yet.")

    st.markdown("<div style='margin-top: 25px; text-align: center;'>", unsafe_allow_html=True)
    if st.button("🔄 Next Proverb"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Page: Stats
elif page == "Stats":
    st.markdown("<h3>📊 Proverbs Stats</h3>", unsafe_allow_html=True)
    stats = core.load_stats()
    st.write(f"Total Proverbs Collected: {stats.get('total_proverbs', 0)}")

    st.markdown("<h4>🏆 Leaderboard</h4>", unsafe_allow_html=True)
    all = vote.get_all()
    region_counts = {}
    for item in all:
        region = item.get("city", "Unknown")
        region_counts[region] = region_counts.get(region, 0) + 1

    sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)

    if sorted_regions:
        for i, (region, count) in enumerate(sorted_regions[:10], start=1):
            st.write(f"{i}. {region}: {count} proverbs")
    else:
        st.info("Leaderboard data not available yet.")
