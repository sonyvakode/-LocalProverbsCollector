from deep_translator import GoogleTranslator

def translate_proverb(text, src_lang, target_lang):
    try:
        if not text:
            return "No proverb provided."

        # Normalize input
        src_lang = src_lang.lower().strip()
        target_lang = target_lang.lower().strip()

        # Prevent translation if source and target languages are same
        if src_lang == target_lang:
            return "Cannot translate to the same language."

        # Supported languages list from GoogleTranslator
        supported_langs = GoogleTranslator.get_supported_languages(as_dict=True)

        # Convert names to codes if needed
        src_code = supported_langs.get(src_lang, src_lang)
        target_code = supported_langs.get(target_lang, target_lang)

        # Validate supported codes
        if src_code not in supported_langs.values() or target_code not in supported_langs.values():
            return f"Translation failed: Unsupported language '{target_lang}'. Please choose a supported language."

        translated = GoogleTranslator(source=src_code, target=target_code).translate(text)
        return translated

    except Exception as e:
        return f"Translation failed: {str(e)}"
