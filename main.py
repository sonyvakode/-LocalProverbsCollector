import streamlit as st
from utils import core, vote, translate, language, audio

st.set_page_config(page_title="Indian Wisdom: Local Proverbs Collector", layout="wide")

# Inject background and style
st.markdown("""
    <style>
        /* Background Gradient */
        body {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        }

        /* Main container styling */
        .main {
            background-color: #ffffffcc;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 0 30px rgba(0,0,0,0.1);
            animation: fadeIn 1.2s ease-in-out;
        }

        /* Title glow effect */
        .title-glow {
            text-align: center;
            font-size: 2.4em;
            font-weight: bold;
            padding: 10px;
            color: #333333;
            text-shadow: 0 0 8px #f7b733, 0 0 16px #fc4a1a;
        }

        /* Smooth fade-in animation */
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(20px); }
            100% { opacity: 1; transform: translateY(0); }
        }
    </style>
""", unsafe_allow_html=True)

# Render Title
st.markdown('<div class="title-glow">🪔 Indian Wisdom: Local Proverbs Collector</div>', unsafe_allow_html=True)
st.markdown('<div class="main">', unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("☰ Choose Mode")
page = st.sidebar.radio("Go to", ["📥 Submit", "📊 Vote", "🌐 Translate", "🎤 Record Audio"])

# --- Submit Proverb ---
if page == "📥 Submit":
    st.subheader("📝 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")
    audio_bytes = st.file_uploader("Or upload an audio file (MP3/WAV)", type=["mp3", "wav"])
    region = st.text_input("Enter your location or region")

    if st.button("Submit"):
        if proverb.strip():
            core.save_proverb(proverb.strip(), region or "Unknown")
            if audio_bytes:
                audio.save_audio_file(audio_bytes)
            st.success("Thanks for submitting your proverb!")
        else:
            st.warning("Please enter a proverb or upload audio.")

# --- Vote ---
elif page == "📊 Vote":
    st.subheader("📊 Vote for a Proverb")
    proverbs = core.load_proverbs()
    if not proverbs:
        st.info("No proverbs available yet.")
    else:
        selected = st.selectbox("Choose a proverb to vote for", [p['proverb'] for p in proverbs])
        if st.button("Vote"):
            vote.increment_vote(selected)
            st.success("Thanks for voting!")

# --- Translate ---
elif page == "🌐 Translate":
    st.subheader("🌐 Translate a Proverb")
    input_text = st.text_input("Enter the text to translate")
    target_lang = st.selectbox("Translate to", language.get_languages())
    if st.button("Translate"):
        if input_text.strip() and target_lang:
            translated = translate.mock_translate(input_text.strip(), target_lang)
            st.info(f"Translated '{input_text}' to [{target_lang}]: {translated}")
        else:
            st.warning("Please enter text and select a language.")

# --- Record Audio ---
elif page == "🎤 Record Audio":
    st.subheader("🎤 Record a Proverb")
    audio_file = st.file_uploader("Upload your audio (MP3/WAV)", type=["mp3", "wav"])
    if audio_file:
        audio.save_audio_file(audio_file)
        st.success("Audio saved successfully!")
        st.audio(audio_file)

# Stats Toggle
st.sidebar.markdown("---")
if st.sidebar.checkbox("📈 Show Region Stats"):
    st.sidebar.subheader("Region Stats")
    stats = core.get_stats()
    for region, count in stats.items():
        st.sidebar.write(f"{region}: {count}")

# End of main block
st.markdown("</div>", unsafe_allow_html=True)
