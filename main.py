import streamlit as st
from utils import core, translate, vote
import random

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# Sidebar Navigation
with st.sidebar:
    st.title("📚 Indian Wisdom")
    page = st.radio("Navigate", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# Sample Regions for Dropdown
regions_list = [
    "Andhra Pradesh", "Tamil Nadu", "Punjab","Telangana", "West Bengal", "Maharashtra",
    "Karnataka", "Kerala", "Gujarat", "Assam", "Uttar Pradesh", "Odisha", "Bihar", "Rajasthan", "Delhi"
]

# Sample Extra Proverbs
extra_proverbs = [
    {"proverb": "Patience is the key to paradise.", "region": "Kashmir"},
    {"proverb": "Even a hare will bite when it is cornered.", "region": "Tamil Nadu"},
    {"proverb": "Words are like arrows, once loosed you cannot call them back.", "region": "Assam"},
    {"proverb": "One thread for the needle, one for the knot.", "region": "Maharashtra"},
    {"proverb": "He who digs a pit for others falls into it himself.", "region": "Gujarat"},
    {"proverb": "A single tree does not make a forest.", "region": "Kerala"}
]

# Pages
if page == "Submit":
    st.header("📝 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")
    audio = st.file_uploader("Or upload an audio file (WAV/MP3)", type=["mp3", "wav"])
    region = st.selectbox("Select your region", regions_list)

    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.warning("⚠️ Please enter a proverb before submitting.")

elif page == "Translate":
    st.header("🌐 Translate a Proverb")
    text = st.text_input("Enter proverb to translate")

    lang_map = {
        "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn",
        "Marathi": "mr", "Malayalam": "ml", "Gujarati": "gu", "Punjabi": "pa", "Urdu": "ur",
        "Assamese": "as", "Odia": "or", "Sanskrit": "sa", "English": "en", "Arabic": "ar",
        "French": "fr", "Spanish": "es", "German": "de", "Chinese": "zh-CN", "Japanese": "ja",
        "Russian": "ru", "Korean": "ko", "Portuguese": "pt", "Italian": "it", "Turkish": "tr"
    }

    chosen_lang = st.selectbox("🎯 Target language", list(lang_map.keys()))

    if st.button("Translate"):
        if text.strip():
            lang_code = lang_map[chosen_lang]
            result = translate.translate(text, lang_code)
            st.success(result)
        else:
            st.warning("⚠️ Please enter a proverb to translate.")

elif page == "Stats":
    st.header("📊 Region-wise Contributions")
    stats = core.get_stats()
    if stats:
        st.bar_chart(stats)
    else:
        st.warning("ℹ️ No statistics available yet.")

elif page == "Proverb of the Day":
    st.header("🎁 Today's Proverbs")
    
    # 1 from real data + 3 from static
    primary = vote.get_random()
    featured = [primary] if primary else []
    featured += random.sample(extra_proverbs, 3)

    for item in featured:
        proverb_text = item["proverb"]
        region = item.get("region", "India")
        st.markdown(f"""
            <div style='padding: 15px; background: rgba(255,255,255,0.8); border-radius: 10px; margin-bottom: 20px;'>
                <h5 style='margin-bottom: 5px;'>{proverb_text}</h5>
                <p style='font-size: 0.85rem; color: #555;'>📍 Region: {region}</p>
                ❤️ <span style='font-size: 0.85rem; color: #777;'>Like</span>
            </div>
        """, unsafe_allow_html=True)

elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More app configuration settings coming soon.")

# Transparent background with gradient overlay
st.markdown("""
<style>
body {
    background: linear-gradient(rgba(255,255,255,0.8), rgba(255,255,255,0.8)), url('https://images.unsplash.com/photo-1584697964154-df6c03c99fb5?auto=format&fit=crop&w=1600&q=80');
    background-size: cover;
    background-attachment: fixed;
}
</style>
""", unsafe_allow_html=True)
