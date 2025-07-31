# utils/translate.py

# Language map: language name -> ISO code
LANGUAGE_MAP = {
    "Hindi": "hi", "Telugu": "te", "Tamil": "ta", "Kannada": "kn", "Bengali": "bn",
    "Marathi": "mr", "Malayalam": "ml", "Gujarati": "gu", "Punjabi": "pa", "Urdu": "ur",
    "Assamese": "as", "Odia": "or", "Sanskrit": "sa", "English": "en", "Arabic": "ar",
    "French": "fr", "Spanish": "es", "German": "de", "Chinese": "zh-CN", "Japanese": "ja",
    "Russian": "ru", "Korean": "ko", "Portuguese": "pt", "Italian": "it", "Turkish": "tr"
}

def translate_text(text, target_lang_code):
    """
    Simulates translation by mocking the translated output.

    Parameters:
    - text (str): The input proverb or sentence
    - target_lang_code (str): Target language code (e.g. 'hi', 'te')

    Returns:
    - str: Simulated translated text
    """
    if not text:
        return "⚠️ No input provided."

    return f"🔁 Translated '{text}' to [{target_lang_code.upper()}] (mock translation)"

# Optional: helper to get language code from name
def get_lang_code(language_name):
    return LANGUAGE_MAP.get(language_name, "en")
