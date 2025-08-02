import streamlit as st
import random
from utils import core, translate, vote, audio

st.set_page_config(page_title="Indian Wisdom: Local Proverbs Collector", layout="centered")

# Background style
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url('https://cdn.pixabay.com/photo/2021/01/04/11/43/paper-5887765_1280.jpg');
    background-size: cover;
    background-position: top center;
    background-repeat: no-repeat;
    background-attachment: fixed;
    color: #000000;
}
h1, h2, h3, .stTextInput label, .stSelectbox label, .stTextArea label {
    color: #222222 !important;
}
.st-bf, .st-ag, .st-cq {
    background-color: rgba(255, 255, 255, 0.9) !important;
    border-radius: 12px;
    padding: 1rem;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

st.markdown("## 📜 *Indian Wisdom*")
st.markdown("#### Discover, submit, and celebrate the timeless wisdom of Indian proverbs.\n---")

# PROVERB OF THE DAY
st.subheader("🌟 Proverb of the Day")

def rotate_proverb():
    proverbs = vote.get_all()
    if not proverbs:
        return {"text": "No proverbs yet.", "language": "N/A", "region": "N/A", "likes": 0, "views": 0, "saves": 0}
    proverb = random.choice(proverbs)
    proverb["views"] += 1
    core.save_proverb(proverbs)
    return proverb

proverb = rotate_proverb()
st.markdown(f"**🗣️ Proverb:** {proverb['text']}")
st.markdown(f"🌍 Language: {proverb['language']} | 📍 Region: {proverb['region']}")
st.markdown(f"❤️ Likes: {proverb['likes']} | 👁️ Views: {proverb['views']} | 💾 Saves: {proverb['saves']}")

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("❤️ Like"):
        vote.like_proverb(proverb['text'])
with col2:
    if st.button("💾 Save"):
        proverb['saves'] += 1
        core.save_proverb(vote.get_all())
with col3:
    st.button("🔄 Refresh")

st.divider()

# SUBMIT A PROVERB
st.subheader("✍️ Submit a Proverb")

with st.form("submit_form"):
    text = st.text_area("Enter the proverb", max_chars=200)
    language = st.selectbox("Language", ["Hindi", "Marathi", "Tamil", "Bengali", "Telugu", "Gujarati"])
    region = st.selectbox("Region", ["North", "South", "East", "West", "Central", "Northeast"])
    audio_file = st.file_uploader("Optional: Upload audio", type=["mp3", "wav", "ogg"])
    submit = st.form_submit_button("Submit")

    if submit:
        if audio_file:
            text = audio.transcribe_audio(audio_file) or text
        if text:
            core.save_proverb([{
                "text": text,
                "language": language,
                "region": region,
                "likes": 0,
                "views": 0,
                "saves": 0
            }], append=True)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.error("Please enter or upload a proverb.")

st.divider()

# TRANSLATE SECTION
st.subheader("🌐 Translate a Proverb")
with st.form("translate_form"):
    input_text = st.text_input("Enter proverb to translate")
    target_lang = st.selectbox("Translate to", ["en", "hi", "ta", "bn", "mr", "te", "gu"])
    do_translate = st.form_submit_button("Translate")
    if do_translate and input_text:
        translated = translate.translate_proverb(input_text, target_lang)
        st.success(f"🈯 Translated: {translated}")

st.divider()

# STATISTICS
st.subheader("📊 Statistics")

try:
    stats = core.load_stats()
    st.bar_chart(stats)
except Exception as e:
    st.error(f"Could not load stats: {e}")
