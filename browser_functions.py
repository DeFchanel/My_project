from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from translate import Translator
from word2number.w2n import word_to_num
import re
import time
from lists import numbers
from audio_functions import say


def finish_programm(*args):
    say("Завершаю...")
    browser.quit()
    exit()


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


def change_sentence_max(*args):
    global sentence_max
    translator = Translator(from_lang='ru', to_lang='en')
    say('Какой максимум установить?')
    new_max = input()
    try:
        result = translator.translate(new_max)
        new_max = word_to_num(result)
    except ValueError:
        say('Назовите число')
    sentence_max = new_max
    say('Максимум установлен?')


options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('log-level=3')
options.page_load_strategy='eager'
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)