#!/usr/bin/env python3
# -*- coding: utf-8
import urllib
import json
import os
import platform
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
import core
import pyaudio
from nlu.classify import classify_text



def beep(freq, time):
    if platform.system() == 'Windows':
        import winsound
        time = time*1000
        winsound.Beep(freq, int(time))
    else:
        os.system('play -nq -t alsa synth {} sine {}'.format(time, freq))


def getNet():
    try:
        urllib.request.urlopen('https://google.com')  # Python 3.x
        return True
    except:
        return False


if getNet() == True:
    def Hear():
        r = sr.Recognizer()
    # usando o microfone

        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            beep(440, 0.5)
            print("Diga alguma coisa: ")
            audio = r.listen(source)
        try:
            Hear.voice = r.recognize_google(audio, language='pt-BR').lower()
            print("Você disse: " + Hear.voice)
            beep(440, 0.5)
        except sr.UnknownValueError:
            print("Não entendi")
            beep(294, 0.3)
            beep(294, 0.3)


else:
    def Hear():
        if platform.system() == 'Windows':
            model = Model(r'/model')
        else:
            model = Model(r'/model')
        # model = Model(r'/mnt/c/Users/gabri/Desktop/VoiceAssistant/model')
        recognizer = KaldiRecognizer(model, 16000)
        cap = pyaudio.PyAudio()
        stream = cap.open(format=pyaudio.paInt16, channels=1,
                          rate=16000, frames_per_buffer=8192, input=True)
        stream.start_stream()
        while True:
            data = stream.read(8000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                result = recognizer.Result()
                result = json.loads(result)
                voice = result['text']
                print(voice)
                if len(voice) == 0:
                    break
            else:
                print(recognizer.PartialResult())
Hear()
entity = classify_text(Hear.voice)
if entity == 'time\\getTime':
    core.TTS.speak(core.SysInfo.get_time())
elif entity == 'date\\getDate':
    core.TTS.speak(core.SysInfo.get_Date())
elif entity == 'weather\\getWeather':
    core.TTS.speak(core.Search.weather(Hear.voice))
elif entity == 'search\\getAnswer':
    core.TTS.speak(core.Search.search(Hear.voice))
beep(528, 0.7)
