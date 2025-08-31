import streamlit as st
import random
import base64
import requests
from utils import core, translate, vote, audio, language

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
    st.session_state.auth_mode = "login"   # login | signup | reset_password | change_password

# ✅ Centralized API base URL
API_BASE_URL = "https://api.corpus.swecha.org/api/v1/auth"

# ========== Background (UNCHANGED) ==========
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_background("Background.jpg")

# ========== ADDITIONAL LOGIN CARD STYLES ==========
st.markdown("""
<style>
.login-card {
    background: #fff;
    border-radius: 20px;
    box-shadow: 0 8px 40px 0 rgba(25, 62, 152, 0.10);
    max-width: 380px;
    padding: 39px 32px 25px 32px;
    margin: 54px auto;
    display: flex;
    flex-direction: column;
}
.login-title {
    font-weight: 700;
    font-size: 2.1rem;
    text-align: center;
    color: #111;
    margin-bottom: 1.10rem;
}
.tab-group {
    display: flex;
    width: 100%;
    margin-bottom: 1.2rem;
}
.tab-btn {
    flex: 1;
    padding: 0.6rem 0;
    border-radius: 10px 10px 10px 10px;
    border: none;
    background: #eee;
    font-size: 1.07rem;
    color: #193E98;
    font-weight: 600;
    cursor: pointer;
    transition: background 0.17s, color 0.15s;
    outline: none;
}
.tab-btn.active {
    background: linear-gradient(90deg, #1948CB 60%, #176DF7 100%);
    color: #fff;
}
.stTextInput > div > div > input, input[type="text"], input[type="password"], input[type="email"] {
    border-radius: 10px !important;
    border: 1.5px solid #e0e6ef !important;
    background: #f4f7fa !important;
    padding: 0.87rem 1.1rem !important;
    font-size: 1.07rem !important;
    color: #162447 !important;
    margin-bottom: 1.05rem !important;
}
.stButton > button {
    border-radius: 10px !important;
    padding: 0.84rem 0 !important;
    width: 100% !important;
    background: linear-gradient(90deg, #1948CB 60%, #176DF7 100%) !important;
    color: #fff !important;
    font-size: 1.13rem !important;
    font-weight: 700 !important;
    border: none !important;
    margin-top: 0.35rem !important;
    box-shadow: 0 2px 20px 0 rgba(25, 62, 152, 0.09);
    transition: background 0.2s;
}
.forgot-link {
    font-size: 0.97rem;
    color: #307aff;
    text-decoration: none;
    margin-bottom: 1.2rem;
    margin-top: -0.8rem;
    display: inline-block;
    cursor: pointer;
    font-weight: 500;
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
@media (max-width: 600px) {
    .login-card {
        width: 96vw;
        min-width: 0;
        padding: 21px 3vw 12px 3vw;
        margin-top: 6vw;
    }
}
</style>
""", unsafe_allow_html=True)

