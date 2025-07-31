import streamlit as st
from utils import core, vote, translate, language, audio

st.set_page_config(page_title="🪔 Indian Wisdom", layout="wide")

# 🔥 Custom Animated CSS Styling
st.markdown("""
    <style>
    /* General Page Style */
    .stApp {
        animation: fadeIn 1.5s ease-in;
        background: linear-gradient(to right, #fffaf0, #fefbd8);
    }

    /* Fade-in animation */
    @keyframes fadeIn {
        0% {opacity: 0;}
        100% {opacity: 1;}
    }

    /* Animated headers */
    h1, h2, h3 {
        color: #4b2e83;
        animation: pulseHeader 2s infinite alternate;
    }

    @keyframes pulseHeader {
        0% { text-shadow: 0 0 5px #c3b1e1; }
        100% { text-shadow: 0 0 15px #b39ddb; }
    }

    /* Fancy buttons */
    .stButton > button {
        background-color: #7e57c2;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        border-radius: 8px;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background-color: #5e35b1;
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    .stTextInput, .stSelectbox, .stFileUploader {
        transition: transform 0.3s ease;
    }

    .stTextInput:hover, .stSelectbox:hover, .stFileUploader:hover {
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🪔 Indian Wisdom: Local Proverbs Collector")

# Sidebar Navigation
st.sidebar.title("☰ Navigation")
page = st.sidebar.radio("Go to", ["📥 Submit Proverb", "📊 Vote", "🌐 Translate", "🎤 Record Audio"])

# --- Submit Proverb ---
if page == "📥 Submit Proverb":
    st.header("📥 Submit a Proverb")
    proverb = st.text_input("Enter a proverb")
    region = st.selectbox("Select the region/language", language.get_languages())
    if st.button("Submit"):
        if proverb.strip() and region:
            core.save_proverb(proverb.strip(), region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("⚠️ Please fill all fields.")

# --- Vote ---
elif page == "📊 Vote":
    st.header("📊 Vote for a Proverb")
    proverbs = core.load_proverbs()
    if not proverbs:
        st.info("No proverbs found.")
    else:
        selected = st.selectbox("Choose a proverb to vote for", [p['proverb'] for p in proverbs])
        if st.button("Vote"):
            vote.increment_vote(selected)
            st.success("👍 Thanks for your vote!")

# --- Translate ---
elif page == "🌐 Translate":
    st.header("🌐 Translate a Proverb")
    input_text = st.text_input("Enter text to translate")
    target_lang = st.selectbox("Translate to", language.get_languages())
    if st.button("Translate"):
        if input_text.strip() and target_lang:
            translated = translate.mock_translate(input_text.strip(), target_lang)
            st.info(f"🗣️ Translated '{input_text}' to [{target_lang}]: {translated}")
        else:
            st.warning("⚠️ Please enter text and select language.")

# --- Record Audio ---
elif page == "🎤 Record Audio":
    st.header("🎤 Record a Proverb Audio")
    audio_bytes = st.file_uploader("Upload recorded proverb audio (MP3 or WAV)", type=["mp3", "wav"])
    if audio_bytes:
        audio.save_audio_file(audio_bytes)
        st.success("🔊 Audio uploaded successfully!")
        st.audio(audio_bytes)

# Optional stats on sidebar
st.sidebar.markdown("---")
if st.sidebar.checkbox("📈 Show Region Stats"):
    st.sidebar.subheader("📍 Region-wise Stats")
    stats = core.get_stats()
    for region, count in stats.items():
        st.sidebar.write(f"✅ {region}: {count}")
