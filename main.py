import streamlit as st
import random
import base64
from utils import core, translate, vote, audio
from utils.language import LANGUAGES

# ================== BACKGROUND SETUP ==================
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)), 
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        textarea, input, select {{
            background-color: white !important;
            color: black !important;
            border: 1px solid #ccc !important;
            border-radius: 5px !important;
        }}
        label, .stSelectbox > div, .stTextInput > div, .stTextArea > div {{
            color: #111 !important;
            font-weight: 500 !important;
        }}
        .solid-box {{
            background-color: #ffffffcc;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
        .center {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("background.jpg")

# ================== TITLE ==================
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)
st.markdown("<p style='text-align: center;'>Share the timeless wisdom from your region and explore others.</p>", unsafe_allow_html=True)

# ================== NAVIGATION ==================
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "Stats"])

# ========== HOME ==========
if page == "Home":
    st.markdown("### Submit Your Local Proverb")
    with st.container():
        st.markdown('<div class="solid-box">', unsafe_allow_html=True)

        proverb = st.text_area("Enter your local proverb")
        city = st.text_input("City or Region")
        language = st.selectbox("Select Language", list(LANGUAGES.keys()))
        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])

        if st.button("Submit"):
            if proverb.strip() == "":
                st.warning("Please enter a proverb.")
            elif city.strip() == "":
                st.warning("Please enter a city or region.")
            else:
                core.save_proverb(proverb, city, language)  # ✅ FIXED: now passing 3 args
                st.success("Proverb submitted successfully!")

        if audio_file is not None:
            st.markdown("Transcribing audio...")
            text = audio.transcribe_audio(audio_file)
            st.text_area("Transcribed Text", value=text, height=100)

        st.markdown('</div>', unsafe_allow_html=True)

# ========== PROVERB OF THE DAY ==========
elif page == "Proverb of the day":
    st.markdown("### 🌟 Proverb of the Day")
    proverbs = core.get_all_proverbs()
    if proverbs:
        selected = random.choice(proverbs)
        st.markdown('<div class="solid-box center">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align:center;'>{selected}</h3>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Next Proverb"):
            st.experimental_rerun()
    else:
        st.info("No proverbs available yet.")

# ========== STATS ==========
elif page == "Stats":
    st.subheader("📊 Submission Stats")
    stats = core.load_stats()
    total = stats.get("total_submitted", 0)
    st.info(f"📈 Total Proverbs Submitted: **{total}**")

    region_filter = st.selectbox("Filter by Region (Optional)", [
        "All", "Delhi", "Mumbai", "Chennai", "Kolkata", "Bengaluru",
        "Hyderabad", "Lucknow", "Jaipur", "Ahmedabad", "Patna"
    ])

    region_counts = stats.get("regions", {})
    if region_filter != "All":
        count = region_counts.get(region_filter, 0)
        st.success(f"📍 Proverbs from **{region_filter}**: **{count}**")
    else:
        st.markdown("### 🏆 Leaderboard by Region")
        sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)
        for region, count in sorted_regions:
            st.markdown(f"- **{region}**: {count} proverbs")
