from audio_functions import say, listen
from lists import lang_codes
from translate import Translator
import random
import datetime


def get_translation(translate_object):
    if translate_object != '':
        say('Выберите язык для перевода.')
        lang_from = listen()
        try:
            lang_from_code = lang_codes[lang_from]
        except:
            say('Язык не найден')
            return
        say('На какой язык перевести?')
        lang_to = listen()
        try:
            lang_to_code = lang_codes[lang_to]
        except:
            say('Язык не найден')
            return
        translator = Translator(from_lang=lang_from_code, to_lang=lang_to_code)
        result = translator.translate(translate_object)
        print(result)
        say(result)


def play_greeting(*args):
    greeting = random.choice(["привет", "здравствуйте", "добрый день"])
    say(greeting)


def get_time(*args):
    now = datetime.datetime.now()
    now_time = f'Сейчас {now.hour} {now.minute}' 
    if len(now_time) != 12:
        say(f'Сейчас {now.hour} 0 {now.minute}')
    else:
        say(now_time)