import streamlit as st
from utils import core, vote, translate, language, audio

st.set_page_config(page_title="Indian Wisdom: Local Proverbs Collector", layout="wide")
st.title("🪔 Indian Wisdom: Local Proverbs Collector")

# Sidebar Navigation
st.sidebar.title("☰ Menu")
page = st.sidebar.radio("Go to", ["📥 Submit Proverb", "📊 Vote", "🌐 Translate", "🎤 Record Audio"])

# --- Submit Proverb ---
if page == "📥 Submit Proverb":
    st.header("📥 Submit a Proverb")
    proverb = st.text_input("Enter a proverb")
    region = st.selectbox("Select the region/language", language.get_languages())
    if st.button("Submit"):
        if proverb.strip() and region:
            core.save_proverb(proverb.strip(), region)
            st.success("Proverb submitted successfully!")
        else:
            st.warning("Please fill all fields.")

# --- Vote for Proverb ---
elif page == "📊 Vote":
    st.header("📊 Vote for a Proverb")
    proverbs = core.load_proverbs()
    if not proverbs:
        st.info("No proverbs found.")
    else:
        selected = st.selectbox("Choose a proverb to vote for", [p['proverb'] for p in proverbs])
        if st.button("Vote"):
            vote.increment_vote(selected)
            st.success("Thanks for your vote!")

# --- Translate Proverb ---
elif page == "🌐 Translate":
    st.header("🌐 Translate a Proverb")
    input_text = st.text_input("Enter text to translate")
    target_lang = st.selectbox("Translate to", language.get_languages())
    if st.button("Translate"):
        if input_text.strip() and target_lang:
            translated = translate.mock_translate(input_text.strip(), target_lang)
            st.info(f"Translated '{input_text}' to [{target_lang}]: {translated}")
        else:
            st.warning("Please enter text and select language.")

# --- Record Audio ---
elif page == "🎤 Record Audio":
    st.header("🎤 Record a Proverb Audio")
    audio_bytes = st.file_uploader("Upload recorded proverb audio (MP3 or WAV)", type=["mp3", "wav"])
    if audio_bytes:
        audio.save_audio_file(audio_bytes)
        st.success("Audio uploaded and saved successfully!")
        st.audio(audio_bytes)

# Optional region stats
st.sidebar.markdown("---")
if st.sidebar.checkbox("📈 Show Region Stats"):
    st.sidebar.subheader("Region-wise Proverb Count")
    stats = core.get_stats()
    for region, count in stats.items():
        st.sidebar.write(f"{region}: {count}")
