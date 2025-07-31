def mock_translate(text, lang_code):
    return f"[{lang_code}] {text[::-1]}"  # Just reverse the string as a mock
