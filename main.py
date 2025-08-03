import streamlit as st
import random
import base64
from utils import core, translate, vote, audio

# ========== Background ========== #
def set_background():
    try:
        with open("background.jpg", "rb") as img_file:
            img_bytes = img_file.read()
        encoded = base64.b64encode(img_bytes).decode()
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/jpg;base64,{encoded}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        pass

set_background()

# ========== Page Title ========== #
st.markdown("<h1 style='text-align: center;'>📜 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)

# ========== Sidebar Navigation ========== #
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "Stats"])

# ========== Home Page ========== #
if page == "Home":
    st.markdown("<h3 style='text-align: center;'>Submit Your Proverb</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #444;'>Collect and preserve the rich heritage of Indian proverbs in your language.</p>", unsafe_allow_html=True)

    # Input fields
    proverb = st.text_input("Enter the local proverb")
    region = st.text_input("Enter your city or region")

    # Audio upload (placed next to input)
    st.markdown("Upload Audio (Optional):")
    audio_file = st.file_uploader("Choose an audio file...", type=["wav", "mp3"], label_visibility="collapsed")

    if audio_file:
        transcript = audio.transcribe_audio(audio_file)
        if transcript:
            st.success(f"Transcribed Text: {transcript}")
            if not proverb:
                proverb = transcript

    if st.button("Submit"):
        if proverb and region:
            core.save_proverb(proverb, region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("⚠️ Please enter both proverb and region.")

# ========== Proverb of the Day Page ========== #
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

# ========== Stats Page ========== #
elif page == "Stats":
    st.markdown("<h3>📊 Submission Stats & Leaderboard</h3>", unsafe_allow_html=True)

    stats = core.load_stats()
    total = stats.get("total_submitted", 0)
    st.info(f"📈 Total Proverbs Submitted: **{total}**")

    region_filter = st.selectbox("Filter by Region (Optional)", [
        "All", "Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru",
        "Hyderabad", "Lucknow", "Jaipur", "Ahmedabad", "Patna"
    ])

    region_counts = stats.get("regions", {})

    if region_filter != "All":
        count = region_counts.get(region_filter, 0)
        st.success(f"📍 Proverbs from **{region_filter}**: **{count}**")
    else:
        st.markdown("### 🏆 Leaderboard by Region")
        sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)
        if not sorted_regions:
            st.warning("No regional data available yet.")
        else:
            for region, count in sorted_regions:
                st.markdown(f"- 🌆 **{region}**: `{count}` proverbs")
