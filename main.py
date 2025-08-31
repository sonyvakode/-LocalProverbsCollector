import streamlit as st
import random
import base64
import requests
from utils import core, translate, vote, audio, language

# ========== Page setup ==========
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

# ========== Background and Login UI Styling ==========
def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()
    st.markdown(
        f"""
        <style>
        body {{
            background: none !important;
        }}
        .stApp {{
            background: radial-gradient(circle at 65% 36%, #176DF7 0%, #1556C1 100%) !important;
            min-height: 100vh !important;
            font-family: 'Segoe UI', Arial, sans-serif !important;
        }}
        .centered-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 98vh;
            justify-content: center;
        }}
        .login-card {{
            background: #fff;
            border-radius: 18px;
            box-shadow: 0 8px 40px 0 rgba(25, 62, 152, 0.08);
            width: 370px;
            max-width: 96vw;
            padding: 38px 32px 30px 32px;
            margin: 44px auto;
            display: flex;
            flex-direction: column;
        }}
        .login-title, .form-title {{
            font-weight: 700;
            font-size: 2.1rem;
            text-align: center;
            color: #111;
            margin-bottom: 1.25rem;
        }}
        .tab-group, .auth-methods {{
            display: flex;
            gap: 0;
            margin-bottom: 1.55rem;
            margin-top: 0.5rem;
            width: 100%;
        }}
        .tab-btn, .method-btn {{
            flex: 1;
            padding: 0.7rem 0;
            border-radius: 9px 9px 9px 9px;
            border: none;
            background: #eee;
            font-size: 1.09rem;
            color: #193E98;
            font-weight: 600;
            cursor: pointer;
            transition: background 0.2s, color 0.2s;
            outline: none;
        }}
        .tab-btn.active, .method-btn.active {{
            background: linear-gradient(90deg, #1948CB 60%, #176DF7 100%);
            color: #fff;
        }}
        .stTextInput > div > div > input, input[type="text"], input[type="password"], input[type="email"] {{
            border-radius: 10px !important;
            border: 1.5px solid #e0e6ef !important;
            background: #f4f7fa !important;
            padding: 0.90rem 1.05rem !important;
            font-size: 1.09rem !important;
            color: #162447 !important;
            margin-bottom: 1.1rem !important;
        }}
        .stTextInput label {{
            font-size: 1.08rem !important;
            font-weight: 500 !important;
            margin-bottom: 0.46rem !important;
        }}
        .stButton > button {{
            border-radius: 10px !important;
            padding: 0.89rem 0 !important;
            width: 100% !important;
            background: linear-gradient(90deg, #1948CB 60%, #176DF7 100%) !important;
            color: #fff !important;
            font-size: 1.14rem !important;
            font-weight: 700 !important;
            border: none !important;
            margin-top: 0.45rem !important;
            margin-bottom: 0.8rem !important;
            box-shadow: 0 2px 20px 0 rgba(25, 62, 152, 0.09);
            transition: background 0.2s;
        }}
        .forgot-link {{
            font-size: 0.99rem;
            color: #307aff;
            text-decoration: none;
            margin-bottom: 1.4rem;
            margin-top: -0.9rem;
            display: inline-block;
            cursor: pointer;
            font-weight: 500;
        }}
        .switch-links {{
            text-align: center;
            margin-top: 17px;
            font-size: 1.02rem;
        }}
        .switch-links a {{
            color: #307aff;
            font-weight: 500;
            text-decoration: none;
            cursor: pointer;
        }}
        @media (max-width: 600px) {{
            .login-card {{
                width: 99vw;
                min-width: 0;
                padding: 24px 4vw 22px 4vw;
                margin-top: 10vw;
            }}
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
set_background("Background.jpg")

# ========== Authentication ==========
if not st.session_state.authenticated:
    st.markdown('<div class="centered-container"><div class="login-card">', unsafe_allow_html=True)
    # Tab UI for login/signup (optional, you can use your own method)
    st.markdown(
        f"""
        <div class="tab-group">
            <button class="tab-btn {'active' if st.session_state.auth_mode == 'login' else ''}" onclick="window.location.reload()">Login</button>
            <button class="tab-btn {'active' if st.session_state.auth_mode == 'signup' else ''}" onclick="window.location.reload()">Signup</button>
        </div>
        """,
        unsafe_allow_html=True
    )

    if st.session_state.auth_mode == "login":
        st.markdown('<div class="login-title">Login Form</div>', unsafe_allow_html=True)
        user_input = st.text_input("Email Address", placeholder="Email Address", key="login_email", label_visibility="collapsed")
        password = st.text_input("Password", placeholder="Password", type="password", key="login_password", label_visibility="collapsed")
        st.markdown('<a class="forgot-link">Forgot password?</a>', unsafe_allow_html=True)
        login_btn = st.button("Login", key="login_btn")
        if login_btn:
            # Call your authentication logic here
            st.success("Login pressed. (Your backend logic here)")
        st.markdown('<div class="switch-links">Not a member? <a onclick="window.location.reload()">Signup now</a></div>', unsafe_allow_html=True)

    elif st.session_state.auth_mode == "signup":
        st.markdown('<div class="login-title">Signup Form</div>', unsafe_allow_html=True)
        user_input = st.text_input("Email Address", placeholder="Email Address", key="signup_email", label_visibility="collapsed")
        password = st.text_input("Password", placeholder="Password", type="password", key="signup_password", label_visibility="collapsed")
        signup_btn = st.button("Signup", key="signup_btn")
        if signup_btn:
            # Call your signup logic here
            st.success("Signup pressed. (Your backend logic here)")
        st.markdown('<div class="switch-links">Already a member? <a onclick="window.location.reload()">Login</a></div>', unsafe_allow_html=True)
    st.markdown('</div></div>', unsafe_allow_html=True)
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
        regions = [item for item in sorted_regions[:10]]
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