# ========== Authentication ==========
if not st.session_state.authenticated:
    st.markdown('<div style="display:flex;flex-direction:column;align-items:center;justify-content:center;min-height:92vh;"><div class="login-card">', unsafe_allow_html=True)

    # Tabs (visual only; adapt to your logic if needed)
    st.markdown(
        f"""
        <div class="tab-group">
            <button class="tab-btn {'active' if st.session_state.auth_mode == 'login' else ''}" onclick="window.location.reload()">Login</button>
            <button class="tab-btn {'active' if st.session_state.auth_mode == 'signup' else ''}" onclick="window.location.reload()">Signup</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Title
    if st.session_state.auth_mode == "login":
        st.markdown('<div class="login-title">Login Form</div>', unsafe_allow_html=True)
        user_input = st.text_input("📱 Phone Number", placeholder="Enter your 10-digit phone number", max_chars=10)
        if not st.session_state.otp_sent:
            if st.button("Send OTP", key="send_otp_btn"):
                if not user_input.isdigit() or len(user_input) != 10:
                    st.error("⚠️ Please enter a valid 10-digit phone number.")
                else:
                    try:
                        response = requests.post(
                            f"{API_BASE_URL}/login/send-otp",
                            json={"phone_number": user_input}
                        )
                        if response.status_code == 200:
                            st.session_state.otp_sent = True
                            st.session_state.user_identifier = user_input
                            st.success("✅ OTP sent successfully!")
                            st.rerun()
                        else:
                            try:
                                st.error(f"❌ Failed: {response.json()}")
                            except Exception:
                                st.error(f"❌ Failed: {response.text}")
                    except requests.exceptions.RequestException as e:
                        st.error(f"Error connecting to backend: {e}")
        else:
            st.info(f"📱 OTP sent to {st.session_state.user_identifier}")
            otp = st.text_input("🔢 Enter OTP", type="password", placeholder="Enter 6-digit OTP", max_chars=6)
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button("Verify & Sign In", key="verify_otp_btn"):
                    if not otp or len(otp) < 4:
                        st.error("⚠️ Please enter the 6-digit OTP you received.")
                    else:
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/login/verify-otp",
                                json={
                                    "phone_number": st.session_state.user_identifier,
                                    "otp_code": otp
                                }
                            )
                            if response.status_code == 200:
                                json_resp = {}
                                try:
                                    json_resp = response.json()
                                except Exception:
                                    pass
                                verified = json_resp.get("verified", True)
                                if verified:
                                    st.session_state.authenticated = True
                                    st.success("🎉 Login successful!")
                                    st.rerun()
                                else:
                                    st.error("❌ Invalid OTP.")
                            else:
                                try:
                                    st.error(f"❌ Failed: {response.json()}")
                                except Exception:
                                    st.error(f"❌ Failed: {response.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to backend: {e}")
            with col2:
                if st.button("↩️", key="back_btn", help="Go back"):
                    st.session_state.otp_sent = False
                    st.session_state.user_identifier = ""
                    st.rerun()

        st.markdown(
            """<div class="switch-links">
                Not a member? <a onclick="window.location.reload()">Signup now</a><br>
                <a class="forgot-link" onclick="window.location.reload()">Forgot password?</a>
            </div>""",
            unsafe_allow_html=True,
        )

    elif st.session_state.auth_mode == "signup":
        st.markdown('<div class="login-title">Signup Form</div>', unsafe_allow_html=True)
        phone = st.text_input("📱 Phone Number", placeholder="Enter your phone number")
        password = st.text_input("🔑 Create Password", type="password", placeholder="Create a secure password")
        if st.button("Create Account", key="signup_btn"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/signup/send-otp",
                    json={"phone_number": phone, "password": password}
                )
                if response.status_code == 200:
                    st.success("✅ Sign-up successful! Verify OTP sent.")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    try:
                        st.error(f"❌ Failed: {response.json()}")
                    except Exception:
                        st.error(f"❌ Failed: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to backend: {e}")
        st.markdown(
            """<div class="switch-links">
                Already a member? <a onclick="window.location.reload()">Login</a>
            </div>""",
            unsafe_allow_html=True,
        )

    elif st.session_state.auth_mode == "reset_password":
        st.markdown('<div class="login-title">Reset Password</div>', unsafe_allow_html=True)
        phone = st.text_input("📱 Phone Number", placeholder="Enter your phone number")
        new_pass = st.text_input("🔑 New Password", type="password", placeholder="Enter new password")
        if st.button("Reset Password", key="reset_btn"):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/reset-password",
                    json={"phone_number": phone, "new_password": new_pass}
                )
                if response.status_code == 200:
                    st.success("✅ Password reset successfully!")
                    st.session_state.auth_mode = "login"
                    st.rerun()
                else:
                    try:
                        st.error(f"❌ Failed: {response.json()}")
                    except Exception:
                        st.error(f"❌ Failed: {response.text}")
            except requests.exceptions.RequestException as e:
                st.error(f"Error connecting to backend: {e}")
        st.markdown(
            """<div class="switch-links">
                Remember your password? <a onclick="window.location.reload()">Login</a>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("</div></div>", unsafe_allow_html=True)
    st.stop()

# ========== MAIN APP ==========
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)
# ✅ Sidebar Navigation (Removed Translate)
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "States"])
# Page: Home
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

    # ✅ New Inline Translate Section (directly on Home page)
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
        # Show as graph
        import matplotlib.pyplot as plt
        regions = [item[0] for item in sorted_regions[:10]]
        counts = [item[1] for item in sorted_regions[:10]]
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(regions, counts, color='#0073e6')
        ax.set_xlabel('Regions')
        ax.set_ylabel('Number of Proverbs')
        ax.set_title('Top 10 Regions by Proverb Count')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()
        st.pyplot(fig)
        # Also show as list
        st.markdown("**Detailed Rankings:**")
        for i, (region, count) in enumerate(sorted_regions[:10], start=1):
            st.write(f"{i}. {region}: {count} proverbs")
    else:
        st.info("No data yet.")
