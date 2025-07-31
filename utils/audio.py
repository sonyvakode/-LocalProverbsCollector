# utils/audio.py
import streamlit as st

def record_audio_ui(proverbs):
    if not proverbs:
        st.warning("No proverbs available to record.")
        return

    selected = st.selectbox("Select a proverb to record", [p["proverb"] for p in proverbs])
    audio_file = st.file_uploader("Upload audio recording for the proverb", type=["mp3", "wav"])

    if st.button("Submit Recording"):
        if audio_file:
            st.success(f"Audio for '{selected}' uploaded successfully! (Mock)")
        else:
            st.error("Please upload a valid audio file.")
