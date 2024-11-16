import speech_recognition
import pyttsx3
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from translate import Translator
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import datetime
from word2number.w2n import word_to_num
import time
import random
import re


options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('log-level=3')
options.page_load_strategy='eager'
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)
browser.get('https://ya.ru')
recognizer = speech_recognition.Recognizer()
recognizer.pause_threshold = 1



def refresh(*args):
    say('перезагружаю страницу')
    browser.get(browser.current_url)


def add_new_tab(*args):
    say('добавил новую вкладку')
    tabs = browser.window_handles
    browser.switch_to.window(tabs[-1])
    browser.execute_script("window.open('https://www.google.com')")
    tabs = browser.window_handles
    browser.switch_to.window(tabs[-1])


def window_switch_to(tab):
    tabs = browser.window_handles
    try:
        translator = Translator(from_lang='ru', to_lang='en')
        result = translator.translate(tab)
        number = word_to_num(result)
    except ValueError:
        number = int(numbers[tab])
    try:
        browser.switch_to.window(tabs[number - 1])
    except IndexError:
        say('Вкладка не найдена')
        return
    say('вкладка переключена')
    


def click_to(text):
    links = browser.find_elements('xpath', f'//a//*[text()="{text}"]/parent::a') + browser.find_elements('xpath', f'//a[text()="{text}"]')
    buttons = browser.find_elements('xpath', f'//button//*[text()="{text}"]/parent::button') + browser.find_elements('xpath', f'//button[text()="{text}"]')
    elements = links + buttons
    if len(elements) == 0:
        say('Такой элемент не найден или он не является кликабельным')
    elif len(elements) > 1:
        say('Подходящих элементов несколько, выберите номер нужного элемента')
        number = int(input())
        elements[number - 1].click()
    else:
        browser.elements[0].click()


def read_text(*args):
    global now_el
    all_text = browser.find_element('xpath', "/html/body").text
    print(all_text.replace('\n', ' '))
    sentences = re.split('\. |\? |\! ', all_text)
    # for i in range(sentence_max):
    #     say(sentences[now_el + i])
    # say('Продолжить?')
    # answer = listen()
    # if answer in ['продолжи', 'да', 'продолжай']:
    #     now_el += sentence_max
    # elif answer in ['нет', 'не надо', 'не', 'не продолжай']:
    #     now_el = 0
    # else:
    #     say('Ответ не распознан')
    
    # print(browser.find_element('xpath', "/html/body").text)


def listen(mic):
    while True:
        recognizer.adjust_for_ambient_noise(mic)
        try:
            audio = recognizer.listen(mic)
            command = recognizer.recognize_google(audio, language="ru").lower()
            print(command)
            return command
        except speech_recognition.UnknownValueError: 
            continue


def find(target):
    say('ищу ваш запрос')
    browser.get('https://www.google.ru')
    find_field = browser.find_element('class name', 'gLFyf')
    find_field.send_keys(target)
    find_field.send_keys(Keys.ENTER)


def choose_link(target):
    try:
        translator = Translator(from_lang='ru', to_lang='en')
        result = translator.translate(target)
        number = word_to_num(result)
    except ValueError:
        number = int(numbers[target])
    if 'https://www.google.ru/search?' in browser.current_url:
        links = browser.find_elements('xpath', '//a[@jsname="UWckNb"]')
        links2 = []
        for el in links:
            if el.is_displayed() and el.is_enabled():
                links2.append(el)
        links2[number - 1].click()
        say('ссылка открыта')
    elif 'https://yandex.ru/search' in browser.current_url or 'https://ya.ru/search' in browser.current_url:
        try:
            links = browser.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()
        except:
            browser.find_element('class name', 'Distribution-SplashScreenModalCloseButtonOuter').click()
            links = browser.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()
            say('ссылка открыта')
    else:
        say('вы не находитесь на вкладке поиска')
            


