import streamlit as st
import random
from utils import core, translate, vote, audio
from utils.language import LANGUAGE_NAMES_TO_CODES

# App Config
st.set_page_config(page_title="Indian Wisdom", layout="centered")
st.markdown("<h1 style='text-align: center;'>📜 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)

# Load proverbs
all_proverbs = core.load_proverbs()
selected_proverb = random.choice(all_proverbs) if all_proverbs else ""

# --- Navigation ---
nav = st.sidebar.radio("📌 Navigate", ["Proverb of the Day", "Submit Proverb", "Translate", "Leaderboard", "Stats"])

# --- Proverb of the Day ---
if nav == "Proverb of the Day":
    st.subheader("📝 Proverb of the day")
    if selected_proverb:
        parts = selected_proverb.split("|")
        if len(parts) >= 4:
            original = parts[0]
            region = parts[1]
            language = parts[2]
            views = parts[3]
            st.markdown(f"**Original:** {original}")
            st.markdown(f"🌍 *Region:* {region}  |  🗣️ *Language:* {language}")

            # Translate
            display_lang = "English"
            lang_code = LANGUAGE_NAMES_TO_CODES.get(display_lang.lower(), "en")

            try:
                translated = translate.translate_text(original, lang_code)
            except Exception as e:
                translated = f"Translation failed: {e}"

            st.markdown(f"**Translated:** {translated}")
        else:
            st.warning("Invalid proverb format.")
    else:
        st.info("No proverbs available yet.")

# --- Submit Proverb ---
elif nav == "Submit Proverb":
    st.subheader("📬 Submit a New Proverb")

    with st.form("submit_form"):
        proverb = st.text_area("Enter the Proverb")
        region = st.text_input("Region")
        language = st.selectbox("Language", list(LANGUAGE_NAMES_TO_CODES.keys()))
        audio_file = st.file_uploader("🎤 Or upload an audio file", type=["wav", "mp3", "m4a"])
        submitted = st.form_submit_button("Submit")

        if submitted:
            if audio_file:
                proverb = audio.transcribe_audio(audio_file)
                st.success(f"Transcribed: {proverb}")

            if proverb and region and language:
                core.save_proverb(proverb, region, language)
                st.success("✅ Proverb submitted successfully!")
            else:
                st.warning("Please complete all fields.")

# --- Translate Section ---
elif nav == "Translate":
    st.subheader("🌐 Translate a Proverb")
    text = st.text_input("Enter proverb to translate")
    display_lang = st.selectbox("Translate to", list(LANGUAGE_NAMES_TO_CODES.keys()))
    lang_code = LANGUAGE_NAMES_TO_CODES.get(display_lang.lower(), "en")

    if st.button("Translate"):
        try:
            result = translate.translate_text(text, lang_code)
            st.markdown(f"**Translated:** {result}")
        except Exception as e:
            st.error(f"Translation failed: {e}")

# --- Leaderboard ---
elif nav == "Leaderboard":
    st.subheader("🏆 Top Proverbs by Views")
    all_sorted = sorted(all_proverbs, key=lambda x: int(x.split("|")[3]) if len(x.split("|")) > 3 else 0, reverse=True)
    for i, line in enumerate(all_sorted[:10], 1):
        parts = line.split("|")
        if len(parts) >= 4:
            st.markdown(f"**{i}. {parts[0]}**  \n🌍 {parts[1]} | 🗣️ {parts[2]} | 👁️ {parts[3]} views")

# --- Stats ---
elif nav == "Stats":
    st.subheader("📊 Stats")
    try:
        stats = core.load_stats()
        total = stats.get("total_proverbs", 0)
        st.metric("Total Proverbs Collected", total)
    except Exception as e:
        st.error(f"Failed to load stats: {e}")
