import pyttsx3
import time
import speech_recognition as sr
from enum import Enum

engine = pyttsx3.init()
'''
voices = engine.getProperty('voices')
for voice in voices:
    print("Voice:")
    print(" - ID: %s" % voice.id)
    print(" - Name: %s" % voice.name)
    print(" - Languages: %s" % voice.languages)
    print(" - Gender: %s" % voice.gender)
    print(" - Age: %s" % voice.age)'''

es_voice_id = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
engine.setProperty('voice', es_voice_id)
engine.setProperty('rate', 95) 

class Language(Enum):
    ENGLISH = "en-US"
    SPANISH_SPAIN = "es-ES"


class SpeechToText():
    def print_mic_device_index():
        for index, name in enumerate(sr.Microphone.list_microphone_names()):
            print("{1}, device_index={0}".format(index,name))
    
    def speech_to_text(device_index, language=Language.ENGLISH):
        r = sr.Recognizer()
        with sr.Microphone(device_index=device_index) as source:
            print("Start Talking:")
            audio = r.listen(source)
            try:
                text = r.recognize_google(audio,language=language.value)
                print("You said: {}".format(text))
                if text == 'hola':
                    print("Well done")
                else:
                    print("Try again")
            except:
                print("Please try again.")

def check_mic_device_index():
    SpeechToText.print_mic_device_index()

def run_speech_to_text_english(device_index):
    SpeechToText.speech_to_text(device_index)

def run_speech_to_text_spanish(device_index, language):
    SpeechToText.speech_to_text(device_index, language)

if __name__ == '__main__':
    #check_mic_device_index() index is 1 for microphone 
    #run_speech_to_text_english(device_index=1)
    #Spanish voice
    print("Can you repeat this word?")
    time.sleep(1.5)
    engine.say('Hola')
    engine.runAndWait()
    time.sleep(2)
    run_speech_to_text_spanish(device_index=1, language=Language.SPANISH_SPAIN)

