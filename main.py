import streamlit as st
from utils import core, vote, language, translate, audio

st.set_page_config(page_title="Indian Wisdom: Local Proverbs Collector", layout="centered")

st.title("🪔 Indian Wisdom: Local Proverbs Collector")

menu = st.sidebar.radio("Navigate", ["Submit", "Vote", "Stats"])

if menu == "Submit":
    st.subheader("📜 Share a Proverb")
    proverb = st.text_area("Enter a local proverb")
    region = st.selectbox("Select the region/language", language.get_supported_languages())
    audio_file = st.file_uploader("Upload audio (optional)", type=["wav", "mp3", "m4a"])

    if st.button("Submit"):
        if proverb.strip() == "":
            st.warning("Please enter a proverb.")
        else:
            core.save_proverb(proverb, region)
            if audio_file:
                audio.save_audio_file(audio_file, proverb)
            st.success("Thank you! Proverb submitted.")

elif menu == "Vote":
    st.subheader("👍 Vote for Proverbs")
    proverbs = core.load_proverbs()
    if not proverbs:
        st.info("No proverbs found.")
    else:
        vote.render_voting_ui(proverbs)

elif menu == "Stats":
    st.subheader("📊 Statistics")
    stats = core.get_stats()
    if not stats:
        st.info("No data to show.")
    else:
        st.bar_chart(stats)

st.markdown("---")
st.caption("An open-source project powered by viswam.ai 🧠")
