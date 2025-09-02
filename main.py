import streamlit as st
import random
import base64
import requests
from utils import core, translate, vote, audio, language
import matplotlib.pyplot as plt

# Page setup
st.set_page_config(page_title="Indian Wisdom", layout="centered")

# ========== Session State ==========
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "otp_sent" not in st.session_state:
    st.session_state.otp_sent = False
if "user_identifier" not in st.session_state:
    st.session_state.user_identifier = ""
if "auth_mode" not in st.session_state:
    st.session_state.auth_mode = "login"

# ✅ API URL
API_BASE_URL = "https://api.corpus.swecha.org/api/v1/auth/login"

# ========== Background ==========
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
            color: black !important;
        }}
        h1, h2, p {{
            color: black !important;
        }}
        .stTextInput > div > div > input {{
            border-radius: 8px !important;
            border: 1px solid #ddd !important;
            padding: 0.75rem !important;
            color: black !important;
            font-weight: bold !important;
            background-color: white !important;
        }}
        .stButton > button {{
            background-color: white !important;
            color: black !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-weight: bold !important;
            width: 100% !important;
        }}
        @media (max-width: 768px) {{
            .stTextInput > div > div > input {{
                font-size: 16px !important;
            }}
            .stButton > button {{
                font-size: 16px !important;
                padding: 1rem !important;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("Background.jpg")

# ========== Helper: normalize phone to E.164 ==========
def normalize_indian_phone(raw: str) -> str:
    if not raw or not isinstance(raw, str):
        return ""
    s = raw.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
    if s.startswith("+"):
        if s[1:].isdigit() and 7 <= len(s[1:]) <= 15:
            return s
        return ""
    if s.startswith("0") and s[1:].isdigit() and len(s[1:]) == 10:
        return "+91" + s[1:]
    if s.startswith("91") and s.isdigit() and len(s) == 12:
        return "+" + s
    if s.isdigit() and len(s) == 10:
        return "+91" + s
    return ""

# ========== Authentication ==========
if not st.session_state.authenticated:
    st.markdown(
        "<h2 style='text-align:center; margin-top:80px; font-weight:bold;'>Welcome Back!</h2>",
        unsafe_allow_html=True
    )

    st.markdown("<div style='margin-top:20px;'>", unsafe_allow_html=True)
    
    user_input = st.text_input(
        "📱 Phone Number",
        placeholder="Enter your 10-digit phone number",
        max_chars=10,
        key="phone_input"
    )
    
    if not st.session_state.otp_sent:
        if st.button("Send OTP", key="send_otp_btn"):
            if not user_input.isdigit() or len(user_input) != 10:
                st.error("⚠️ Please enter a valid 10-digit phone number.")
            else:
                phone_e164 = normalize_indian_phone(user_input)
                if not phone_e164:
                    st.error("⚠️ Could not normalize phone number. Try again or include country code.")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/send-otp",
                            json={"phone_number": phone_e164},  # ✅ fixed key
                            timeout=10
                        )
                        if response.status_code == 200:
                            st.session_state.otp_sent = True
                            st.session_state.user_identifier = phone_e164
                            st.success(f"✅ OTP sent successfully to {phone_e164}!")
                            st.rerun()
                        else:
                            try:
                                err = response.json()
                                st.error(f"❌ Failed: {err}")
                            except Exception:
                                st.error(f"❌ Failed: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to backend: {e}")
    else:
        st.info(f"📱 OTP sent to {st.session_state.user_identifier}")
        otp = st.text_input(
            "🔢 Enter OTP",
            type="password",
            placeholder="Enter 6-digit OTP",
            max_chars=6,
            key="otp_input"
        )
        
        col1, col2 = st.columns([3, 1])
        with col1:
            if st.button("Verify & Sign In", key="verify_otp_btn"):
                if not otp or len(otp) < 4:
                    st.error("⚠️ Please enter the OTP you received.")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/verify-otp",
                            json={
                                "phone_number": st.session_state.user_identifier,
                                "otp_code": otp.strip()  # ✅ fixed key
                            },
                            timeout=10
                        )
                        if response.status_code == 200:
                            try:
                                json_resp = response.json()
                            except Exception:
                                json_resp = {}
                            if json_resp.get("verified", True):
                                st.session_state.authenticated = True
                                st.success("🎉 Login successful!")
                                st.rerun()
                            else:
                                st.error("❌ Invalid OTP.")
                        else:
                            try:
                                err = response.json()
                                st.error(f"❌ Failed: {err}")
                            except Exception:
                                st.error(f"❌ Failed: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to backend: {e}")
        
        with col2:
            if st.button("↩️", key="back_btn"):
                st.session_state.otp_sent = False
                st.session_state.user_identifier = ""
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ========== MAIN APP ==========
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)

# ✅ Sidebar Navigation + Logout
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "States"])
if st.sidebar.button("🚪 Logout"):
    st.session_state.authenticated = False
    st.session_state.otp_sent = False
    st.session_state.user_identifier = ""
    st.success("✅ Logged out successfully.")
    st.rerun()

# Page: Home
if page == "Home":
    st.subheader("Submit Your Proverb")
    with st.form("submit_form"):
        proverb = st.text_area("Enter a local proverb")
        meaning = st.text_area("Write the meaning of the proverb")
        city = st.selectbox(
            "City/Region",
            ["Select", "Hyderabad", "Mumbai", "Chennai", "Bangalore", "Kolkata", "Delhi", "Other"]
        )
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

# Page: Proverb of the Day
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
            <div style='text-align: center; margin-top: 20px; font-size: 18px; color: black;'>
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

# Page: States
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
    sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)
    
    if sorted_regions:
        regions = [item[0] for item in sorted_regions[:10]]
        counts = [item[1] for item in sorted_regions[:10]]
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(regions, counts, color='skyblue')
        ax.set_xlabel('Regions', fontsize=12)
        ax.set_ylabel('Number of Proverbs', fontsize=12)
        ax.set_title('Top 10 Regions by Proverb Count', fontsize=14, fontweight='bold', pad=15)
        plt.xticks(rotation=90, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        
        st.markdown("**Detailed Rankings:**")
        for i, (region, count) in enumerate(sorted_regions[:10], start=1):
            st.write(f"{i}. {region}: {count} proverbs")
    else:
        st.info("No data yet.")
