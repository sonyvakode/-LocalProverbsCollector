import streamlit as st
import random
from utils import core, translate, vote, audio, language

# ========== Transparent Light Background ========== #
st.markdown("""
    <style>
    .stApp {
        background-color: rgba(255, 192, 203, 0.15);
    }
    </style>
    """, unsafe_allow_html=True
)

# ========== App Title ========== #
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)

# ========== Navigation ========== #
page = st.sidebar.selectbox("📚 Navigate", ["Home", "Proverb of the Day", "Stats"])

# ========== Home Page ========== #
if page == "Home":
    st.subheader("✨ Submit a Local Proverb")

    region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central", "Northeast"])
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
elif page == "Proverb of the Day":
    st.subheader("🌟 Proverb of the Day")
    proverbs = core.load_proverbs()
    if proverbs:
        selected_proverb = random.choice(proverbs)
        display_lang = random.choice(language.get_all_languages())
        translated = translate.translate_text(selected_proverb, display_lang)

        st.markdown(f"""
            <div style='
                background-color: rgba(255,255,255,0.85);
                padding: 20px;
                border-radius: 12px;
                margin-top: 20px;
                font-size: 22px;
                text-align: center;
                color: #333;
            '>
                <strong>{translated}</strong>
                <div style='margin-top: 10px; font-size: 14px; color: #555;'>Language: {display_lang}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No proverbs submitted yet.")

    if st.button("🔁 Next Proverb"):
        st.rerun()

# ========== Stats Page ========== #
elif page == "Stats":
    st.subheader("📊 Submission Stats")
    stats = core.load_stats()
    total = stats.get("total_submitted", 0)
    st.info(f"📈 Total Proverbs Submitted: **{total}**")
