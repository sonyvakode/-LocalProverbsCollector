from deep_translator import GoogleTranslator

def translate(text, target_lang):
    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Translation failed: {e}"
