from deep_translator import GoogleTranslator

def translate_proverb(text, source_lang, target_lang="en"):
    try:
        translated = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        return translated
    except Exception as e:
        return f"Translation error: {str(e)}"
