def translate_proverb(text, target_lang="hi"):
    # Dummy translation
    translations = {
        "Love conquers all": "प्यार सब पर भारी होता है",
        "An apple a day": "रोज़ एक सेब डॉक्टर से दूर रखता है"
    }
    return translations.get(text, text)
