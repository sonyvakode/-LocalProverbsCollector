from deep_translator import GoogleTranslator

def translate_proverb(text, lang_code):
    try:
        return GoogleTranslator(source='auto', target=lang_code).translate(text)
    except Exception as e:
        return f"Error: {e}"
