from deep_translator import GoogleTranslator

def translate_text(text, target_lang):
    try:
        translated = GoogleTranslator(target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {e}"
