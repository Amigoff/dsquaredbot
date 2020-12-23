import speech_recognition as sr
import wave


r = sr.Recognizer()
def recorgnize(audio, file=True):
    if file:
        file = sr.AudioFile(audio)
        with file as source:
            audio = r.record(source)
    result = r.recognize_google(audio, language='ru-RU')
    return result
   
  