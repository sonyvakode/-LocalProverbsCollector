import streamlit as st
import base64
import random
from utils import core, translate, vote, audio

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# --- Set Background ---
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
        .main-title {{
            font-size: 40px;
            text-align: center;
            padding: 15px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

set_background("Background.jpg")  # ✅ Case-sensitive!

# --- Title with Book Icon ---
st.markdown('<div class="main-title">📘 Indian Wisdom: Local Proverbs Collector</div>', unsafe_allow_html=True)

# --- Proverb of the Day ---
st.markdown("### 🌞 Proverb of the Day")
all_proverbs = vote.get_all()
if all_proverbs:
    random_proverb = random.choice(all_proverbs)
    st.info(f"_{random_proverb['proverb']}_")
else:
    st.warning("No proverbs available yet.")

st.markdown("---")

# --- Submit a Local Proverb ---
st.markdown("### ✍️ Submit a Local Proverb")
with st.form("submit_form"):
    proverb = st.text_area("Enter the proverb here")
    region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central", "Northeast"])
    audio_file = st.file_uploader("Optional: Upload audio", type=["wav", "mp3", "m4a"])
    submitted = st.form_submit_button("Submit")
    if submitted and proverb:
        core.save_proverb(proverb, region)
        st.success("✅ Proverb saved successfully!")
        if audio_file:
            transcription = audio.transcribe_audio(audio_file)
            if transcription:
                st.markdown(f"**Transcription:** _{transcription}_")
            else:
                st.warning("❌ Transcription failed.")

st.markdown("---")

# --- Translate Section ---
st.markdown("### 🌐 Translate a Proverb")
to_translate = st.text_input("Enter a proverb to translate")
target_lang = st.selectbox("Translate to", ["hi", "bn", "ta", "te", "gu", "ml", "mr", "kn"])
if st.button("Translate"):
    if to_translate:
        translated = translate.translate_proverb(to_translate, target_lang)
        st.success(f"**Translated Proverb:** {translated}")
    else:
        st.warning("Please enter a proverb.")

st.markdown("---")

# --- Stats Section ---
st.markdown("### 📊 Submission Stats")
try:
    stats = core.load_stats()
    total = stats.get("total_proverbs", 0)
    st.write(f"**Total Proverbs Submitted:** {total}")
except:
    st.warning("⚠️ Could not load stats.")
