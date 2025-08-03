import streamlit as st
import random
from utils import core, translate, vote, audio, language
import base64

# --- Set Light Background Image ---
def set_background(image_file):
    with open(image_file, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-color: rgba(255,255,255,0.5);
        z-index: -1;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_background("sunrise_background.png")


# --- App Title ---
st.markdown(
    "<h1 style='text-align: center; font-weight: bold;'>📚 Indian Wisdom: Local Proverb Collector</h1>",
    unsafe_allow_html=True
)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📝 Submit Proverb", "📖 Proverb of the Day", "📊 Stats & Translate"])

# --- Tab 1: Submit Proverb ---
with tab1:
    st.subheader("Share a Local Proverb")
    st.markdown(
        "<p style='font-size:16px;'>Local proverbs are cultural gems passed down through generations — share one from your city, town, or village!</p>",
        unsafe_allow_html=True
    )

    proverb = st.text_area("Enter Proverb")
    lang = st.selectbox("Select Language", language.languages())
    region = st.text_input("Enter Region (City or State)")
    audio_file = st.file_uploader("Optional: Upload Audio", type=["wav", "mp3", "m4a"])

    if audio_file:
        transcribed = audio.transcribe_audio(audio_file)
        if transcribed:
            st.success("Transcription: " + transcribed)
            proverb = transcribed

    if st.button("Submit"):
        if proverb.strip() and lang.strip():
            core.save_proverb(proverb.strip(), lang, region)
            st.success("Proverb saved successfully!")
        else:
            st.error("Please provide both proverb and language.")

# --- Tab 2: Proverb of the Day ---
with tab2:
    st.subheader("Proverb of the Day")
    all_proverbs = core.load_proverbs()
    if all_proverbs:
        selected = random.choice(all_proverbs)
        st.markdown(
            f"""
            <div style='padding: 20px; background-color: #ffffffcc; border-radius: 10px; margin-top: 10px;'>
                <h3 style='font-weight:600; color:#222;'>{selected['text']}</h3>
                <p><b>Language:</b> {selected['lang']} &nbsp; | &nbsp; <b>Region:</b> {selected['region']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.info("No proverbs available yet. Be the first to submit one!")

# --- Tab 3: Stats and Translate ---
with tab3:
    st.subheader("Translation")
    text = st.text_input("Enter proverb to translate")
    from_lang = st.selectbox("From Language", language.languages())
    to_lang = st.selectbox("To Language", language.languages())

    if st.button("Translate"):
        if text:
            try:
                translated = translate.translate_text(text, from_lang, to_lang)
                st.success(f"Translation: {translated}")
            except Exception as e:
                st.error("Translation failed.")
        else:
            st.warning("Please enter a proverb to translate.")

    st.markdown("---")
    st.subheader("Submission Stats")

    stats = core.load_stats()
    if stats:
        st.write("Total Proverbs Submitted:", stats.get("total", 0))
        st.write("By Language:", stats.get("by_language", {}))
    else:
        st.info("No stats available.")
