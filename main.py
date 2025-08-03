import streamlit as st
import random
import time
from datetime import datetime, timedelta
from utils import core, translate, vote, audio, language

# ========== Transparent Light Background Styling ========== #
st.markdown("""
    <style>
    .stApp {
        background-color: rgba(255, 240, 245, 0.2);  /* Light transparent background */
    }
    </style>
""", unsafe_allow_html=True)

# ========== Bold Centered Title ========== #
st.markdown(
    "<h1 style='text-align: center; font-weight: bold; color: black;'>Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)

# ========== Navigation ========== #
page = st.sidebar.selectbox("📚 Navigate", ["Home", "Today’s Featured Proverb", "Stats"])

# ========== Home Page ========== #
if page == "Home":
    st.markdown("""
    <div style='padding: 10px; background-color: #fff7e6; border-left: 5px solid #f4b400; border-radius: 5px; font-weight: 500;'>
    Local proverbs carry the timeless wisdom and vibrant culture of every Indian region—share yours!
    </div>
    """, unsafe_allow_html=True)

    region = st.selectbox("Select Your Region (State/City)", [
        "Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru",
        "Hyderabad", "Lucknow", "Jaipur", "Ahmedabad", "Patna"
    ])
    lang = st.selectbox("Select Language", language.get_all_languages())
    proverb = st.text_area("Enter the proverb in local language")

    audio_file = st.file_uploader("🎤 Upload an audio proverb", type=["wav", "mp3", "m4a"])
    if audio_file is not None:
        transcript = audio.transcribe_audio(audio_file)
        if transcript:
            st.success("Transcribed Text:")
            st.write(transcript)
            proverb = transcript

    if st.button("✅ Submit Proverb"):
        if proverb.strip():
            core.save_proverb(proverb.strip())
            st.success("Proverb submitted successfully!")
        else:
            st.warning("Please enter or upload a proverb before submitting.")

    st.markdown("---")
    st.subheader("🌐 Translate a Proverb")
    input_text = st.text_input("Enter a proverb to translate")
    target_lang = st.selectbox("Translate to", language.get_all_languages())

    if st.button("🌍 Translate"):
        if input_text.strip():
            translated = translate.translate_text(input_text.strip(), target_lang)
            st.success(f"Translated: {translated}")
        else:
            st.warning("Please enter a proverb to translate.")

# ========== Proverb of the Day Page ========== #
elif page == "Today’s Featured Proverb":
    st.subheader("📝 Today’s Featured Proverb")

    # Load proverbs
    proverbs = core.load_proverbs()
    if proverbs:
        now = datetime.now()
        if 'proverb_of_the_day' not in st.session_state or 'timestamp' not in st.session_state:
            st.session_state.proverb_of_the_day = random.choice(proverbs)
            st.session_state.timestamp = now
        else:
            elapsed = now - st.session_state.timestamp
            if elapsed > timedelta(hours=24):  # change daily
                st.session_state.proverb_of_the_day = random.choice(proverbs)
                st.session_state.timestamp = now

        proverb = st.session_state.proverb_of_the_day
        translated = translate.translate_text(proverb, "English")

        st.markdown(f"""
            <div style='
                background-color: rgba(255,255,255,0.9);
                padding: 20px;
                border-radius: 12px;
                margin-top: 20px;
                font-size: 20px;
                color: #333;
            '>
                <div><strong>Original:</strong> {proverb}</div>
                <div style='margin-top: 10px;'><strong>Translated:</strong> {translated}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No proverbs submitted yet.")

    if st.button("🔄 Next Proverb"):
        st.session_state.proverb_of_the_day = random.choice(proverbs)
        st.session_state.timestamp = datetime.now()
        st.rerun()

# ========== Stats Page ========== #
elif page == "Stats":
    st.subheader("📊 Submission Stats")

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
        for region, count in sorted_regions:
            st.markdown(f"- **{region}**: {count} proverbs")
