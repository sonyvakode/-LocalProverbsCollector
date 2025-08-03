import streamlit as st
import random
import base64
from utils import core, translate, vote, audio, language

# ========== Background Image Setup (Background.jpg with capital B) ========== #
def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-attachment: fixed;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background("Background.jpg")

# ========== App Title ========== #
st.markdown(
    "<h1 style='text-align: center; color: black;'>Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)

# ========== Navigation ========== #
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "Stats"])

# ========== Home Page ========== #
if page == "Home":
    st.markdown("""
    <div style='padding: 10px; background-color: rgba(255, 255, 255, 0.85); border-left: 5px solid #f4b400; border-radius: 5px; font-weight: 500; color: #333;'>
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
            proverb = transcript  # Override text area with audio text

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
                background-color: rgba(255,255,255,0.9);
                padding: 20px;
                border-radius: 12px;
                margin-top: 20px;
                font-size: 20px;
                color: #333;
            '>
                <div><strong>Original:</strong> {selected_proverb}</div>
                <div style='margin-top: 10px;'><strong>Translated:</strong> {translated}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No proverbs available in the file yet.")

    if st.button("🔄 Next Proverb"):
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
