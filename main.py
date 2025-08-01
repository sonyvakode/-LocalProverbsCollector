import streamlit as st
import random
import time
import os
import base64
import matplotlib.pyplot as plt
from utils import core, vote, translate, audio

# === Page Config ===
st.set_page_config(page_title="Indian Wisdom", layout="centered")
st.markdown("<h1 style='text-align:center; color: white;'>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)

# === Background ===
def set_background():
    img_url = "https://t4.ftcdn.net/jpg/08/04/67/63/360_F_804676330_hVxnVs6vGpu1uL6WmNL6qxSApym3zxUF.jpg"
    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("{img_url}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        color: white;
    }}
    </style>
    """, unsafe_allow_html=True)

set_background()

# === Load Proverbs File ===
os.makedirs("data", exist_ok=True)
if not os.path.exists("data/proverbs.txt"):
    with open("data/proverbs.txt", "w", encoding="utf-8") as f:
        pass

with open("data/proverbs.txt", "r", encoding="utf-8") as f:
    all_proverbs = [line.strip().split(" | ")[0] for line in f if line.strip()]

# === Proverb of the Day Section ===
st.subheader("🌟 Proverb of the Day")

if all_proverbs:
    current = random.choice(all_proverbs)
    st.markdown(f"<div style='font-size: 22px; background-color: rgba(0,0,0,0.5); padding: 15px; border-radius: 12px;'>{current}</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 5])
    with col1:
        if st.button("❤️", key=f"like_{current}"):
            vote.like_proverb(current)
    with col2:
        likes = vote.get_all().get(current, 0)
        st.caption(f"Likes: {likes}")
else:
    st.info("No proverbs saved yet.")

st.markdown("---")

# === Submit New Proverb ===
st.subheader("📝 Submit a Proverb")
with st.form("submit_form"):
    proverb = st.text_input("Enter a proverb")
    author = st.text_input("Your name or nickname")
    region = st.selectbox("Region", ["North", "South", "East", "West", "Central"])
    language = st.selectbox("Language", ["Hindi", "Tamil", "Telugu", "Kannada", "Bengali", "Other"])
    submitted = st.form_submit_button("Submit")
    if submitted and proverb:
        core.save_proverb(proverb, author, region, language)
        st.success("Thank you! Your proverb was saved.")

# === Audio Input ===
st.markdown("### 🎙️ Say a Proverb (Audio)")
uploaded_audio = st.file_uploader("Upload audio file (WAV/MP3)", type=["wav", "mp3"])
if uploaded_audio:
    transcription = audio.transcribe_audio(uploaded_audio)
    st.info(f"Transcribed Text: {transcription}")

# === Translate Section ===
st.subheader("🌐 Translate a Proverb")
proverb_to_translate = st.text_input("Enter proverb to translate")
target_lang = st.selectbox("Choose target language", ["Hindi", "Tamil", "Telugu", "Kannada", "Bengali"])
if st.button("Translate"):
    if proverb_to_translate:
        translated = translate.translate_proverb(proverb_to_translate, target_lang)
        st.success(f"Translation ({target_lang}): {translated}")
    else:
        st.warning("Please enter a proverb to translate.")

# === Stats Section ===
st.subheader("📊 Proverb Stats")
stats = core.load_stats()
if stats["languages"] or stats["regions"]:
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("**Languages**")
        plt.figure(figsize=(3,2))
        plt.bar(stats["languages"].keys(), stats["languages"].values(), color="orange")
        st.pyplot(plt)

    with col2:
        st.markdown("**Regions**")
        plt.figure(figsize=(3,2))
        plt.bar(stats["regions"].keys(), stats["regions"].values(), color="teal")
        st.pyplot(plt)
else:
    st.info("No stats yet. Submit a few proverbs to see insights.")
