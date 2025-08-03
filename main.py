import streamlit as st
import base64
from utils import core, translate, vote, audio

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Set background image
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        b64_img = base64.b64encode(img_file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{b64_img}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        .title-style {{
            font-size: 40px;
            text-align: center;
            padding: 10px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("Background.jpg")  # Correct casing!

# Title with book emoji
st.markdown('<div class="title-style">📘 Indian Wisdom: Local Proverbs Collector</div>', unsafe_allow_html=True)

st.markdown("### 📝 Submit a Local Proverb")
with st.form("submit_proverb_form"):
    proverb = st.text_area("Enter a local proverb")
    region = st.selectbox("Select region", ["North", "South", "East", "West", "Central", "Northeast"])
    audio_file = st.file_uploader("Upload audio of the proverb (optional)", type=["wav", "mp3", "m4a"])
    submitted = st.form_submit_button("Submit")
    if submitted and proverb:
        core.save_proverb(proverb, region)
        st.success("✅ Proverb saved successfully!")
        if audio_file:
            transcription = audio.transcribe_audio(audio_file)
            if transcription:
                st.markdown(f"**Transcription:** _{transcription}_")
            else:
                st.error("⚠️ Could not transcribe audio.")

st.markdown("---")

st.markdown("### 🌐 Translate a Proverb")
to_translate = st.text_input("Enter a proverb to translate")
target_lang = st.selectbox("Choose language", ["hi", "ta", "te", "bn", "ml", "gu", "mr", "kn"])
if st.button("Translate"):
    if to_translate:
        result = translate.translate_proverb(to_translate, target_lang)
        st.success(f"**Translated Proverb:** {result}")
    else:
        st.warning("Please enter a proverb to translate.")

st.markdown("---")

st.markdown("### 📊 Submission Stats")
try:
    stats = core.load_stats()
    st.write(f"**Total Proverbs Submitted:** {stats.get('total_proverbs', 0)}")
except Exception as e:
    st.error("Could not load stats.")
