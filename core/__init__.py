import datetime
from gtts import gTTS
import platform
from bs4 import BeautifulSoup
import requests
from urllib.request import Request, urlopen


class TTS:
    def __init__():
        pass

    @staticmethod
    def speak(text):
        tts = gTTS(text=text, lang='pt-br')
        filename = "core\\voice.mp3"
        print(filename)
        tts.save(filename)
        if platform.system() == 'Windows':
            import playsound
            playsound.playsound(filename)

        else:        
            from pydub import AudioSegment
            from pydub.playback import play
            audio = AudioSegment.from_mp3(filename)
            play(audio)

class SysInfo:
    def __init__():
        pass

    @staticmethod
    def get_time():

        now = datetime.datetime.now()
        answer = 'São {} horas e {} minutos'.format(now.hour, now.minute)
        return answer

    def get_Date():
        now = datetime.datetime.now()
        answer = 'Hoje é dia {} de {} de {}'.format(
            now.day, now.month, now.year)
        return answer


class Search:
    def __init__():
        pass

    @staticmethod
    def search(quest):

        Queue = 'https://www.google.com/search?q=' + quest
        url = Queue.replace(" ", "%20")
        req = Request(
            url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'})
        print(url)
        page = urlopen(req).read()
        soup = BeautifulSoup(page, 'lxml')
        infoList = soup.find(
            "div", {"data-attrid": "kc:/people/person:age"})
        children = infoList.findChildren()
        age = children[1].get_text()
        print(age)
        return age

    @staticmethod
    def weather(text):
        frase = text.title()
        exwords = ['qual', 'em', 'no', 'na', 'a', 'atual',
                   'temperatura', 'clima', 'cidade', 'regiao']
        red = [s.lower()
               for s in frase.split() if s.lower() not in exwords]
        city = ' '.join(red)
        print(city)
        BASE = 'http://api.openweathermap.org/data/2.5/weather?'
        URL = BASE + 'q='+city + '&units=metric&appid=4f0318954fded0ded8dcd167e435ffe7&lang=pt_br'
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            main = data['main']
            temperatura = main['temp']
            temp_str = 'a Temperatura atual em {} é de {} graus celsius'.format(
                city, str(round(temperatura)))
        return temp_str
