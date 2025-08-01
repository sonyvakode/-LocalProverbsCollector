import speech_recognition as sr
import tempfile

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
        temp_audio.write(audio_file.read())
        temp_audio.flush()

        with sr.AudioFile(temp_audio.name) as source:
            audio_data = recognizer.record(source)
            try:
                return recognizer.recognize_google(audio_data, language="en-IN")
            except sr.UnknownValueError:
                return "Could not understand the audio."
            except sr.RequestError:
                return "Error reaching the speech recognition service."
