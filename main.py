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
            background: linear-gradient(rgba(255,255,255,0.95), rgba(255,255,255,0.95)),
                        url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            font-family: 'Segoe UI', sans-serif;
            color: black !important;
        }}
        h1, h2, h3, p {{
            color: black !important;
        }}
        .auth-title {{
            text-align: center;
            font-size: 48px;
            font-weight: bold;
            background-color: #D2B48C;  /* Light brown */
            padding: 1rem 0.5rem;
            border-radius: 12px;
            margin-bottom: 2rem;
            color: black !important;
        }}
        .stTextInput > div > div > input {{
            border-radius: 8px !important;
            border: 1px solid #ddd !important;
            padding: 0.75rem !important;
            color: black !important;
        }}
        .stButton > button {{
            background-color: #555 !important;
            color: white !important;
            border: none !important;
            border-radius: 8px !important;
            padding: 0.75rem 2rem !important;
            font-weight: 600 !important;
            width: 100% !important;
        }}
        .switch-links {{
            text-align: center;
            margin-top: 1rem;
        }}
        .switch-links a {{
            color: #000;
            text-decoration: none;
            font-weight: 500;
            cursor: pointer;
            margin: 0 10px;
        }}
        @media (max-width: 768px) {{
            .auth-title {{
                font-size: 36px;
                padding: 0.75rem 0.5rem;
            }}
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

# ========== Authentication ==========
if not st.session_state.authenticated:

    # Centered Welcome Back
    if st.session_state.auth_mode == "login":
        st.markdown('<div class="auth-title">Welcome Back!</div>', unsafe_allow_html=True)
    elif st.session_state.auth_mode == "signup":
        st.markdown('<div class="auth-title">Create Account</div>', unsafe_allow_html=True)
    elif st.session_state.auth_mode == "reset_password":
        st.markdown('<div class="auth-title">Reset Password</div>', unsafe_allow_html=True)

    # Login Form
    if st.session_state.auth_mode == "login":
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

    # Signup Form
    elif st.session_state.auth_mode == "signup":
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

    # Reset Password Form
    elif st.session_state.auth_mode == "reset_password":
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
    st.stop()

# ========== MAIN APP ==========
st.markdown(
    "<h1 style='text-align: center; color: black;'>📜 Indian Wisdom: Local Proverbs Collector</h1>",
    unsafe_allow_html=True
)

# ✅ Sidebar Navigation
page = st.sidebar.selectbox("Navigate", ["Home", "Proverb of the day", "States"])

# Page content remains the same as before...
