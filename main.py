import streamlit as st
import random
import time
from utils.audio import transcribe_audio
from utils.translate import translate_proverb
from utils.vote import vote_proverb, get_votes
from utils.core import load_proverbs, save_proverb, load_stats

# App Config
st.set_page_config(page_title="Indian Wisdom Collector", layout="centered")
st.markdown("<h1 style='text-align: center;'>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)

# --- Proverb Data ---
proverbs = load_proverbs()

# Sample rotating proverbs
sample_proverbs = [
    {"proverb": "अति सर्वत्र वर्जयेत्", "lang": "Sanskrit"},
    {"proverb": "Too much of anything is bad", "lang": "English"},
    {"proverb": "अतिसयलूणं चव नाही", "lang": "Marathi"},
    {"proverb": "அதிகமும் நஞ்சாகும்", "lang": "Tamil"},
    {"proverb": "ತುಂಬಿದ ಪಾತ್ರೆಯು ಕೂಡ ಹರಿದುಹೋಗುತ್ತದೆ", "lang": "Kannada"},
    {"proverb": "చిక్కిన మొండి గూటిలో పడి పోతుంది", "lang": "Telugu"}
]

# --- Proverb of the Day Section ---
if "current_index" not in st.session_state:
    st.session_state.current_index = 0

def rotate_proverb():
    st.session_state.current_index = (st.session_state.current_index + 1) % len(sample_proverbs)

# Rotate every 30 seconds
if time.time() % 30 < 1:
    rotate_proverb()

proverb_item = sample_proverbs[st.session_state.current_index]
proverb_text = proverb_item["proverb"]
language = proverb_item["lang"]

st.markdown("### 🌞 Proverb of the Day")
st.markdown(f"**🗣 Language:** {language}")
st.markdown(f"📜 _{proverb_text}_")

if st.button("❤️ Like"):
    vote_proverb(proverb_text)
    st.success("Thanks for your love!")

likes = get_votes(proverb_text)
st.markdown(f"👍 Total Likes: {likes}")

# --- Region Selection ---
region = st.selectbox("🌍 Select your region", ["Andhra Pradesh", "Maharashtra", "Punjab", "Tamil Nadu", "Karnataka", "Uttar Pradesh", "West Bengal"])

# --- Submit New Proverb ---
st.markdown("## ✍️ Submit a Local Proverb")
with st.form("submit_form"):
    proverb = st.text_input("Enter your proverb")
    meaning = st.text_input("Enter its meaning")
    language = st.text_input("Language")
    submitted = st.form_submit_button("Submit")
    if submitted and proverb and meaning and language:
        save_proverb(proverb, meaning, language)
        st.success("Proverb submitted successfully!")

# --- Translate Section ---
st.markdown("## 🌐 Translate a Proverb")
with st.form("translate_form"):
    proverb_to_translate = st.text_input("Enter proverb to translate")
    target_lang = st.text_input("Translate to (e.g., Hindi)")
    translate_btn = st.form_submit_button("Translate")
    if translate_btn and proverb_to_translate and target_lang:
        translated = translate_proverb(proverb_to_translate, target_lang)
        st.success(f"🔄 Translated: {translated}")

# --- Audio Upload Section ---
st.markdown("## 🎙️ Upload Audio")
audio_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
if audio_file:
    text = transcribe_audio(audio_file)
    st.markdown("### 📝 Transcribed Text")
    st.write(text)

# --- Stats Section ---
st.markdown("## 📊 Proverb Stats")
try:
    stats = load_stats()
    if stats:
        sorted_stats = sorted(stats.items(), key=lambda x: x[1]["likes"], reverse=True)
        top = sorted_stats[:5]

        st.markdown("### 🔝 Top Proverbs by Likes")
        for p, data in top:
            st.write(f"**{p}** - 👍 {data['likes']} | 👀 {data.get('views', 0)}")

        # Bar chart
        import pandas as pd
        chart_data = pd.DataFrame({
            "Proverb": [p for p, d in top],
            "Likes": [d["likes"] for p, d in top],
            "Views": [d.get("views", 0) for p, d in top]
        })
        st.bar_chart(chart_data.set_index("Proverb"))

except Exception as e:
    st.warning("📉 No stats available or error loading stats.")
