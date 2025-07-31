# utils/language.py

def get_supported_languages():
    """
    Returns a list of supported languages for the app.
    These should match gTTS and GoogleTranslator language codes.
    """
    return [
        "en",  # English
        "hi",  # Hindi
        "ta",  # Tamil
        "te",  # Telugu
        "ml",  # Malayalam
        "kn",  # Kannada
        "gu",  # Gujarati
        "mr",  # Marathi
        "bn",  # Bengali
        "pa",  # Punjabi
        "ur",  # Urdu
    ]
