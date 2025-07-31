from deep_translator import GoogleTranslator

def translate_proverb(text, src, target):
    try:
        return GoogleTranslator(source=src, target=target).translate(text)
    except Exception as e:
        return f"Translation failed: {e}"
