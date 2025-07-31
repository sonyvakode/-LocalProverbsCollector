import streamlit as st
from utils import core, vote
from datetime import datetime

st.set_page_config(page_title="Indian Wisdom", layout="centered")

st.markdown("""
    <style>
    body {
        background: linear-gradient(to bottom, #def3e2, #d8e4f5);
    }
    .proverb-card {
        background-color: #fff5cc;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 5px 5px 10px rgba(0,0,0,0.1);
        margin-top: 20px;
    }
    .action-icons span {
        margin-right: 1.5rem;
        font-size: 0.9rem;
        color: #333;
    }
    .category-btn {
        background-color: #fff8e1;
        border: none;
        padding: 0.6rem 1rem;
        border-radius: 12px;
        margin: 0.3rem;
        font-weight: 600;
        cursor: pointer;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar Navigation
st.sidebar.title("🎨 Choose Mode")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark", "Colorful"])
section = st.sidebar.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

if section == "Proverb of the Day":
    st.markdown("## 🎁 Proverb of the Day")
    proverb = core.get_random_proverb()

    with st.container():
        st.markdown(f"""
        <div class="proverb-card">
            <h3>{proverb['text']}</h3>
            <p><i>Brought from the heart of Indian villages.</i></p>
            <hr>
            <div class="action-icons">
                <span>❤️ {proverb['likes']}</span>
                <span>👁️ {proverb['views']}</span>
                <span>⏱️ 1 min read</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### 📝 Read by category:")
    categories = [
        ("❤️ Love", "love"), ("🏃 Motivation", "motivation"), ("🧠 Wisdom", "wisdom"),
        ("💼 Work", "work"), ("👑 Philosophy", "philosophy"), ("🧘 Ethics & Morals", "ethics")
    ]
    cols = st.columns(3)
    for i, (label, key) in enumerate(categories):
        with cols[i % 3]:
            st.button(label, key=key)

# Slide-in: Voting region
with st.sidebar.expander("✨ Vote on Proverb"):
    selected = vote.vote_on_proverb()
    if selected:
        st.success("Thanks for your vote!")

