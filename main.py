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
    st.session_state.auth_mode = "login"  # login | signup | reset_password | change_password

API_BASE_URL = "https://api.corpus.swecha.org/api/v1/auth"

def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        html, body, [class*="css"] {{
            color: #000 !important;
            font-weight: 500 !important;
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
            border-radius: 8px !important;
            padding: 0.75rem !important;
        }}
        label, .stSelectbox > div, .stTextInput > div, .stTextArea > div {{
            color: #000 !important;
            font-weight: 600 !important;
        }}
        .card {{
            background-color: #fff !important;
            padding: 2rem;
            border-radius: 12px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
            margin: auto;
            max-width: 420px;
        }}
        h2 {{
            text-align: center;
            margin-bottom: 1rem;
            color: #000 !important;
            font-weight: 700;
        }}
        .switch-links {{
            text-align: center;
            margin-top: 1rem;
        }}
        .switch-links a {{
            color: #0073e6;
            text-decoration: none;
            font-weight: 600;
            cursor: pointer;
            margin: 0 10px;
        }}
        @media (max-width: 768px) {{
            .card {{
                max-width: 95%;
                padding: 1.5rem;
                margin: 1rem auto;
            }}
            textarea, input, select {{
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

# Authentication UI block as per user request - verbatim update
if not st.session_state.authenticated:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if st.session_state.auth_mode == "login":
            st.markdown("<h2>Sign In</h2>", unsafe_allow_html=True)
            user_input = st.text_input("📱 Enter your Phone Number", max_chars=10)
            if not st.session_state.otp_sent:
                if st.button("Send OTP"):
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
                            else:
                                try:
                                    st.error(f"❌ Failed: {response.json()}")
                                except Exception:
                                    st.error(f"❌ Failed: {response.text}")
                        except requests.exceptions.RequestException as e:
                            st.error(f"Error connecting to backend: {e}")
            else:
                # Enter OTP shown after send otp
                otp = st.text_input("Enter OTP", type="password", max_chars=6)
                if st.button("Verify OTP"):
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
        elif st.session_state.auth_mode == "reset_password":
            st.markdown("<h2>Reset Password</h2>", unsafe_allow_html=True)
            phone = st.text_input("📱 Phone Number")
            new_pass = st.text_input("🔑 New Password", type="password")
            if st.button("Reset Password"):
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
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Main App
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
        if not region or region.strip() == "":
            region = "Unknown"
        region_counts[region] = region_counts.get(region, 0) + 1
    sorted_regions = sorted(region_counts.items(), key=lambda x: x[1], reverse=True)
    if sorted_regions:
        import matplotlib.pyplot as plt
        regions = [item[0] for item in sorted_regions[:10]]
        counts = [item[1] for item in sorted_regions[:10]]
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(regions, counts, color='#0073E6')  # Normal blue color
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
