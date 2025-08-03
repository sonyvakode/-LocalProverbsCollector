import streamlit as st
import random
import base64
from utils import core, translate, vote, audio, language

st.set_page_config(page_title="Indian Wisdom: Local Proverbs Collector", layout="centered")

def set_background(image_path):
    try:
        with open(image_path, "rb") as image_file:
            encoded = base64.b64encode(image_file.read()).decode()
        css = f"""
        <style>
            .stApp {{
                background-image: url("data:image/jpeg;base64,{encoded}");
                background-size: cover;
                background-attachment: fixed;
                background-repeat: no-repeat;
                background-position: center;
            }}
            .block-container {{
                max-width: 800px;
                margin: auto;
                padding-top: 2rem;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 12px;
            }}
            h1, h2, h3 {{
                text-align: center;
            }}
            .stTextInput>div>div>input, .stSelectbox>div>div {{
                background-color: rgba(255,255,255,0.9);
            }}
        </style>
        """
        st.markdown(css, unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Background image not found. Please ensure 'Background.jpg' exists.")

set_background("Background.jpg")

st.title("📜 Indian Wisdom: Local Proverbs Collector")

menu = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "Stats", "Leadership"])

all_proverbs = core.load_proverbs()
stats = core.load_stats()

if menu == "Home":
    st.header("📝 Submit a Proverb")

    col1, col2 = st.columns([3, 1])
    with col1:
        user_proverb = st.text_input("Enter your proverb")
    with col2:
        region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central", "Northeast"])

    audio_file = st.file_uploader("Upload audio proverb", type=["mp3", "wav"])
    if st.button("Submit"):
        if user_proverb:
            core.save_proverb(user_proverb, region)
            st.success("Proverb saved!")
        elif audio_file:
            text = audio.transcribe_audio(audio_file)
            if text:
                core.save_proverb(text, region)
                st.success("Audio proverb saved!")
            else:
                st.error("Could not transcribe audio.")
        else:
            st.warning("Please enter a proverb or upload audio.")

elif menu == "Proverb of the day":
    st.header("🌟 Proverb of the Day")
    if all_proverbs:
        selected_proverb = random.choice(all_proverbs)
        display_lang = st.selectbox("Display in Language", ["en", "hi", "ta", "te", "bn"])
        translated = translate.translate_text(selected_proverb, display_lang)
        st.info(translated)
        st.button("Next Proverb", on_click=st.experimental_rerun)
    else:
        st.warning("No proverbs available.")

elif menu == "Stats":
    st.header("📊 Proverbs Stats")
    st.write(f"Total Proverbs Submitted: {len(all_proverbs)}")

elif menu == "Leadership":
    st.header("🏆 Leadership Board")
    st.info("This section can showcase top contributors, popular regions, or more in future updates.")
