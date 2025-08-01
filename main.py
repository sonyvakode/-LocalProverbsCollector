# main.py
import streamlit as st
import random
import base64
from utils import core, vote, translate

# ---------------- BACKGROUND SETUP -------------------
def set_background(image_file):
    with open(image_file, "rb") as f:
        data = f.read()
        encoded = base64.b64encode(data).decode()
    background_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        backdrop-filter: brightness(0.5);
    }}
    </style>
    """
    st.markdown(background_style, unsafe_allow_html=True)

set_background("background.jpg")

# ---------------- PROVERB OF THE DAY -------------------
def show_proverb_of_the_day():
    st.markdown("### 🌟 Proverb of the Day:")
    all_proverbs = vote.get_all()

    if isinstance(all_proverbs, list) and len(all_proverbs) > 0:
        try:
            proverb = random.choice(all_proverbs)
            st.markdown(f"<p style='font-size: 24px;'>{proverb['text']}</p>", unsafe_allow_html=True)

            if st.button("❤️ Like this proverb"):
                vote.like_proverb(proverb["text"])
            st.write(f"👍 Likes: {proverb.get('likes', 0)}")
        except Exception as e:
            st.error(f"Something went wrong while showing the proverb: {e}")
    else:
        st.info("No proverbs available yet. Submit one!")

# -------------------- PAGE NAVIGATION ------------------
def main():
    st.sidebar.title("Navigate")
    selection = st.sidebar.radio("", ["Home", "Submit", "Translate", "Stats"])

    st.markdown("""
        <h1 style='text-align: center; color: white;'>
            🪔 Indian Wisdom: Local Proverbs Collector
        </h1>
    """, unsafe_allow_html=True)

    if selection == "Home":
        show_proverb_of_the_day()

    elif selection == "Submit":
        st.subheader("Submit a New Proverb")
        text = st.text_input("Enter proverb:")
        if st.button("Submit"):
            if text:
                core.save_proverb(text)
                st.success("Proverb submitted!")
            else:
                st.warning("Please enter a proverb.")

    elif selection == "Translate":
        st.subheader("Translate a Proverb")
        translate.translate_ui()

    elif selection == "Stats":
        st.subheader("Proverb Stats")
        stats = core.load_stats()
        if stats:
            st.bar_chart(stats)
        else:
            st.info("No statistics available.")

if __name__ == "__main__":
    main()
