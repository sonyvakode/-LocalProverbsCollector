from deep_translator import GoogleTranslator

def translate_text(text, target_lang):
    """
    Translates the given text to the specified target language.
    """
    if not text.strip():
        return "No text provided for translation."

    try:
        translated = GoogleTranslator(source='auto', target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"⚠️ Translation error: {str(e)}"