def say(text_to_speech):
    time.sleep(0.5)
    ttsEngine.say(str(text_to_speech))
    ttsEngine.runAndWait()


def get_translation(translate_object):
    if translate_object != '':
        say('Выберите язык для перевода.')
        lang_from = listen(mic)
        try:
            lang_from_code = lang_codes[lang_from]
        except:
            say('Язык не найден')
            return
        say('На какой язык перевести?')
        lang_to = listen(mic)
        try:
            lang_to_code = lang_codes[lang_to]
        except:
            say('Язык не найден')
            return
        translator = Translator(from_lang=lang_from_code, to_lang=lang_to_code)
        result = translator.translate(translate_object)
        print(result)
        say(result)


def finish_programm(*args):
    say("Завершаю...")
    browser.quit()
    exit()


def play_greeting(*args):
    greeting = random.choice(greetings)
    say(greeting)


def get_time(*args):
    now = datetime.datetime.now()
    now_time = f'Сейчас {now.hour} {now.minute}' 
    if len(now_time) != 12:
        say(f'Сейчас {now.hour} 0 {now.minute}')
    else:
        say(now_time)
    ttsEngine.runAndWait()


def change_sentence_max(*args):
    global sentence_max
    translator = Translator(from_lang='ru', to_lang='en')
    say('Какой максимум установить?')
    # new_max = listen(mic)
    new_max = input()
    try:
        result = translator.translate(new_max)
        new_max = word_to_num(result)
    except ValueError:
        say('Назовите число')
    sentence_max = new_max
    say('Максимум установлен?')


