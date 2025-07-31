import streamlit as st

# Sidebar - Theme Selection
st.sidebar.markdown("### 🎨 Choose Mode")
theme = st.sidebar.radio("Choose Theme", ["Light", "Dark", "Colorful"], index=0)

# Apply CSS Styles Based on Theme
def set_theme_css(selected):
    if selected == "Light":
        css = """
        <style>
        .stApp {
            background: linear-gradient(to right, #e3ffe7, #d9e7ff);
            color: black;
        }
        </style>
        """
    elif selected == "Dark":
        css = """
        <style>
        .stApp {
            background: linear-gradient(to right, #0f2027, #203a43, #2c5364);
            color: white;
        }
        </style>
        """
    elif selected == "Colorful":
        css = """
        <style>
        .stApp {
            background: linear-gradient(to right, #ff9a9e, #fad0c4, #fad0c4);
            color: #222;
        }
        </style>
        """
    st.markdown(css, unsafe_allow_html=True)

# Apply the selected theme
set_theme_css(theme)

# Navigation (just placeholder)
st.sidebar.markdown("### Go to")
nav = st.sidebar.radio("Go to", ["Submit", "Translate", "Stats", "Proverb of the Day", "Settings"])

# Main App Title
st.markdown("## 🍂 Indian Wisdom: Local Proverbs Collector")
st.markdown("### 📝 Submit a Local Proverb")

# Proverb input
st.text_area("Type the proverb in your language")

# Optional audio upload
st.markdown("#### Or upload an audio file (WAV/MP3)")
st.file_uploader("Drag and drop file here", type=["mp3", "wav"])

