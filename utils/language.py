LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Tamil": "ta",
    "Telugu": "te",
    "Kannada": "kn",
    "Gujarati": "gu",
    "Marathi": "mr",
    "Bengali": "bn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Odia": "or"
}

def get_language_code(language_name):
    return LANGUAGES.get(language_name, "en")

def get_all_languages():
    return list(LANGUAGES.keys())
