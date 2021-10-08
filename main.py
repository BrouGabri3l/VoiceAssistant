#!/usr/bin/env python3
# -*- coding: utf-8
import argparse
import json
import queue
import sounddevice as sd
import wave
import os
import sys
import vosk
from playsound import playsound
import speech_recognition as sr
# tts
from gtts import gTTS
import playsound
import core


def speak(text):
    tts = gTTS(text=text, lang='pt-br',)
    filename = "voice.mp3"
    tts.save(filename)
    playsound.playsound(filename)


# Habilita o microfone do usuário
r = sr.Recognizer()

# usando o microfone
with sr.Microphone() as source:

    r.adjust_for_ambient_noise(source)

    print("Diga alguma coisa: ")

    audio = r.listen(source)

try:
    voice = r.recognize_google(audio, language='pt-BR').lower()
    print("Você disse: " + voice)
    if voice == 'que horas são' or voice == 'me diga as horas':
        speak(core.SysInfo.get_time())

except sr.UnkownValueError:
    print("Não entendi")
