import streamlit as st
import random

# Page setup
st.set_page_config(page_title="Auth System", page_icon="🔑", layout="centered")

# In-memory OTP storage (for demo purpose)
otp_storage = {}

# Dark theme styling
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: white;
    }
    .stTabs [data-baseweb="tab-list"] {
        justify-content: center;
    }
    .stTextInput>div>div>input {
        background-color: #1E222A;
        color: white;
    }
    .stPasswordInput>div>div>input {
        background-color: #1E222A;
        color: white;
    }
    .stSelectbox>div>div>select {
        background-color: #1E222A;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Tabs: Sign In / Sign Up
tab1, tab2 = st.tabs(["🔑 Sign In", "📝 Sign Up"])

with tab1:
    st.title("Sign In")

    auth_method = st.radio("Choose login method:", ["Password", "OTP"], horizontal=True)

    phone = st.text_input("Phone Number", placeholder="Enter your phone number")

    if auth_method == "Password":
        password = st.text_input("Password", type="password", placeholder="Enter your password")
        if st.button("Sign In"):
            if phone and password:
                st.success(f"✅ Signed in with phone {phone}")
            else:
                st.error("⚠️ Please fill in all fields.")
    else:
        if st.button("Send OTP"):
            if phone:
                otp = str(random.randint(100000, 999999))
                otp_storage[phone] = otp
                st.info(f"📩 OTP sent to {phone} (Demo: {otp})")  # For demo, showing OTP
            else:
                st.error("⚠️ Please enter phone number.")

        otp = st.text_input("Enter OTP", placeholder="Enter OTP here")
        if st.button("Verify OTP"):
            if phone in otp_storage and otp_storage[phone] == otp:
                st.success("✅ OTP verified, signed in!")
                del otp_storage[phone]
            else:
                st.error("❌ Invalid OTP.")

with tab2:
    st.title("Sign Up")

    new_phone = st.text_input("Phone Number", placeholder="Enter your phone number")
    new_password = st.text_input("Password", type="password", placeholder="Create a password")
    confirm_password = st.text_input("Confirm Password", type="password", placeholder="Re-enter password")

    if st.button("Register"):
        if new_phone and new_password and confirm_password:
            if new_password == confirm_password:
                st.success(f"🎉 Account created for {new_phone}")
            else:
                st.error("⚠️ Passwords do not match.")
        else:
            st.error("⚠️ Please fill in all fields.")
