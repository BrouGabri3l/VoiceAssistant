#!/usr/bin/env python3
# -*- coding: utf-8
import argparse
import json
import queue
import wave
import os
import platform
import sys
from vosk import Model, KaldiRecognizer, SetLogLevel
import speech_recognition as sr
from gtts import gTTS
import core
import pyaudio
# model = Model(r'C:/Users/gabri/Desktop/VoiceAssistant/model')
model = Model(r'/home/pi/Desktop/VoiceAssistant/model')
# model = Model(r'/mnt/c/Users/gabri/Desktop/VoiceAssistant/model')
recognizer = KaldiRecognizer(model, 16000)
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1,
                  rate=16000, frames_per_buffer=8192, input=True)
stream.start_stream()


def speak(text):
    tts = gTTS(text=text, lang='pt-br',)
    filename = "voice.mp3"
    tts.save(filename)
    if platform.system() == 'Windows':
        import playsound
        playsound.playsound(filename)
    else:
        from pydub import AudioSegment
        from pydub.playback import play
        audio = AudioSegment.from_mp3(filename)
        play(audio)


while True:
    data = stream.read(8000)
    if len(data) == 0:
        break
    if recognizer.AcceptWaveform(data):
        result = recognizer.Result()
        result = json.loads(result)
        print(result['text'])
        if len(result['text']) == 0:
            break
    else:
        print(recognizer.PartialResult())


# def getNet():
#     pass


# # Habilita o microfone do usuário
# r = sr.Recognizer()
# # usando o microfone
# with sr.Microphone() as source:
#     r.adjust_for_ambient_noise(source)
#     print("Diga alguma coisa: ")
#     audio = r.listen(source)
# try:
#     # voice = r.recognize_sphinx(audio, language='pt-br').lower()
#     voice = r.recognize_google(audio, language='pt-BR').lower()
#     print("Você disse: " + voice)
#     if voice == 'que horas são' or voice == 'me diga as horas':
#         speak(core.SysInfo.get_time())
#     if voice == 'qual o sistema':
#         speak(platform.system())
# except sr.UnknownValueError:
#     print("Não entendi")
