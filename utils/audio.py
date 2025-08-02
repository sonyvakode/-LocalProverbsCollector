import speech_recognition as sr
from pydub import AudioSegment
import tempfile

def transcribe_audio(file):
    recognizer = sr.Recognizer()
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_wav:
            audio = AudioSegment.from_file(file)
            audio.export(temp_wav.name, format="wav")
            with sr.AudioFile(temp_wav.name) as source:
                audio_data = recognizer.record(source)
                return recognizer.recognize_google(audio_data)
    except Exception as e:
        return f"Error: {e}"
