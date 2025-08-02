import streamlit as st
import random
import time
import base64
from utils import core, translate, vote, audio

# Set background image
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{data}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: white;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Show rotating proverbs
def show_proverb_of_the_day():
    all_proverbs = core.load_proverbs()
    if not all_proverbs:
        st.info("No proverbs available.")
        return

    selected = random.choice(all_proverbs)
    st.markdown("### 🌟 Proverb of the Day")
    st.markdown(f"**📝 {selected['text']}**")
    st.markdown(f"🌍 Region: {selected.get('region', 'Unknown')}")
    st.markdown(f"❤️ {selected.get('likes', 0)}  🔁 {selected.get('views', 0)}  💾 {selected.get('saves', 0)}")

    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("❤️ Like"):
            vote.like_proverb(selected['text'])
    with col2:
        if st.button("💾 Save"):
            vote.save_proverb(selected['text'])
    with col3:
        if st.button("🌐 Translate"):
            lang = st.selectbox("Select Language", ["hi", "ta", "te", "ml", "gu", "kn", "bn", "ur"])
            translated = translate.translate_proverb(selected['text'], lang)
            st.success(f"🔤 Translated: {translated}")

# App layout
def main():
    st.set_page_config(page_title="Indian Wisdom", layout="centered")
    set_background("background.jpg")

    st.title("📜 Indian Wisdom: Local Proverbs Collector")

    menu = ["Submit Proverb", "Proverb of the Day", "Upload Audio", "Stats"]
    choice = st.sidebar.radio("Menu", menu)

    if choice == "Submit Proverb":
        st.subheader("📝 Submit a Local Proverb")
        proverb = st.text_area("Enter proverb")
        region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central"])
        if st.button("Submit"):
            core.save_proverb(proverb, region)
            st.success("✅ Proverb saved!")

    elif choice == "Proverb of the Day":
        show_proverb_of_the_day()

    elif choice == "Upload Audio":
        st.subheader("🎤 Upload an Audio File")
        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
        if audio_file is not None:
            text = audio.transcribe_audio(audio_file)
            st.success(f"🗣️ Transcribed Text: {text}")

    elif choice == "Stats":
        stats = core.load_stats()
        if not stats:
            st.info("No data to display.")
        else:
            st.subheader("📊 Proverbs Stats by Region")
            st.bar_chart(stats)

if __name__ == "__main__":
    main()
