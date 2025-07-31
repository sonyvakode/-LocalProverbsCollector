import streamlit as st

def vote_on_proverb():
    st.write("What do you think of today’s proverb?")
    choice = st.radio("Your reaction", ["❤️ Love it", "🤔 Needs better", "🤯 Blown away"])
    if st.button("Submit Vote"):
        return choice
    return None
