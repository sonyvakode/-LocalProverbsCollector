import streamlit as st
from utils import core, vote, translate
from PIL import Image
import base64
import random

# Background setup
def set_custom_bg(png_file):
    with open(png_file, "rb") as f:
        data = base64.b64encode(f.read()).decode()
    st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{data}");
            background-size: cover;
            background-attachment: fixed;
            background-position: center;
        }}
        </style>
    """, unsafe_allow_html=True)

set_custom_bg("streamlit_bg_gradient.png")  # Use your new image here

# Sidebar Navigation
st.sidebar.title("Go to")
section = st.sidebar.radio("", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# Title
st.markdown("## 🪔 Indian Wisdom: Local Proverbs Collector")

# Submit Section
if section == "Submit":
    st.subheader("📝 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")
    audio = st.file_uploader("Or upload an audio file (WAV/MP3)", type=["wav", "mp3"])
    location = st.text_input("Enter your location or region")
    if st.button("Submit"):
        core.save_proverb(proverb, location, audio)
        st.success("✅ Proverb submitted successfully!")

# Translate Section
elif section == "Translate":
    st.subheader("🌐 Translate a Proverb")
    untranslated = core.get_untranslated()
    if untranslated:
        to_translate = random.choice(untranslated)
        st.write("Translate this proverb:")
        st.info(to_translate["text"])
        translation = st.text_input("Enter translation:")
        if st.button("Submit Translation"):
            translate.save_translation(to_translate["id"], translation)
            st.success("✅ Translation saved.")
    else:
        st.success("🎉 All proverbs are translated!")

# Stats Section
elif section == "Stats":
    st.subheader("📊 App Statistics")
    stats = core.get_stats()
    st.write(f"📌 Total Proverbs: {stats['total']}")
    st.write(f"🌍 Translated: {stats['translated']}")
    st.write(f"🔈 Audio Uploads: {stats['audio']}")

# Proverb of the Day Section
elif section == "Proverb of the Day":
    st.subheader("🎁 Proverb of the Day")

    # Sample list
    proverbs = [
        "A stitch in time saves nine.",
        "Actions speak louder than words.",
        "The early bird catches the worm.",
        "A journey of a thousand miles begins with a single step.",
        "Wisdom is wealth.",
        "Even monkeys fall from trees.",
        "Words are the voice of the heart.",
        "Patience is a tree whose root is bitter, but its fruit is sweet.",
        "No smoke without fire.",
        "A coconut shell seems big to a louse."
    ]

    daily = random.sample(proverbs, 3)
    for prov in daily:
        st.markdown(f"""
        <div style="background-color: rgba(255, 255, 200, 0.8); padding: 1rem; border-radius: 10px; margin-bottom: 1rem;">
            <strong>{prov}</strong>
            <br><br>
            <div style='text-align: right'>
                ❤️ <button style='border: none; background: none; font-size: 1.1em; cursor: pointer;'>Like</button>
            </div>
        </div>
        """, unsafe_allow_html=True)

# Settings Section
elif section == "Settings":
    st.subheader("⚙️ Settings")
    st.info("Theme and customization options will be added soon.")
