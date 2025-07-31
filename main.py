import streamlit as st
from utils import core, vote, audio, language, translate

st.set_page_config(page_title="Indian Wisdom: Local Proverbs Collector", layout="centered")

st.title("🪔 Indian Wisdom: Local Proverbs Collector")
st.markdown("Help preserve regional culture by submitting proverbs in your language.")

with st.form("proverb_form"):
    proverb = st.text_area("Enter a local proverb")
    region = st.selectbox("Select your region", ["Andhra Pradesh", "Tamil Nadu", "Kerala", "Karnataka", "Maharashtra", "Other"])
    audio_file = st.file_uploader("Upload an audio recording (optional)", type=["mp3", "wav", "m4a"])
    submitted = st.form_submit_button("Submit")

    if submitted and proverb:
        core.save_proverb(proverb, region)
        if audio_file:
            audio.save_audio(audio_file, proverb)
        st.success("Thank you! Your proverb has been submitted.")

st.markdown("### 📊 Proverbs by Region")
stats = core.get_stats()
st.bar_chart(stats)

st.markdown("### 🗳️ Vote for a Proverb")
proverbs = core.load_proverbs()
selected = st.selectbox("Choose a proverb to vote for", [p["proverb"] for p in proverbs] or ["No proverbs available"])
if st.button("Vote"):
    vote.vote_proverb(selected)
    st.success("Thanks for your vote!")

st.markdown("### 🌐 Translate a Proverb")
to_translate = st.text_input("Enter text to translate")
lang = st.selectbox("Translate to", language.get_languages())
if st.button("Translate"):
    translated = translate.translate_text(to_translate, lang)
    st.info(translated)
