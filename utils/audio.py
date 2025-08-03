# utils/audio.py

import speech_recognition as sr

def transcribe_audio(file):
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-IN")
            return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Error connecting to the speech recognition service."
    except Exception as e:
        return f"Error processing audio: {str(e)}"
