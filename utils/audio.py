import pyttsx3

def speak_text(text, lang_code):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print("TTS error:", e)
