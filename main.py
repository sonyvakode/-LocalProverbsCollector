import streamlit as st
import random
import time
import uuid

from utils.core import load_proverbs, save_proverb
from utils.language import get_languages
from utils.translate import translate_proverb
from utils.vote import vote_proverb

# ----------------------- SETUP -----------------------
st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Initialize session state
if "nickname" not in st.session_state:
    st.session_state.nickname = ""

if "liked_proverbs" not in st.session_state:
    st.session_state.liked_proverbs = set()

if "proverb_index" not in st.session_state:
    st.session_state.proverb_index = 0

if "last_update" not in st.session_state:
    st.session_state.last_update = time.time()

# Load proverbs
proverbs = load_proverbs()

# ------------------ HEADER / UI -----------------------
st.markdown(
    "<h1 style='text-align: center; color: white;'>🌟 Indian Wisdom 🌟</h1>",
    unsafe_allow_html=True,
)

nickname = st.text_input("Enter your nickname to start 👇", value=st.session_state.nickname)
st.session_state.nickname = nickname

st.markdown("---")

# ---------------- PROVERB OF THE DAY -------------------
def get_next_proverb():
    st.session_state.proverb_index = (st.session_state.proverb_index + 1) % len(proverbs)
    st.session_state.last_update = time.time()

# Refresh proverb every 20 seconds
if time.time() - st.session_state.last_update > 20:
    get_next_proverb()

if proverbs:
    proverb = proverbs[st.session_state.proverb_index]
    proverb_text = proverb.get("proverb", "No proverb")
    region = proverb.get("region", "Unknown")
    language = proverb.get("language", "Unknown")
    pid = proverb.get("id", str(uuid.uuid4()))

    st.markdown(
        f"""
        <div style="background-color: #222; padding: 20px; border-radius: 10px; margin-bottom: 10px;">
            <h3 style="color: #ffcc00;">📜 Proverb of the Day</h3>
            <p style="font-size: 20px; color: white;">"{proverb_text}"</p>
            <p style="font-size: 16px; color: #aaa;">🗺️ {region} | 🈯 {language}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # ❤️ Like Button
    liked = pid in st.session_state.liked_proverbs
    if st.button(f"{'❤️ Liked' if liked else '🤍 Like'}"):
        if not liked:
            vote_proverb(pid)
            st.session_state.liked_proverbs.add(pid)

else:
    st.warning("No proverbs available.")

# ---------------- SUBMIT A PROVERB --------------------
with st.expander("➕ Submit Your Proverb"):
    proverb_text = st.text_input("Enter Proverb")
    region = st.text_input("Enter Region (e.g., Tamil Nadu, Bengal, Punjab)", placeholder="e.g., Kerala, Odisha")
    language = st.selectbox("Select Language", get_languages())

    if st.button("Submit Proverb"):
        if proverb_text and region:
            new_proverb = {
                "id": str(uuid.uuid4()),
                "proverb": proverb_text,
                "region": region,
                "language": language,
                "likes": 0,
                "views": 0
            }
            save_proverb(new_proverb)
            st.success("Proverb submitted successfully!")
        else:
            st.error("Please fill in all fields.")

# ---------------- STATS / REGION WISE ------------------
with st.expander("📊 View Region Stats"):
    region_names = sorted(set(p.get("region", "Unknown") for p in proverbs))
    selected_region = st.selectbox("Choose a Region", region_names)

    regional_data = [p for p in proverbs if p.get("region") == selected_region]

    st.write(f"**Total Proverbs from {selected_region}:** {len(regional_data)}")

    if regional_data:
        st.bar_chart(
            data={p["language"]: p["likes"] for p in regional_data if "language" in p},
            use_container_width=True
        )

# ---------------- STYLE / BACKGROUND -------------------
st.markdown(
    """
    <style>
    body {
        background-color: #111;
    }
    .stApp {
        background-image: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True
)
