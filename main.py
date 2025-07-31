import streamlit as st
from utils import core, translate, vote
from utils.audio import transcribe_audio

# --- Background image with base64 (transparent effect) ---
def set_custom_bg():
    bg_image = '''
    <style>
    .stApp {
        background-image: url("data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABkAAAAOECAIAAAB2L2r1AAAZRklEQVR4nO3YQW7CMBRAwbb3P2DPwQXcHVJBqRLihAed2bFI/G0i");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }
    </style>
    '''
    st.markdown(bg_image, unsafe_allow_html=True)

# Call it early to render
set_custom_bg()

# --- App Title ---
st.markdown("<h1 style='font-size: 2.5rem;'>🪔 Indian Wisdom: Local Proverbs Collector</h1>", unsafe_allow_html=True)
st.markdown("---")

# --- Navigation ---
tabs = ["Submit", "Translate", "Stats", "Proverb of the Day"]
selected = st.sidebar.radio("Go to", tabs)

# --- Submit Tab ---
if selected == "Submit":
    st.subheader("📝 Submit a Local Proverb")
    proverb = st.text_area("Type the proverb in your language")

    audio_file = st.file_uploader("Or upload an audio file (WAV/MP3)", type=["mp3", "wav"])
    location = st.text_input("Enter your location or region")

    if st.button("Submit"):
        if audio_file:
            proverb = transcribe_audio(audio_file)
        if proverb:
            core.save_proverb(proverb, location)
            st.success("✅ Proverb submitted successfully!")
        else:
            st.error("⚠️ Please enter or upload a proverb.")

# --- Translate Tab ---
elif selected == "Translate":
    st.subheader("🌍 Translate a Proverb")
    original = st.text_input("Enter the proverb to translate")
    target_lang = st.selectbox("Choose target language", ["en", "hi", "ta", "te", "kn", "ml", "bn"])

    if st.button("Translate"):
        if original:
            translated = translate.translate_proverb(original, target_lang)
            st.success(f"✅ Translated: {translated}")
        else:
            st.error("⚠️ Please enter a proverb to translate.")

# --- Stats Tab ---
elif selected == "Stats":
    st.subheader("📊 Proverb Statistics")
    stats = core.get_stats()
    st.write("**Total Proverbs:**", stats["total"])
    st.write("**Most Active Region:**", stats["top_region"])
    st.write("**Most Liked Proverb:**", stats["top_proverb"])

# --- Proverb of the Day ---
elif selected == "Proverb of the Day":
    st.subheader("🎁 Proverb of the Day")
    proverbs = vote.get_multiple(3)

    for proverb in proverbs:
        text = proverb["text"]
        likes = proverb.get("likes", 0)
        views = proverb.get("views", 0)

        with st.container():
            st.markdown(
                f"""
                <div style="background-color: #fff3c4; padding: 1.2rem; border-radius: 1rem; margin-bottom: 1.5rem;">
                    <h4 style="color:#333;">{text}</h4>
                    <p style="font-style: italic;">Brought from the heart of Indian villages.</p>
                    <hr>
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>❤️ {likes}</div>
                        <div>👁️ {views}</div>
                        <div>⏱️ 1 min read</div>
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )
            if st.button(f"Like this ❤️", key=f"like_{text}"):
                vote.increment_like(text)
                st.experimental_rerun()
