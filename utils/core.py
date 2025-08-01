import streamlit as st
import pandas as pd
import os

DATA_FILE = "data/proverbs.txt"

def save_proverb(text, region, language):
    with open(DATA_FILE, "a", encoding="utf-8") as f:
        line = f"{text}|{region}|{language}|0|0\n"
        f.write(line)

def load_proverbs():
    proverbs = []
    if not os.path.exists(DATA_FILE):
        return proverbs

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split("|")
            if len(parts) >= 5:
                proverbs.append({
                    "text": parts[0],
                    "region": parts[1],
                    "language": parts[2],
                    "likes": int(parts[3]),
                    "views": int(parts[4])
                })
    return proverbs

def load_stats():
    proverbs = load_proverbs()
    if not proverbs:
        st.warning("No stats available.")
        return

    df = pd.DataFrame(proverbs)
    st.bar_chart(df["likes"], use_container_width=True)
    st.markdown(f"**Total Proverbs:** {len(proverbs)}")
