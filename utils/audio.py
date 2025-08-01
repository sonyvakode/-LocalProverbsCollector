import speech_recognition as sr

def transcribe_audio(file):
    try:
        recognizer = sr.Recognizer()
        with sr.AudioFile(file) as source:
            audio = recognizer.record(source)
        return recognizer.recognize_google(audio)
    except Exception as e:
        return f"Transcription error: {str(e)}"
