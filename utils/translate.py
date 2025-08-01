def translate_proverb(proverb, target_language):
    translations = {
        "Hindi": "यह एक उदाहरण है",
        "Tamil": "இது ஒரு எடுத்துக்காட்டு ஆகும்",
        "Telugu": "ఇది ఒక ఉదాహరణ",
        "Kannada": "ಇದು ಒಂದು ಉದಾಹರಣೆ",
        "Bengali": "এটি একটি উদাহরণ",
    }
    return translations.get(target_language, proverb)
