from deep_translator import GoogleTranslator

# Define supported languages (lowercase)
SUPPORTED_LANGUAGES = GoogleTranslator.get_supported_languages(as_dict=True)

def translate_text(text, target_language):
    try:
        # Normalize target language name (e.g., "English" → "english")
        target_language = target_language.strip().lower()

        if target_language not in SUPPORTED_LANGUAGES:
            return f"Translation failed: '{target_language}' not supported. Choose from: {list(SUPPORTED_LANGUAGES.keys())}"

        return GoogleTranslator(source='auto', target=target_language).translate(text)

    except Exception as e:
        return f"Translation failed: {str(e)}"
