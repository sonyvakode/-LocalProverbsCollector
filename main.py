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

# Show rotating proverbs with like button
def show_proverb_of_the_day():
    st.markdown("### 🌟 Proverb of the Day:")
    all_proverbs = vote.get_all()
    if all_proverbs:
        proverb = random.choice(all_proverbs)
        st.markdown(f"<p style='font-size: 24px;'>{proverb['text']}</p>", unsafe_allow_html=True)

        if st.button("❤️ Like this proverb"):
            vote.like_proverb(proverb["text"])
        st.write(f"👍 Likes: {proverb.get('likes', 0)}")
    else:
        st.write("No proverbs available yet. Submit one!")

# Submit a new proverb
def submit_proverb():
    st.header("📤 Submit a Proverb")
    proverb = st.text_input("Enter your local proverb:")
    region = st.selectbox("Select region:", ["North", "South", "East", "West", "Central", "North-East"])
    if st.button("Submit"):
        if proverb.strip():
            core.save_proverb(proverb.strip())
            st.success("Proverb saved successfully!")
        else:
            st.warning("Proverb cannot be empty.")

# Translate section
def translate_section():
    st.header("🌐 Translate a Proverb")
    text = st.text_input("Enter proverb to translate:")
    if st.button("Translate"):
        if text.strip():
            translated = translate.translate_text(text)
            st.write("Translated Proverb:", translated)
        else:
            st.warning("Please enter text to translate.")

# Statistics section
def stats_section():
    st.header("📊 Proverbs Stats")
    stats = core.load_stats()
    if stats:
        st.bar_chart(stats)
    else:
        st.info("No data to display yet.")

# Page router
def main():
    st.set_page_config(page_title="Indian Wisdom", layout="wide")
    set_background()
    st.sidebar.title("Navigate")
    page = st.sidebar.radio("Go to", ["Home", "Submit", "Translate", "Stats"])

    st.markdown("<h1 style='text-align: center;'>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)
    
    if page == "Home":
        show_proverb_of_the_day()
    elif page == "Submit":
        submit_proverb()
    elif page == "Translate":
        translate_section()
    elif page == "Stats":
        stats_section()

if __name__ == "__main__":
    main()
