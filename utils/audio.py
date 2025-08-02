import speech_recognition as sr
from pydub import AudioSegment
import tempfile

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    try:
        # Convert uploaded file to .wav using pydub
        audio = AudioSegment.from_file(audio_file)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp_wav:
            audio.export(tmp_wav.name, format="wav")
            with sr.AudioFile(tmp_wav.name) as source:
                audio_data = recognizer.record(source)
                text = recognizer.recognize_google(audio_data, language="en-IN")
                return text
    except Exception as e:
        return f"Could not transcribe audio: {e}"
