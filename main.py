import streamlit as st
from utils import core, translate, vote

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# ---- Choose your preferred background URL here ----
background_url = "https://images.unsplash.com/photo-1683078142484-2c7aec5ae048?auto=format&fit=crop&w=1950&q=80"  # pastel blur
# background_url = "https://images.unsplash.com/photo-1683078243370-ab777dd24f11?auto=format&fit=crop&w=1950&q=80"  # pastel orange-pink
# background_url = "https://images.unsplash.com/photo-1683078235170-8b3bcd1549cb?auto=format&fit=crop&w=1950&q=80"  # yellow-green mix
# background_url = "https://images.unsplash.com/photo-1683078264564-0bd24fcd74f1?auto=format&fit=crop&w=1950&q=80"  # beige-white bokeh

st.markdown(f"""
    <style>
    body {{
        background: url("{background_url}") no-repeat center center fixed;
        background-size: cover;
    }}
    .block-container {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 12px;
    }}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.title("Choose Mode")
    theme = st.radio("Choose Theme", ["Light", "Dark", "Colorful"])
    page = st.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

if page == "Submit":
    st.header("🪔 Indian Wisdom: Local Proverbs Collector")
    st.subheader("📝 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")
    audio = st.file_uploader("Or upload an audio file (WAV/MP3)", type=["mp3", "wav"])
    region = st.text_input("Enter your location or region")
    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("Proverb submitted successfully!")
        else:
            st.warning("Please enter a proverb before submitting.")

elif page == "Translate":
    st.header("🌐 Translate a Proverb")
    text = st.text_input("Enter proverb to translate")
    lang_map = {
        "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", 
        "Bengali": "bn", "Marathi": "mr", "Malayalam": "ml", "Gujarati": "gu", 
        "Punjabi": "pa", "Urdu": "ur", "Assamese": "as", "Odia": "or", "Sanskrit": "sa", 
        "English": "en", "Arabic": "ar", "French": "fr", "Spanish": "es", 
        "German": "de", "Chinese": "zh-CN", "Japanese": "ja", "Russian": "ru", 
        "Korean": "ko", "Portuguese": "pt", "Italian": "it", "Turkish": "tr"
    }
    chosen_lang = st.selectbox("🎯 Target language", list(lang_map.keys()))
    if st.button("Translate"):
        if text.strip():
            result = translate.translate(text, lang_map[chosen_lang])
            st.success(result)
        else:
            st.warning("Please enter a proverb to translate.")

elif page == "Stats":
    st.header("📊 Region-wise Contributions")
    stats = core.get_stats()
    if stats:
        st.json(stats)
    else:
        st.warning("No statistics available yet.")

elif page == "Proverb of the Day":
    st.header("🎁 Proverb of the Day")
    proverb = vote.get_random()
    if proverb:
        st.success(proverb)
        if st.button("❤️ Like"):
            vote.increment_vote(proverb)
            st.toast("Thanks for liking!", icon="❤️")
    else:
        st.warning("No proverb found.")

elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More app configuration settings coming soon.")
