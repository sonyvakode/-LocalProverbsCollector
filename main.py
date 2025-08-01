import streamlit as st
import random
import base64
import time
from utils import core, translate, vote

# Updated background setup with light overlay
def set_background():
    image_url = "https://t4.ftcdn.net/jpg/08/04/67/63/360_F_804676330_hVxnVs6vGpu1uL6WmNL6qxSApym3zxUF.jpg"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255, 255, 255, 0.6), rgba(255, 255, 255, 0.6)), url("{image_url}");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
            background-position: center;
        }}
        h1, h2, h3, .stButton>button, .css-10trblm, .css-1v3fvcr {{
            color: #000 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )

# Proverb of the Day section with rotation and like button
def show_proverb_of_the_day():
    st.subheader("📜 Proverb of the Day")

    all_proverbs = vote.get_all()
    if not all_proverbs:
        st.info("No proverbs available yet. Please submit one!")
        return

    proverb = random.choice(all_proverbs)
    proverb_text = proverb.get("text", "")
    region = proverb.get("region", "Unknown")
    lang = proverb.get("language", "Unknown")
    likes = proverb.get("likes", 0)
    views = proverb.get("views", 0)

    st.markdown(f"""
    <div style='border: 1px solid #ccc; padding: 1em; border-radius: 10px; background-color: rgba(255, 255, 255, 0.8);'>
        <p style='font-size: 1.2em;'><strong>{proverb_text}</strong></p>
        <small>📍 {region} | 🌐 {lang}</small><br>
        ❤️ {likes} &nbsp;&nbsp; 👁️ {views}
    </div>
    """, unsafe_allow_html=True)

    if st.button("❤️ Like this proverb"):
        vote.like_proverb(proverb_text)
        st.success("Liked!")

# Main app
def main():
    set_background()

    st.title("🌸 Indian Wisdom: Local Proverbs Collector")

    menu = ["🏠 Home", "➕ Submit", "🌐 Translate", "📊 Stats"]
    choice = st.sidebar.radio("Navigate", menu)

    if choice == "🏠 Home":
        show_proverb_of_the_day()

    elif choice == "➕ Submit":
        st.subheader("Submit a Proverb")
        text = st.text_input("Enter your proverb")
        region = st.selectbox("Select Region", ["North", "South", "East", "West", "Central"])
        language = st.selectbox("Language", ["Hindi", "Tamil", "Telugu", "Malayalam", "Kannada", "Gujarati", "Punjabi"])
        if st.button("Submit"):
            if text:
                core.save_proverb(text, region, language)
                st.success("Proverb submitted successfully!")
            else:
                st.warning("Please enter a proverb.")

    elif choice == "🌐 Translate":
        st.subheader("Translate a Proverb")
        translate.translate_proverb()

    elif choice == "📊 Stats":
        st.subheader("Proverb Stats")
        core.load_stats()

if __name__ == "__main__":
    main()
