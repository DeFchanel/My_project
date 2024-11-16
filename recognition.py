from lists import *
from commands import *


if __name__ == '__main__':
    browser.get('https://ya.ru')
    sentence_max = 5
    now_el = 0
    while True:
        done = False
        stop_dialog = False
        command = listen()
        print(command)
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
