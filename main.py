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

# ========== Background ==========
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            min-height: 100vh;
        }}
        
        .main-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            padding: 20px;
        }}
        
        .auth-card {{
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            padding: 3rem 2.5rem;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            margin: auto;
            max-width: 450px;
            width: 100%;
            border: 1px solid rgba(255,255,255,0.2);
        }}
        
        .app-title {{
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            color: #2d3748;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }}
        
        .app-subtitle {{
            text-align: center;
            color: #666;
            margin-bottom: 2rem;
            font-size: 0.95rem;
        }}
        
        .form-title {{
            text-align: center;
            margin-bottom: 2rem;
            color: #2d3748;
            font-size: 1.5rem;
            font-weight: 600;
        }}
        
        .stTextInput > div > div > input {{
            border-radius: 12px !important;
            border: 2px solid #e2e8f0 !important;
            padding: 0.75rem 1rem !important;
            font-size: 1rem !important;
            transition: all 0.3s ease !important;
        }}
        
        .stTextInput > div > div > input:focus {{
            border-color: #667eea !important;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
        }}
        
        .stButton > button {{
            background: linear-gradient(135deg, #667eea, #764ba2) !important;
            color: white !important;
            border: none !important;
            border-radius: 12px !important;
            padding: 0.75rem 2rem !important;
            font-size: 1rem !important;
            font-weight: 600 !important;
            width: 100% !important;
            transition: all 0.3s ease !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3) !important;
        }}
        
        .switch-links {{
            text-align: center;
            margin-top: 1.5rem;
            padding-top: 1rem;
            border-top: 1px solid #e2e8f0;
        }}
        
        .switch-links a {{
            color: #667eea;
            text-decoration: none;
            font-weight: 500;
            cursor: pointer;
            margin: 0 10px;
            transition: color 0.3s ease;
        }}
        
        .switch-links a:hover {{
            color: #764ba2;
        }}
        
        .success-message {{
            background: linear-gradient(135deg, #48bb78, #38a169);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
        }}
        
        .error-message {{
            background: linear-gradient(135deg, #f56565, #e53e3e);
            color: white;
            padding: 1rem;
            border-radius: 12px;
            text-align: center;
            margin: 1rem 0;
        }}
        
        .input-label {{
            font-weight: 600;
            color: #2d3748;
            margin-bottom: 0.5rem;
            font-size: 0.95rem;
        }}
        
        /* Hide default streamlit styling */
        .stTextInput > label {{
            font-weight: 600 !important;
            color: #2d3748 !important;
            font-size: 0.95rem !important;
        }}
        
        /* Responsive design */
        @media (max-width: 768px) {{
            .auth-card {{
                padding: 2rem 1.5rem;
                margin: 1rem;
            }}
            .app-title {{
                font-size: 1.75rem;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_background("Background.jpg")

# ========== Authentication ==========
if not st.session_state.authenticated:

    st.markdown("<div class='main-container'>", unsafe_allow_html=True)
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    
    # App branding
    st.markdown("<div class='app-title'>📜 Indian Wisdom</div>", unsafe_allow_html=True)
    st.markdown("<div class='app-subtitle'>Preserving Local Proverbs & Cultural Heritage</div>", unsafe_allow_html=True)

    if st.session_state.auth_mode == "login":
        st.markdown("<div class='form-title'>Welcome Back!</div>", unsafe_allow_html=True)

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
                Don't have an account? <a onclick="window.location.reload()">Sign Up</a><br>
                <a onclick="window.location.reload()">Forgot Password?</a>
            </div>""",
            unsafe_allow_html=True,
        )

    elif st.session_state.auth_mode == "signup":
        st.markdown("<div class='form-title'>Create Account</div>", unsafe_allow_html=True)
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
                Already have an account? <a onclick="window.location.reload()">Sign In</a>
            </div>""",
            unsafe_allow_html=True,
        )

    elif st.session_state.auth_mode == "reset_password":
        st.markdown("<div class='form-title'>Reset Password</div>", unsafe_allow_html=True)
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
                Remember your password? <a onclick="window.location.reload()">Sign In</a>
            </div>""",
            unsafe_allow_html=True,
        )

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
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
        for i, (region, count) in enumerate(sorted_regions[:10], start=1):
            st.write(f"{i}. {region}: {count} proverbs")
    else:
        st.info("No data yet.")