commands = {
    'найди': find,
    'google': find,
    'загугли': find, 
    'поищи': find, 
    'найти': find,
    "перевод": get_translation, 
    "перевести": get_translation, 
    "переведи": get_translation,
    "открой новую вкладку": add_new_tab, 
    "добавь новую вкладку": add_new_tab, 
    "новая вкладка": add_new_tab,
    "привет": play_greeting, 
    "здравствуй" : play_greeting,
    "добрый день": play_greeting,
    "здарова": play_greeting, 
    "приветик": play_greeting,
    "переключись на вкладку под номером": window_switch_to,
    "переключись на вкладку под номер": window_switch_to, 
    "переключись на вкладку потом номер": window_switch_to, 
    "переключись на вкладку с номером": window_switch_to,  
    "переключись на вкладку номер": window_switch_to, 
    "переключись на вкладку": window_switch_to,
    "перезагрузи": refresh, 
    "перезагрузка": refresh, 
    "перезагрузи страницу": refresh, 
    "перезагрузка страницы": refresh,
    "заверши работу программы": finish_programm, 
    "заверши программу": finish_programm, 
    "заверши работу": finish_programm, 
    "закончить работу": finish_programm, 
    "завершил работу": finish_programm, 
    "выключи программу": finish_programm, 
    "завершить программу": finish_programm, 
    "завершить работу": finish_programm, 
    "останови программу": finish_programm,
    "который час": get_time, 
    "сколько времени": get_time, 
    'скажи время': get_time, 
    "сколько сейчас времени": get_time, 
    "время": get_time,
    "открой ссылку под номером": choose_link,
    "открой ссылку под номер": choose_link, 
    "открой ссылку с номером": choose_link, 
    "открой ссылку номер": choose_link, 
    "перейди по ссылке под номером": choose_link,
    "перейди по ссылке под номер": choose_link,
    "перейди по ссылке с номером": choose_link, 
    "перейди по ссылке номер": choose_link, 
    "выбери ссылку под номером": choose_link,
    "выбери ссылку под номер": choose_link, 
    "выбери ссылку с номером": choose_link, 
    "выбери ссылку номер": choose_link, 
    "перейди по ссылке": choose_link, 
    "нажми на ссылку под номером": choose_link,
    "нажми на ссылку под номер": choose_link, 
    "нажми на ссылку с номером": choose_link, 
    "нажми на ссылку номер": choose_link, 
    "выбери ссылку": choose_link,
    "нажми на ссылку": choose_link,
    "установи новый максимум предложений": change_sentence_max,
    "измени максимум предложений": change_sentence_max,
    "новый максимум предложений": change_sentence_max,
    "установи новый максиму предложений": change_sentence_max,
    "измени максиму предложений": change_sentence_max,
    "новый максиму предложений": change_sentence_max,
    "установи новый максимум": change_sentence_max,
    "измени максимум": change_sentence_max,
    "новый максимум": change_sentence_max,
    "прочитай мне текст страницы": read_text,
    "зачитай мне текст страницы": read_text,
    "прочитай текст страницы": read_text,
    "зачитай текст страницы": read_text,
    "зачитай": read_text,
    "прочитай": read_text,
    "читай": read_text,
}
lang_codes = {
    'русский': 'ru',
    'английский': 'en',
    'арабский': 'ar',
    'болгарский': 'bg',
    'китайский': 'zh',
    'чешский': 'cs',
    'немецкий': 'de',
    'греческий': 'el',
    'испанский': 'es',
    'финский': 'fi',
    'французский': 'fr',
    'итальянский': 'it',
    'японский': 'ja',
    'корейский': 'ko',
    'польский': 'pl',
    'португальский': 'pt',
    'румынский': 'ro',
    'хорватский': 'hr',
    'шведский': 'sv',
    'тайский': 'th',
    'турецкий': 'tr',
    'украинский': 'uk',
    'белорусский': 'be',
    'литовский': 'lt',
    'армянский': 'hy',
    'вьетнамский': 'vi',
    'азербайджанский': 'az',
    'грузинский': 'ka',
    'казахский': 'kk',
    'узбекский': 'uz',
    'татарский': 'tt',
    'сирийский': 'syr',
    'филиппинский': 'fil',
    'башкирский': 'ba',
    'гренландский': 'kl',
    'гавайский': 'haw'
}
stop_commands = ["закончи диалог", 'хватит', "закончить диалог", "хватит болтать", "закончи разговор", "закончить разговор", "завершить диалог", "завершить разговор", "разговор окончен", "заверши диалог"]
numbers = {
    'один': '1',
    'два': '2',
    'три': '3',
    'четыре': '4',
    'пять': '5',
    'шесть': '6',
    'семь': '7',
    'восемь': '8',
    'девять': '9',
    'десять': '10',
    'одиннадцать': '11',
    'двенадцать': '12',
    'тринадцать': '13',
    'четырнадцать': '14',
    'пятнадцать': '15',
}
greetings = ["привет", "здравствуйте", "добрый день"]
farewells = ["пока", "до свидания", "увидимся", "до встречи"]

class VoiceAssistant:
    names = []

ttsEngine = pyttsx3.init()
assistant = VoiceAssistant()
voices = ttsEngine.getProperty("voices")
assistant.recognition_language = "ru-RU"
ttsEngine.setProperty("voice", voices[0].id)
assistant.names = ["вайс", "вася", "ice", "айс", "vice", "wise", "вась", "вальс"]
sentence_max = 5
now_el = 0
with speech_recognition.Microphone(device_index=1) as mic:
    while True:
        command = listen(mic)
        if command in assistant.names:
            say('слушаю вас')
            while True:
                done = False
                stop_dialog = False
                command = listen(mic)
                for stop_command in stop_commands:
                    if command.startswith(stop_command):
                        stop_dialog = True
                        break
                if stop_dialog:
                    say('прекращаю слушать')
                    break
                else: 
                    for key in commands:
                        if command.startswith(key):
                            try:
                                commands[key](command.replace(key, '')[1:])
                            except KeyError:
                                say('передан неверный аргумент')
                            done = True
                            break
                if not done:
                    say('команда не найдена')
