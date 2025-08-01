from googletrans import Translator

translator = Translator()

def translate(text, dest_lang="hi"):
    try:
        translated = translator.translate(text, dest=dest_lang)
        return translated.text
    except Exception as e:
        return "Translation failed."
