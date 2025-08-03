import speech_recognition as sr

def transcribe_audio(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio_data = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio_data, language="en-IN")
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError:
        return "Speech Recognition service is not available."
