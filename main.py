import streamlit as st
import random
import base64
import requests
from utils import core, translate, vote, audio, language

# Page setup
st.set_page_config(page_title="Indian Wisdom", layout="centered")

# Session State
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False
if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "user_identifier" not in st.session_state:
    st.session_state.user_identifier = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"   # login | signup | reset_password | change_password

# API Base URL
API_BASE_URL = "https://api.corpus.swecha.org/api/v1/auth"

# Background (unchanged)
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            color: #111 !important;
        }}
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.85), rgba(255,255,255,0.85)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
        }}
        textarea, input, select {{
            background-color: white !important;
            color: #000 !important;
            border: 1px solid #ccc !important;
            border-radius: 5px !important;
        }}
        label, .stSelectbox > div, .stTextInput > div, .stTextArea > div {{
            color: #111 !important;
            font-weight: 500 !important;
        }}
        .solid-box {{
            background-color: #ffffffcc;
            padding: 1rem;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            margin-bottom: 1.5rem;
        }}
        .center {{
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_background("Background.jpg")

# Custom CSS for card and buttons (optional, maintain consistent style)
st.markdown("""
<style>
.card {
    background: #fff !important;
    border-radius: 20px;
    box-shadow: 0 8px 40px 0 rgba(25, 62, 152, 0.10);
    max-width: 380px;
    margin: 54px auto;
    display: flex;
    flex-direction: column;
    padding: 38px 30px 32px 30px;
}
h2 {
    font-weight: 700;
    font-size: 2.0rem;
    text-align: center;
    color: #111;
    margin-bottom: 1.13rem;
}
.stTextInput > div > div > input,
input[type="text"], input[type="password"], input[type="email"] {
    border-radius: 10px !important;
    border: 1.5px solid #e0e6ef !important;
    background: #f6f8fa !important;
    padding: 0.87rem 1.1rem !important;
    font-size: 1.06rem !important;
    color: #162447 !important;
    margin-bottom: 1.00rem !important;
}
.stButton > button {
    border-radius: 10px !important;
    padding: 0.84rem 0 !important;
    width: 100% !important;
    background: linear-gradient(90deg, #1948CB 60%, #176DF7 100%) !important;
    color: #fff !important;
    font-size: 1.09rem !important;
    font-weight: 700 !important;
    border: none !important;
    margin-top: 0.2rem !important;
    margin-bottom: 0.65rem !important;
    box-shadow: 0 2px 20px 0 rgba(25, 62, 152, 0.09);
    transition: background 0.2s;
}
.switch-links {
    text-align: center;
    margin-top: 13px;
    font-size: 0.98rem;
}
.switch-links a {
    color: #307aff;
    font-weight: 500;
    text-decoration: none;
    cursor: pointer;
}
.forgot-link {
    font-size: 0.97rem;
    color: #307aff;
    text-decoration: none;
    margin-bottom: 1.0rem;
    margin-top: -0.8rem;
    display: inline-block;
    cursor: pointer;
    font-weight: 500;
}
@media (max-width: 600px) {
    .card {
        width: 99vw;
        min-width: 0;
        padding: 20px 4vw 17px 4vw;
        margin-top: 6vw;
    }
}
</style>
""", unsafe_allow_html=True)

# Authentication block replaced with your snippet exactly
if not st.session_state.authenticated:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if st.session_state.auth_mode == "login":
            st.markdown("<h2>Sign In</h2>", unsafe_allow_html=True)
            user_input = st.text_input("📱 Enter your Phone Number", max_chars=10)
            if not st.session_state.otp_sent:
                if st.button("Send OTP"):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/send-otp",   # ✅ fixed path
                            json={"phone": user_input}
                        )
                        if response.status_code == 200:
                            st.session_state.otp_sent = True
                            st.session_state.user_identifier = user_input
                            st.success("✅ OTP sent successfully!")
                        else:
                            st.error(f"❌ Failed: {response.text}")
                    except Exception as e:
                        st.error(f"Error: {e}")
            else:
                otp = st.text_input("Enter OTP", type="password")
                if st.button("Verify OTP"):
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/verify-otp",   # ✅ fixed path
                            json={"phone": st.session_state.user_identifier, "otp": otp}
                        )
                        if response.status_code == 200 and response.json().get("verified"):
                            st.session_state.authenticated = True
                            st.success("🎉 Login successful!")
                            st.rerun()
                        else:
                            st.error("❌ Invalid OTP.")
                    except Exception as e:
                        st.error(f"Error: {e}")
            st.markdown(
                """<div class="switch-links">
                    <a onClick="window.location.reload()">Sign Up</a> | 
                    <a onClick="window.location.reload()">Forgot Password?</a>
                </div>""",
                unsafe_allow_html=True,
            )
        elif st.session_state.auth_mode == "signup":
            st.markdown("<h2>Sign Up</h2>", unsafe_allow_html=True)
            phone = st.text_input("📱 Phone Number")
            password = st.text_input("🔑 Password", type="password")
            if st.button("Register"):
                try:
                    response = requests.post(f"{API_BASE_URL}/sign-up_send-otp",
                                             json={"phone": phone, "password": password})
                    if response.status_code == 200:
                        st.success("✅ Sign-up successful! Verify OTP sent.")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error(f"❌ Failed: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
        elif st.session_state.auth_mode == "reset_password":
            st.markdown("<h2>Reset Password</h2>", unsafe_allow_html=True)
            phone = st.text_input("📱 Phone Number")
            new_pass = st.text_input("🔑 New Password", type="password")
            if st.button("Reset Password"):
                try:
                    response = requests.post(f"{API_BASE_URL}/reset-password",
                                             json={"phone": phone, "new_password": new_pass})
                    if response.status_code == 200:
                        st.success("✅ Password reset successfully!")
                        st.session_state.auth_mode = "login"
                        st.rerun()
                    else:
                        st.error(f"❌ Failed: {response.text}")
                except Exception as e:
                    st.error(f"Error: {e}")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# MAIN APP
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "States"])

