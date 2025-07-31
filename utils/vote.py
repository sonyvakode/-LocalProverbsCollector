import streamlit as st
from utils.core import load_proverbs, save_proverb

def render_voting_ui(proverbs):
    for i, entry in enumerate(proverbs):
        col1, col2 = st.columns([4, 1])
        with col1:
            st.write(f"**{entry['proverb']}** ({entry['region']})")
        with col2:
            if st.button(f"👍 {entry['votes']}", key=f"vote_{i}"):
                entry['votes'] += 1
                save_all_proverbs(proverbs)
                st.experimental_rerun()

def save_all_proverbs(data):
    import os, json
    os.makedirs("data", exist_ok=True)
    with open("data/proverbs.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
