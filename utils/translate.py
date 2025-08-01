from googletrans import Translator

def translate_text(text, from_lang, to_lang):
    try:
        translator = Translator()
        result = translator.translate(text, src=from_lang, dest=to_lang)
        return result.text
    except Exception as e:
        return f"Translation error: {str(e)}"
