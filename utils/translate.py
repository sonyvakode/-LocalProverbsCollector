from deep_translator import GoogleTranslator
from .language import LANGUAGE_NAMES_TO_CODES

def translate_text(text, target_lang):
    try:
        lang_code = LANGUAGE_NAMES_TO_CODES.get(target_lang.lower(), "en")
        translated = GoogleTranslator(target=lang_code).translate(text)
        return translated
    except Exception as e:
        return f"⚠️ Translation error: {str(e)}"