if page == "Home":
    st.subheader("Submit Your Proverb")
    with st.form("submit_form"):
        proverb = st.text_area("Enter a local proverb")
        meaning = st.text_area("Write the meaning of the proverb")
        city = st.selectbox("City/Region", ["Select", "Hyderabad", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Delhi", "Other"])
        lang = st.selectbox("Language", language.get_all_languages())
        audio_file = st.file_uploader("Upload Audio", type=["wav", "mp3", "m4a"])
        submitted = st.form_submit_button("Submit")
        if submitted:
            if audio_file:
                proverb_from_audio = audio.transcribe_audio(audio_file)
                proverb = proverb or proverb_from_audio
            if proverb and city != "Select":
                core.save_proverb(proverb, city, lang, meaning=meaning)
                try:
                    with open("data/proverbs.txt", "a", encoding="utf-8") as f:
                        f.write(f"{proverb.strip()} - {meaning.strip()}\n")
                except Exception as e:
                    st.error(f"⚠️ Failed to save: {e}")
                st.success("✅ Proverb saved successfully!")

    st.markdown("---")
    st.subheader("🌍 Translate a Proverb")
    proverb_to_translate = st.text_input("Enter proverb to translate")
    target_lang = st.selectbox("Choose target language", language.get_all_languages())
    if st.button("Translate"):
        if proverb_to_translate.strip():
            try:
                translated = translate.translate_text(proverb_to_translate, target_lang)
                st.success(f"Translated: {translated}")
            except Exception as e:
                st.error(f"⚠️ Translation failed: {e}")
        else:
            st.warning("Please enter a proverb to translate.")

elif page == "Proverb of the day":
    st.subheader("📝 Proverb of the Day")
    try:
        with open("data/proverbs.txt", "r", encoding="utf-8") as f:
            all_proverbs = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        all_proverbs = []
    if all_proverbs:
        selected = random.choice(all_proverbs)
        translated = translate.translate_text(selected, "English")
        st.markdown(
            f"""
            <div style='text-align: center; margin-top: 20px; font-size: 18px; color: #000;'>
                <p><b>✨ Original:</b> {selected}</p>
                <p><b>➡️ Translated:</b> {translated}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    else:
        st.warning("No proverbs available.")
    if st.button("🔄 Next Proverb"):
        st.rerun()

elif page == "States":
    st.subheader("📊 Proverbs Stats")
    stats = core.load_stats()
    st.write(f"Total Proverbs Collected: {stats.get('total_proverbs', 0)}")
    st.markdown("#### 🏆 Leaderboard")
    all_data = vote.get_all()
    region_counts = {}
    for item in all_data:
        region = item.get("city", "Unknown")
        region_counts[region] = region_counts.get(region, 0) + 1

    # Sort with Unknown last
    sorted_regions = sorted(
        region_counts.items(),
        key=lambda x: (x[0] == "Unknown", -x[1])
    )

    if sorted_regions:
        import matplotlib.pyplot as plt
        regions = [item[0] for item in sorted_regions[:10]]
        counts = [item[1] for item in sorted_regions[:10]]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(regions, counts, color='#0073e6')  # normal blue color
        ax.set_xlabel('Regions')
        ax.set_ylabel('Number of Proverbs')
        ax.set_title('Top 10 Regions by Proverb Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("**Detailed Rankings:**")
        for i, (region, count) in enumerate(sorted_regions[:10], start=1):
            st.write(f"{i}. {region}: {count} proverbs")
    else:
        st.info("No data yet.")
