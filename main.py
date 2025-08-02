import streamlit as st
import random
from utils import core, translate, vote, audio
from PIL import Image
import base64

st.set_page_config(layout="centered", page_title="Indian Wisdom")

# Load background
def set_background(image_path):
    with open(image_path, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{data}");
        background-size: cover;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("utils/bg.png")  # use your uploaded background image

def show_proverb_of_the_day():
    all_proverbs = vote.get_all()
    if not all_proverbs:
        st.warning("No proverbs available.")
        return

    proverb = random.choice(all_proverbs)
    proverb['views'] += 1
    st.markdown("## 🌟 Proverb of the Day")
    st.markdown(f"**🗣️ Proverb:** {proverb['text']}")
    st.markdown(f"**🌐 Language:** {proverb['language']} | 📍 Region: {proverb['region']}")
    st.markdown(f"👁️ Views: {proverb['views']} | ❤️ Likes: {proverb['likes']}")
    
    if st.button("❤️ Like", key=proverb['text']):
        vote.like_proverb(proverb['text'])

def main():
    st.markdown("<h1 style='text-align: center;'>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)

    show_proverb_of_the_day()
    st.markdown("---")

    # New Submission
    st.subheader("➕ Submit a New Proverb")
    new_proverb = st.text_input("Enter a proverb")
    region = st.selectbox("Select region", ["Kerala", "Maharashtra", "Punjab", "Tamil Nadu", "Assam"])
    language = st.selectbox("Language", ["Hindi", "English", "Tamil", "Malayalam", "Punjabi"])

    if st.button("Submit"):
        if new_proverb:
            core.save_proverb(new_proverb, language, region)
            st.success("Proverb submitted successfully!")
        else:
            st.warning("Please enter a proverb.")

    # Translate
    st.markdown("---")
    st.subheader("🌐 Translate a Proverb")
    input_text = st.text_input("Enter proverb to translate")
    target_lang = st.selectbox("Translate to", ["hi", "en", "ta", "ml", "pa"])
    if st.button("Translate"):
        if input_text:
            translated = translate.translate_text(input_text, target_lang)
            st.success(f"Translated: {translated}")
        else:
            st.warning("Enter text first.")

    # Audio Upload
    st.markdown("---")
    st.subheader("🎤 Upload Audio for Proverb")
    audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
    if audio_file:
        transcription = audio.transcribe_audio(audio_file)
        st.info(f"📝 Transcription: {transcription}")

    # Stats
    st.markdown("---")
    st.subheader("📊 Proverbs Statistics")
    stats = core.load_stats()
    if stats:
        for lang, count in stats.items():
            st.write(f"🔤 {lang}: {count} proverbs")
    else:
        st.info("No stats yet.")

if __name__ == "__main__":
    main()
