import streamlit as st
from utils import core, vote, audio, translate

st.set_page_config(page_title="Indian Wisdom: Local Proverbs", layout="centered")

st.title("📚 Indian Wisdom: Local Proverbs Collector")

# Collapsible slide-like section using expander
with st.expander("➕ Submit a Proverb"):
    st.subheader("📝 Add a New Proverb")
    proverb = st.text_input("Enter a local proverb")
    region = st.text_input("Enter the region/language of this proverb")

    if st.button("Submit"):
        if proverb and region:
            core.save_proverb(proverb, region)
            st.success("Proverb saved successfully!")
        else:
            st.warning("Please enter both proverb and region.")

with st.expander("📊 Vote for a Proverb"):
    st.subheader("🗳️ Vote for a Proverb")
    proverbs = [p["proverb"] for p in core.load_proverbs()]
    selected = st.selectbox("Choose a proverb to vote for", proverbs)

    if st.button("Vote"):
        vote.vote_for_proverb(selected)
        st.success("Thank you for voting!")

with st.expander("🌐 Translate a Proverb"):
    st.subheader("🌍 Translate a Proverb")
    text = st.text_input("Enter text to translate")
    target_lang = st.selectbox("Translate to", ["Hindi", "Telugu", "Tamil", "Kannada", "Bengali", "English"])

    if st.button("Translate"):
        if text:
            result = translate.mock_translate(text, target_lang)
            st.info(f"Translated '{text}' to [{target_lang}]: {result}")
        else:
            st.warning("Please enter text to translate.")

with st.expander("📈 View Statistics"):
    st.subheader("📊 Proverbs per Region")
    stats = core.get_stats()
    for region, count in stats.items():
        st.write(f"**{region}**: {count} proverb(s)")

with st.expander("🎙️ Record Audio (Optional)"):
    st.subheader("🎧 Record Your Proverb")
    st.write("Upload an audio file of the proverb (WAV/MP3 format).")
    uploaded = st.file_uploader("Upload Audio", type=["wav", "mp3"])
    if uploaded:
        audio.save_audio_file(uploaded)
        st.success("Audio uploaded successfully!")
