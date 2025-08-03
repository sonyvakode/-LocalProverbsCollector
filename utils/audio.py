import speech_recognition as sr
import io

def transcribe_audio(uploaded_file):
    recognizer = sr.Recognizer()

    # Read file as bytes and wrap in BytesIO
    audio_bytes = uploaded_file.read()
    audio_file = io.BytesIO(audio_bytes)

    try:
        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            return text
    except Exception as e:
        return f"Transcription failed: {e}"
