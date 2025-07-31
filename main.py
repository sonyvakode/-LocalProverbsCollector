import streamlit as st
from utils import core, vote, translate, language, audio

st.set_page_config(page_title="Indian Wisdom", layout="centered")

st.title("🪔 Indian Wisdom: Local Proverbs Collector")

menu = ["Contribute", "Vote", "Stats"]
choice = st.sidebar.radio("Go to", menu)

if choice == "Contribute":
    st.subheader("Share a Local Proverb")

    region = st.selectbox("Select your region", language.regions())
    proverb = st.text_area("Enter the proverb in your language")

    audio_file = st.file_uploader("Upload audio (optional)", type=["mp3", "wav"])

    if st.button("Submit"):
        if proverb.strip() == "":
            st.warning("Please enter a proverb.")
        else:
            core.save_proverb(proverb, region, audio_file)
            st.success("✅ Proverb submitted!")

elif choice == "Vote":
    st.subheader("Vote on Proverbs")

    data = core.load_proverbs()
    if not data:
        st.info("No proverbs available yet.")
    else:
        for idx, entry in enumerate(data):
            st.markdown(f"**{entry['proverb']}**  _(Region: {entry['region']})_")
            if "audio" in entry:
                st.audio(entry["audio"])
            col1, col2 = st.columns([1, 5])
            with col1:
                if st.button("👍", key=f"up_{idx}"):
                    vote.cast_vote(idx, upvote=True)
            with col2:
                st.write(f"Votes: {entry.get('votes', 0)}")

elif choice == "Stats":
    st.subheader("📊 Contribution Stats")
    stats = core.get_stats()
    if not stats:
        st.info("No data available.")
    else:
        for region, count in stats.items():
            st.write(f"**{region}**: {count} proverb(s)")
