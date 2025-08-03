from deep_translator import GoogleTranslator

# Only include supported Indian languages
indian_languages = {
    "Hindi": "hi",
    "Bengali": "bn",
    "Telugu": "te",
    "Marathi": "mr",
    "Tamil": "ta",
    "Urdu": "ur",
    "Gujarati": "gu",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Punjabi": "pa",
    "Assamese": "as",
    "Odia": "or",
    "Sanskrit": "sa",
    "Maithili": "mai",
    "Konkani": "gom",
    "Manipuri": "mni-Mtei",
    "Mizo": "lus",
}

def get_all_languages():
    return list(indian_languages.keys())

def translate_proverb(proverb, target_lang):
    try:
        if target_lang not in indian_languages:
            return f"Translation failed: Unsupported language '{target_lang}'"
        lang_code = indian_languages[target_lang]
        translated = GoogleTranslator(source='auto', target=lang_code).translate(proverb)
        return translated
    except Exception as e:
        return f"Translation failed: {e}"
