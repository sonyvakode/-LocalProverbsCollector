import streamlit as st
from utils import core, translate, vote

st.set_page_config(page_title="Indian Wisdom", layout="wide", initial_sidebar_state="expanded")

# ---- Sidebar ----
with st.sidebar:
    st.title("Choose Mode")
    theme = st.radio("Choose Theme", ["Light", "Dark", "Colorful"])
    page = st.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# ---- Background and Styling ----
if theme == "Dark":
    st.markdown("""
        <style>
            body, .stApp { background-color: #121212; color: white; font-family: 'Segoe UI'; }
        </style>
    """, unsafe_allow_html=True)
elif theme == "Colorful":
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(to bottom right, #f9d423, #ff4e50);
                color: white;
                font-family: 'Segoe UI';
            }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            .stApp {
                background: linear-gradient(to bottom right, #e3ffe7, #d9e7ff);
                color: black;
                font-family: 'Segoe UI';
            }
        </style>
    """, unsafe_allow_html=True)

# ---- Main Pages ----
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
            st.warning("Please enter a proverb to translate.")

elif page == "Stats":
    st.header("📊 Region-wise Contributions")
    stats = core.get_stats()
    if stats:
        st.json(stats)
    else:
        st.warning("No statistics available yet.")

elif page == "Proverb of the Day":
    st.markdown("## 🎁 Proverb of the Day")
    proverb = vote.get_random()

    if proverb:
        st.markdown(f"""
        <div style="background-color: #fff3cd; padding: 25px; border-radius: 15px; border-left: 8px solid #ffc107; box-shadow: 2px 2px 12px rgba(0,0,0,0.1); margin-bottom: 20px;">
            <h3 style="color: #333;">{proverb}</h3>
            <p style="margin-top: 10px; color: #555;"><i>Brought from the heart of Indian villages.</i></p>
            <hr>
            <div style="display: flex; justify-content: space-between; color: #555;">
                <span>❤️ 997</span>
                <span>👁️ 309</span>
                <span>⏱️ 1 min read</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("#### 🔖 Read by category:")
        categories = [
            ("Love", "❤️"), ("Motivation", "🏃‍♂️"), ("Wisdom", "🦉"),
            ("Work", "💼"), ("Philosophy", "👑"), ("Ethics & Morals", "🧠")
        ]

        cols = st.columns(3)
        for i, (cat, emoji) in enumerate(categories):
            with cols[i % 3]:
                st.markdown(f"""
                    <div style='padding:10px 15px;margin:5px;background-color:#fef6e4;
                        border-radius:10px;display:inline-block;box-shadow:0 2px 5px rgba(0,0,0,0.1);'>
                        <strong>{emoji} {cat}</strong>
                    </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("No proverb found.")

elif page == "Settings":
    st.header("⚙️ App Settings")
    st.write("More app configuration settings coming soon.")
