import streamlit as st
import random
import time

from utils import core, translate, vote, language

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Load data
proverbs = core.load_proverbs()
languages = language.get_languages()

# Store likes in session
if "likes" not in st.session_state:
    st.session_state.likes = {}

# Auto-refresh every 10 seconds for proverb rotation
def auto_refresh(interval_sec=10):
    time.sleep(interval_sec)
    st.experimental_rerun()

# Set title and subtitle
st.markdown("<h1 style='text-align:center;'>🧠 Indian Wisdom</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>Collect, Translate & Vote on Local Proverbs!</p>", unsafe_allow_html=True)

# ShabdKhoj-like nickname input
nickname = st.text_input("👤 Enter your nickname to start:")
if not nickname:
    st.warning("Please enter a nickname to proceed.")
    st.stop()

# Region selection
region = st.selectbox("🌍 Select your region", ["Andhra Pradesh", "Bihar", "Gujarat", "Karnataka", "Kerala", "Punjab", "Rajasthan", "Tamil Nadu", "Telangana", "Uttar Pradesh"])

st.markdown("---")

# ---------- Proverb of the Day ----------
st.subheader("📜 Proverb of the Day")

# Rotate proverb
random.seed(int(time.time() / 10))  # changes every ~10 sec
if proverbs:
    proverb_item = random.choice(proverbs)
    proverb_text = proverb_item["proverb"]
    proverb_lang = proverb_item["language"]

    st.markdown(f"**🗣️ {proverb_lang}**")
    st.markdown(f"👉 _{proverb_text}_")

    # Like button
    key = f"{proverb_text}_{proverb_lang}"
    liked = st.session_state.likes.get(key, False)
    if st.button("❤️ Like" if not liked else "💔 Unlike", key=key):
        st.session_state.likes[key] = not liked

    st.caption(f"👍 Likes: {1 if liked else 0}")
else:
    st.info("No proverbs available.")

st.markdown("---")

# ---------- Submit a Proverb ----------
st.subheader("➕ Submit a New Proverb")
new_proverb = st.text_area("Enter a proverb")
new_lang = st.selectbox("Select language", languages)
if st.button("Submit Proverb"):
    if new_proverb:
        core.save_proverb(new_proverb.strip(), new_lang)
        st.success("Proverb submitted successfully!")
    else:
        st.error("Proverb cannot be empty.")

# ---------- Translate a Proverb ----------
st.subheader("🌐 Translate a Proverb")
proverb_to_translate = st.text_input("Enter proverb to translate")
target_lang = st.selectbox("Translate to", languages)
if st.button("Translate"):
    if proverb_to_translate:
        translated = translate.translate_proverb(proverb_to_translate, target_lang)
        st.success(f"Translated: {translated}")
    else:
        st.warning("Please enter a proverb.")

# ---------- Voting Section ----------
st.subheader("📊 Vote on Proverbs")
if proverbs:
    selected_proverb = st.selectbox("Choose a proverb to vote on", [f"{p['proverb']} ({p['language']})" for p in proverbs])
    if st.button("Vote"):
        proverb_text = selected_proverb.split(" (")[0]
        vote.vote_proverb(proverb_text)
        st.success("Thanks for voting!")

# ---------- Stats Section ----------
st.subheader("📈 Stats")

stats = core.load_stats()
if stats:
    st.bar_chart(stats)
else:
    st.info("No voting data yet.")
