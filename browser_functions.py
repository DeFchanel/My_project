from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from translate import Translator
from word2number.w2n import word_to_num
from audio_functions import listen
import time
from lists import numbers
from audio_functions import say
from pprint import pprint


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
    text = text
    translate = "translate({value},'ABCDEFGHIJKLMNOPQRSTUVWXYZЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮЁ','abcdefghijklmnopqrstuvwxyzйцукенгшщзхъфывапролджэячсмитьбюё')"
    links = browser.find_elements('xpath', f'//a//*[{translate.format(value="normalize-space(text())")} = "{text.lower()}"]/parent::a') + browser.find_elements('xpath', f'//a[{translate.format(value="normalize-space(text())")} = "{text.lower()}"]')
    buttons = browser.find_elements('xpath', f'//button//*[{translate.format(value="normalize-space(text())")} = "{text.lower()}"]/parent::button') + browser.find_elements('xpath', f'//button[{translate.format(value="normalize-space(text())")} = "{text.lower()}"]')
    elements = links + buttons
    if len(elements) == 0:
        say('Такой элемент не найден или на него невозможно нажать')
    elif len(elements) > 1:
        say('Подходящих элементов несколько, выберите номер нужного элемента')
        try:
            number = int(input())
            elements[number - 1].click()
        except IndexError:
            say('Элемент не существует')
    else:
        elements[0].click()


def read_text(*args):
    global now_el
    all_text = browser.find_element('xpath', "/html/body")
    cleared_text = all_text.text.replace("'", '').split('\n')
    pprint(cleared_text)
    now_element = 0
    answer = 'да'
    while answer in ['продолжи', 'да', 'продолжай']:
        for element_text in cleared_text[now_element: now_element + sentence_max]:
            say(element_text)
            now_element
        flag = 0
        while not flag:
            say('Продолжить зачитывание страницы?')
            answer = listen()
            if answer in ['продолжи', 'да', 'продолжай']:
                now_element += sentence_max
                flag = 1
            elif answer in ['нет', 'не надо', 'не', 'не продолжай']:
                now_element = 0
                flag = 1
            else:
                say('Ответ не распознан')


def find(target):
    say('ищу ваш запрос')
    browser.get('https://www.google.ru')
    find_field = browser.find_element('class name', 'gLFyf')
    find_field.send_keys(target)
    find_field.send_keys(Keys.ENTER)


def choose_link(target):
    tabs = browser.window_handles
    current_tab = tabs.index(browser.current_window_handle)
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
        tabs = browser.window_handles
        browser.switch_to.window(tabs[current_tab + 1])
        browser.refresh()
        say('ссылка открыта')
    elif 'https://yandex.ru/search' in browser.current_url or 'https://ya.ru/search' in browser.current_url:
        try:
            links = browser.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()
        except:
            browser.find_element('class name', 'Distribution-SplashScreenModalCloseButtonOuter').click()
            links = browser.find_elements('xpath', '//a[contains(@class, "OrganicTitle-Link")]')
            links[number - 1].click()
            tabs = browser.window_handles
            browser.switch_to.window(tabs[current_tab + 1])
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
sentence_max = 5
options.add_argument('--disable-blink-features=AutomationControlled')
options.add_argument('log-level=3')
options.page_load_strategy='eager'
options.add_experimental_option('useAutomationExtension', False)
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)

add_new_tab()
find('госуслуги')
choose_link('Один')
time.sleep(5)
# read_text()
click_to('каталог')
click_to('услуги')