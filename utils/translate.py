from deep_translator import GoogleTranslator

def translate_text(text, target_lang):
    try:
        lang_map = {
            "Hindi": "hi",
            "Tamil": "ta",
            "Telugu": "te",
            "Kannada": "kn",
            "Malayalam": "ml",
            "Bengali": "bn",
            "Punjabi": "pa",
            "Gujarati": "gu",
            "Marathi": "mr",
            "Urdu": "ur",
            "English": "en"
        }
        lang_code = lang_map.get(target_lang, "en")
        translated = GoogleTranslator(source='auto', target=lang_code).translate(text)
        return translated
    except Exception as e:
        return f"Translation Error: {str(e)}"
