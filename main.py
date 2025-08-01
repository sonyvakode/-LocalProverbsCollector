import streamlit as st
import random
import time
import base64
from utils import core, translate, vote

def set_background():
    image_url = "https://t4.ftcdn.net/jpg/08/04/67/63/360_F_804676330_hVxnVs6vGpu1uL6WmNL6qxSApym3zxUF.jpg"
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(255,255,255,0.6), rgba(255,255,255,0.6)), url("{image_url}");
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
        unsafe_allow_html=True
    )

def show_proverb_of_the_day():
    try:
        with open("data/proverbs.txt", "r", encoding="utf-8") as f:
            all_proverbs = [line.strip() for line in f if line.strip()]
        if not all_proverbs:
            st.warning("No proverbs available.")
            return
        proverb_line = random.choice(all_proverbs)
        text, region, lang, views, likes = proverb_line.split("|")

        st.markdown("## 🌞 Proverb of the Day")
        st.markdown(f"**📝 Proverb**: {text}")
        st.markdown(f"🌐 **Language**: {lang} | 📍 **Region**: {region}")
        st.markdown(f"👁️ Views: {views} | ❤️ Likes: {likes}")
    except Exception as e:
        st.error(f"Failed to load proverb of the day: {e}")

def main():
    set_background()
    st.title("🪔 Indian Wisdom: Local Proverbs Collector")

    show_proverb_of_the_day()

    st.header("➕ Submit a New Proverb")
    proverb = st.text_input("Enter a proverb")
    region = st.selectbox("Select region", ["Tamil Nadu", "Kerala", "Maharashtra", "Gujarat", "Punjab"])
    language = st.selectbox("Language", ["Hindi", "English", "Tamil", "Telugu", "Gujarati"])
    if st.button("Submit"):
        if proverb:
            core.save_proverb(proverb, region, language)
            st.success("Proverb saved successfully!")

    st.header("📊 Stats")
    stats = core.load_stats()
    st.bar_chart(stats)

    st.header("🌐 Translate a Proverb")
    translate.translate_interface()

    st.header("👍 Vote for Proverbs")
    vote.vote_interface()

if __name__ == "__main__":
    main()
