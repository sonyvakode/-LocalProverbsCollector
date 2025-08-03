import streamlit as st
import random
from utils import core, translate, vote, audio
from utils.language import get_all_languages

st.set_page_config(page_title="Indian Wisdom", layout="centered")

# ========== Background Setup ==========
def set_background():
    with open("background.jpg", "rb") as img_file:
        img_base64 = img_file.read().encode("base64").decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{img_base64}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

set_background()

# ========== App Title ==========
st.markdown("""
    <div style='text-align:center; margin-top: 20px;'>
        <h1 style='font-size: 36px;'>📜 Indian Wisdom: Local Proverbs Collector</h1>
    </div>
""", unsafe_allow_html=True)

# ========== Sidebar Navigation ==========
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "Stats"])

# ========== Home Page ==========
if page == "Home":
    st.markdown("### ✍️ Submit a Local Proverb")

    with st.form("submit_form"):
        proverb = st.text_input("Enter your local proverb", "")
        city = st.text_input("City or Region", "")
        lang = st.selectbox("Select Language", get_all_languages())
        audio_file = st.file_uploader("Upload Audio (optional)", type=["wav", "mp3", "m4a"])

        submitted = st.form_submit_button("Submit Proverb")

        if submitted and proverb and city and lang:
            core.save_proverb(proverb, city, lang)
            if audio_file:
                audio_text = audio.transcribe_audio(audio_file)
                if audio_text:
                    st.success(f"Transcribed Audio: {audio_text}")
            st.success("✅ Proverb submitted successfully!")
        elif submitted:
            st.warning("⚠️ Please fill in all fields before submitting.")

    # ========== Translation Section ==========
    st.markdown("---")
    st.markdown("### 🌐 Translate a Proverb")
    user_input = st.text_input("Enter proverb to translate")
    selected_lang = st.selectbox("Translate to", get_all_languages())

    if st.button("Translate"):
        if user_input and selected_lang:
            translated_text = translate.translate_text(user_input, selected_lang)
            st.success(f"🔤 Translated: {translated_text}")
        else:
            st.warning("Please enter a proverb and select language.")

# ========== Proverb of the Day Page ==========
elif page == "Proverb of the day":
    st.subheader("📝 Proverb of the day")

    try:
        with open("data/proverbs.txt", "r", encoding="utf-8") as f:
            all_proverbs = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        all_proverbs = []

    if all_proverbs:
        selected_proverb = random.choice(all_proverbs)
        display_lang = "English"
        translated = translate.translate_text(selected_proverb, display_lang)

        st.markdown(f"""
            <div style='
                background-color: #ffffff;
                padding: 24px;
                border-radius: 10px;
                margin: 30px auto 20px;
                font-size: 18px;
                color: #222;
                width: 90%;
                max-width: 700px;
                text-align: center;
                box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            '>
                <div><strong>Original:</strong> {selected_proverb}</div>
                <div style='margin-top: 12px;'><strong>Translated:</strong> {translated}</div>
            </div>
        """, unsafe_allow_html=True)
    else:
        st.warning("No proverbs available in the file yet.")

    st.markdown("<div style='margin-top: 25px; text-align: center;'>", unsafe_allow_html=True)
    if st.button("🔄 Next Proverb"):
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ========== Stats Page ==========
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
