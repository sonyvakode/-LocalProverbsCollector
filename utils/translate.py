import streamlit as st

def translate_proverb():
    text = st.text_input("Enter proverb to translate")
    target_language = st.selectbox("Translate to", ["Hindi", "English", "Tamil", "Telugu", "Kannada", "Gujarati"])

    if st.button("Translate"):
        if text:
            # Dummy translation (mock logic)
            translated = f"{text} (translated to {target_language})"
            st.success(f"🔤 {translated}")
        else:
            st.warning("Please enter a proverb to translate.")
