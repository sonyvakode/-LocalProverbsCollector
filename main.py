import streamlit as st
from utils import core, vote, translate

st.set_page_config(page_title="Indian Wisdom", layout="centered")
st.title("🪔 Indian Wisdom: Local Proverbs Collector")

st.markdown("Contribute and explore timeless Indian proverbs across regions and languages.")

# Input form
with st.form("proverb_form", clear_on_submit=True):
    proverb = st.text_area("Enter a local proverb in any Indian language:")
    region = st.text_input("Enter the region or state (e.g., Tamil Nadu, Assam):")
    submitted = st.form_submit_button("Submit")

    if submitted:
        if proverb.strip() and region.strip():
            core.save_proverb(proverb.strip(), region.strip())
            st.success("✅ Proverb saved successfully!")
        else:
            st.error("⚠️ Please enter both a proverb and a region.")

# Show stats
with st.expander("📊 View Contribution Stats"):
    stats = core.get_stats()
    if stats:
        st.write("Proverbs by Region:")
        st.json(stats)
    else:
        st.info("No proverbs yet.")

# Translation
with st.expander("🌐 Translate a Proverb (mock)"):
    input_text = st.text_input("Proverb to translate:")
    target_lang = st.text_input("Target language (e.g., en, hi):", value="en")
    if st.button("Translate"):
        if input_text.strip():
            result = translate.translate_text(input_text, target_lang)
            st.success(result)
        else:
            st.warning("Enter some text to translate.")

# Voting
with st.expander("🗳️ Vote on Proverbs"):
    proverbs = vote.load_proverbs()
    for i, p in enumerate(proverbs):
        st.markdown(f"**{p['proverb']}** (_{p['region']}_) — 👍 {p.get('votes', 0)} votes")
        if st.button(f"Vote for #{i+1}"):
            vote.vote_proverb(i)
            st.experimental_rerun()

# Audio Upload
with st.expander("🎤 Upload Audio of a Proverb"):
    uploaded_file = st.file_uploader("Upload audio file", type=["mp3", "wav"])
    if uploaded_file:
        save_path = core.save_audio_file(uploaded_file)
        st.success(f"Audio saved to `{save_path}`.")
