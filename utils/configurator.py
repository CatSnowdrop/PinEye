import configparser
import os

import sys
from pprint import pprint
sys.path.append(os.path.realpath("."))
import inquirer


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def input_str_or_int(text, text_error):
    while True:
        try:
            input_str = input(text)
            input_int = int(input_str)
            break
        except ValueError:
            if input_str == '':
                input_int = ''
                break
            print(text_error)
            continue
    return input_str


async def configurator():
    clear()
    questions = [
        inquirer.List(
            "action",
            message="Select languege | Выберите язык | Оберіть мову",
            choices=["English", "Русский", "Українська"]
        ),
    ]
    action_mapping = {
                'English': 'EN',
                'Русский': 'RU',
                'Українська': 'UA'
            }
    answers = inquirer.prompt(questions)
    lang = action_mapping[answers['action']]
    clear()
    if lang == 'RU':
        print('API_ID и API_HASH Telegram можно получить здесь - https://my.telegram.org/auth')
        print('Вы можете указать пустое значение, чтобы использовать API Android (не рекомендуется).')
        text_error = "\nВведённое значение должно быть числом!"
        API_ID = input_str_or_int("Введите свой API_ID: ", text_error)
        API_HASH = str(input("Введите свой API_HASH: "))
        clear()
        REF_LINK = str(input("Введите свою реферальную ссылку (не обязательно): "))
        clear()
        print('Вы можете передать пустое значение, чтобы использовать параметры по умолчанию (5-10)')
        DELAY_RELOGIN_MIN = input_str_or_int("Введите минимальную задержку после попытки входа в систему (в секундах): ", text_error)
        DELAY_RELOGIN_MAX = input_str_or_int("Введите максимальную задержку после попытки входа в систему (в секундах): ", text_error)
        clear()
        print('Вы можете передать пустое значение, чтобы использовать параметры по умолчанию (5-15)')
        DELAY_ACCOUNT_MIN = input_str_or_int("Введите минимальную задержку между подключениями к аккаунтам (чем больше аккаунтов, тем больше задержка) (в секундах): ", text_error)
        DELAY_ACCOUNT_MAX = input_str_or_int("Введите максимальную задержку между подключениями к аккаунтам (чем больше аккаунтов, тем больше задержка) (в секундах): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Включить автоматические тапы (автокликер)?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        SEND_TAPS = action_mapping[answers['action']]
        clear()
        print('Вы можете передать пустое значение, чтобы использовать параметры по умолчанию (10-100)')
        TAPS_COUNT_MIN = input_str_or_int("Введите минимальное количество тапов отправляемых за один раз: ", text_error)
        TAPS_COUNT_MAX = input_str_or_int("Введите максимальную количество тапов отправляемых за один раз: ", text_error)
        clear()
        print('Вы можете передать пустое значение, чтобы использовать параметры по умолчанию (6-10)')
        DELAY_SEND_TAPS_MIN = input_str_or_int("Введите минимальную задержку перед отправкой количества тапов: ", text_error)
        DELAY_SEND_TAPS_MAX = input_str_or_int("Введите минимальную задержку перед отправкой количества тапов: ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Использовать буст восполнения, когда энергия для тапов закончилась?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        BOOST_FULL_ENERGY = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Получать ежедневную награду?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        DAILY_REWARD = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Включить автоматические выполнение заданий?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        TASKS = action_mapping[answers['action']]
        clear()
        print('Вы можете передать пустое значение, чтобы использовать параметры по умолчанию (5-10)')
        DELAY_GET_TASKS_MIN = input_str_or_int("Введите минимальную задержку после получения списка заданий (в секундах): ", text_error)
        DELAY_GET_TASKS_MAX = input_str_or_int("Введите максимальную задержку после получения списка заданий (в секундах): ", text_error)
        clear()
        print('Вы можете передать пустое значение, чтобы использовать параметры по умолчанию (10-25)')
        DELAY_TASK_COMPLETE_MIN = input_str_or_int("Введите минимальную зажержку после выполнения задания (в секундах): ", text_error)
        DELAY_TASK_COMPLETE_MAX = input_str_or_int("Введите максимальную зажержку после выполнения задания (в секундах): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Покупать лотерейные былеты автоматически?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        LOTTERY = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Какое количество лотерейных билетов покупать (Если покупка разрешена)?",
                choices=["1", "3", "5", "10", "Случайное количество"]
            ),
        ]
        action_mapping = {
                    '1': "1",
                    '3': "3",
                    '5': "5",
                    '10': "10",
                    'Случайное количество': "random",
                }
        answers = inquirer.prompt(questions)
        LOTTERY_COUNT = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Играть в игру с выбором карт автоматически?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        GAME_CARD = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Какую карту выбирать в игре (Если игра разрешена)?",
                choices=["1", "2", "3", "Случайная карта"]
            ),
        ]
        action_mapping = {
                    '1': "1",
                    '2': "2",
                    '3': "3",
                    'Случайная карта': "random",
                }
        answers = inquirer.prompt(questions)
        GAME_CARD_NUM = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Автоматически выбирать биржу?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        EXCHANGE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Какую биржу выбирать (Если выбор разрешён)?",
                choices=["Binance", "Kucoin", "Bybit", "OKX", "Случайный выбор"]
            ),
        ]
        action_mapping = {
                    'Binance': "Binance",
                    'Kucoin': "Kucoin",
                    'Bybit': "Bybit",
                    'OKX': "OKX",
                    'Случайный выбор': "random",
                }
        answers = inquirer.prompt(questions)
        SET_EXCHANGE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Автоматически покупать Multitap бустер?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        BAY_BOOSTER_MULTITAP = action_mapping[answers['action']]
        clear()
        BAY_BOOSTER_MULTITAP_LVL = input_str_or_int("До какого уровня улучшать Multitap бустер? (от 0 до 1000): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Автоматически покупать Energy Limit бустер?",
                choices=["Да", "Нет"]
            ),
        ]
        action_mapping = {
                    'Да': True,
                    'Нет': False,
                }
        answers = inquirer.prompt(questions)
        BAY_BOOSTER_ENERGY_LIMIT = action_mapping[answers['action']]
        clear()
        BAY_BOOSTER_ENERGY_LIMIT_LVL = input_str_or_int("До какого уровня улучшать Energy Limit бустер? (от 0 до 1000): ", text_error)
        clear()
        print('Вы можете передать пустое значение, чтобы использовать параметры по умолчанию (600-1800)')
        DELAY_RESTARTING_MIN = input_str_or_int("Введите минимальную задержку перед перезапуском (в секундах): ", text_error)
        DELAY_RESTARTING_MAX = input_str_or_int("Введите максимальную задержку перед перезапуском (в секундах): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Использовать прокси из файла (data/proxi.txt) или прокси, указанный при создании сессии (sessions/accounts.json)?",
                choices=["Прокси из файла", "Прокси, указанный при создании сессии"]
            ),
        ]
        action_mapping = {
                    'Прокси из файла': True,
                    'Прокси, указанный при создании сессии': False,
                }
        answers = inquirer.prompt(questions)
        USE_PROXY_FROM_FILE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Выберите тип прокси для сессии telegram:",
                choices=["http", "socks4", "socks5"]
            ),
        ]
        answers = inquirer.prompt(questions)
        PROXY_TYPE_TG = answers['action']
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Выберите тип прокси для запросов:",
                choices=["http", "socks4", "socks5"]
            ),
        ]
        answers = inquirer.prompt(questions)
        PROXY_TYPE_REQUESTS = answers['action']
    elif lang == 'UA':
        print('API_ID та API_HASH Telegram можна отримати тут - https://my.telegram.org/auth')
        print('Ви можете вказати порожнє значення, щоб використовувати API Android (не рекомендується).')
        text_error = "\nВведене значення має бути числом!"
        API_ID = input_str_or_int("Введіть свій API_ID: ", text_error)
        API_HASH = str(input("Введіть свій API_HASH: "))
        clear()
        REF_LINK = str(input("Введіть своє реферальне посилання (не обов'язково): "))
        clear()
        print('Ви можете передати порожнє значення, щоб використовувати параметри за замовчуванням (5-10)')
        DELAY_RELOGIN_MIN = input_str_or_int("Введіть мінімальну затримку після спроби входу в систему (у секундах): ", text_error)
        DELAY_RELOGIN_MAX = input_str_or_int("Введіть максимальну затримку після спроби входу в систему (у секундах): ", text_error)
        clear()
        print('Ви можете передати порожнє значення, щоб використовувати параметри за замовчуванням (5-15)')
        DELAY_ACCOUNT_MIN = input_str_or_int("Введіть мінімальну затримку між підключеннями до акаунтів (що більше акаунтів, то більша затримка) (у секундах): ", text_error)
        DELAY_ACCOUNT_MAX = input_str_or_int("Введіть максимальну затримку між підключеннями до акаунтів (що більше акаунтів, то більша затримка) (у секундах): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Увімкнути автоматичні тапи (автоклікер)?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        SEND_TAPS = action_mapping[answers['action']]
        clear()
        print('Ви можете передати порожнє значення, щоб використовувати параметри за замовчуванням (10-100)')
        TAPS_COUNT_MIN = input_str_or_int("Введіть мінімальну кількість тапів, що відправляються за один раз: ", text_error)
        TAPS_COUNT_MAX = input_str_or_int("Введіть максимальну кількість тапів, що відправляються за один раз: ", text_error)
        clear()
        print('Ви можете передати порожнє значення, щоб використовувати параметри за замовчуванням (6-10)')
        DELAY_SEND_TAPS_MIN = input_str_or_int("Введіть мінімальну затримку перед надсиланням кількості тапів: ", text_error)
        DELAY_SEND_TAPS_MAX = input_str_or_int("Введіть мінімальну затримку перед надсиланням кількості тапів: ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Використовувати буст поновлення, коли енергія для тапів закінчилася?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        BOOST_FULL_ENERGY = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Отримувати щоденну нагороду?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        DAILY_REWARD = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Увімкнути автоматичне виконання завдань?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        TASKS = action_mapping[answers['action']]
        clear()
        print('Ви можете передати порожнє значення, щоб використовувати параметри за замовчуванням (5-10)')
        DELAY_GET_TASKS_MIN = input_str_or_int("Введіть мінімальну затримку після отримання списку завдань (у секундах): ", text_error)
        DELAY_GET_TASKS_MAX = input_str_or_int("Введіть максимальну затримку після отримання списку завдань (у секундах): ", text_error)
        clear()
        print('Ви можете передати порожнє значення, щоб використовувати параметри за замовчуванням (10-25)')
        DELAY_TASK_COMPLETE_MIN = input_str_or_int("Введіть мінімальну затримку після виконання завдання (у секундах): ", text_error)
        DELAY_TASK_COMPLETE_MAX = input_str_or_int("Введіть максимальну зажержку після виконання завдання (у секундах): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Купувати лотерейні білети автоматично?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        LOTTERY = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Яку кількість лотерейних білетів купувати (Якщо купівля дозволена)?",
                choices=["1", "3", "5", "10", "Випадкова кількість"]
            ),
        ]
        action_mapping = {
                    '1': "1",
                    '3': "3",
                    '5': "5",
                    '10': "10",
                    'Випадкова кількість': "random",
                }
        answers = inquirer.prompt(questions)
        LOTTERY_COUNT = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Грати в гру з вибором карт автоматично?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        GAME_CARD = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Яку карту обирати в грі (Якщо гра дозволена)?",
                choices=["1", "2", "3", "Випадкова карта"]
            ),
        ]
        action_mapping = {
                    '1': "1",
                    '2': "2",
                    '3': "3",
                    'Випадкова карта': "random",
                }
        answers = inquirer.prompt(questions)
        GAME_CARD_NUM = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Автоматично вибирати біржу?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        EXCHANGE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Яку біржу обирати (Якщо вибір дозволений)?",
                choices=["Binance", "Kucoin", "Bybit", "OKX", "Випадковий вибір"]
            ),
        ]
        action_mapping = {
                    'Binance': "Binance",
                    'Kucoin': "Kucoin",
                    'Bybit': "Bybit",
                    'OKX': "OKX",
                    'Випадковий вибір': "random",
                }
        answers = inquirer.prompt(questions)
        SET_EXCHANGE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Автоматично купувати Multitap бустер?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        BAY_BOOSTER_MULTITAP = action_mapping[answers['action']]
        clear()
        BAY_BOOSTER_MULTITAP_LVL = input_str_or_int("До якого рівня покращувати Multitap бустер? (від 0 від 1000): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Автоматично купувати Energy Limit бустер?",
                choices=["Так", "Ні"]
            ),
        ]
        action_mapping = {
                    'Так': True,
                    'Ні': False,
                }
        answers = inquirer.prompt(questions)
        BAY_BOOSTER_ENERGY_LIMIT = action_mapping[answers['action']]
        clear()
        BAY_BOOSTER_ENERGY_LIMIT_LVL = input_str_or_int("До якого рівня покращувати Energy Limit бустер? (від 0 від 1000): ", text_error)
        clear()
        print('Ви можете передати порожнє значення, щоб використовувати параметри за замовчуванням (600-1800)')
        DELAY_RESTARTING_MIN = input_str_or_int("Введіть мінімальну затримку перед перезапуском (у секундах): ", text_error)
        DELAY_RESTARTING_MAX = input_str_or_int("Введіть максимальну затримку перед перезапуском (у секундах): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Використовувати проксі з файлу (data/proxi.txt) або проксі, вказаний під час створення сесії (sessions/accounts.json)?",
                choices=["Проксі з файлу", "Проксі, вказаний під час створення сесії"]
            ),
        ]
        action_mapping = {
                    'Проксі з файлу': True,
                    'Проксі, вказаний під час створення сесії': False,
                }
        answers = inquirer.prompt(questions)
        USE_PROXY_FROM_FILE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Оберіть тип проксі для сесії telegram:",
                choices=["http", "socks4", "socks5"]
            ),
        ]
        answers = inquirer.prompt(questions)
        PROXY_TYPE_TG = answers['action']
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Оберіть тип проксі для запитів:",
                choices=["http", "socks4", "socks5"]
            ),
        ]
        answers = inquirer.prompt(questions)
        PROXY_TYPE_REQUESTS = answers['action']















    else:
        print('Telegram API_ID and API_HASH can be obtained here - https://my.telegram.org/auth')
        print('You can drop an empty value to use the Android API (not recommended)')
        text_error = "\nThe entered value must be a number!"
        API_ID = input_str_or_int("Enter your API_ID: ", text_error)
        API_HASH = str(input("Enter your API_HASH: "))
        clear()
        REF_LINK = str(input("Enter your referral link (optional): "))
        clear()
        print('You can pass an empty value to use the default parameters (5-10)')
        DELAY_RELOGIN_MIN = input_str_or_int("Enter the minimum delay after a login attempt (in seconds): ", text_error)
        DELAY_RELOGIN_MAX = input_str_or_int("Enter the maximum delay after a login attempt (in seconds): ", text_error)
        clear()
        print('You can pass an empty value to use the default parameters (5-15)')
        DELAY_ACCOUNT_MIN = input_str_or_int("Enter the minimum delay between connections to accounts (the more accounts, the longer the delay) (in seconds): ", text_error)
        DELAY_ACCOUNT_MAX = input_str_or_int("Enter the maximum delay between connections to accounts (the more accounts, the longer the delay) (in seconds): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Enable automatic taps (autoclicker)?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        SEND_TAPS = action_mapping[answers['action']]
        clear()
        print('You can pass an empty value to use the default parameters (10-100)')
        TAPS_COUNT_MIN = input_str_or_int("Enter the minimum number of taps to be sent at one time: ", text_error)
        TAPS_COUNT_MAX = input_str_or_int("Enter the maximum number of taps to be sent at one time: ", text_error)
        clear()
        print('You can pass an empty value to use the default parameters (6-10)')
        DELAY_SEND_TAPS_MIN = input_str_or_int("Enter the minimum delay before sending the number of taps counts: ", text_error)
        DELAY_SEND_TAPS_MAX = input_str_or_int("Enter the maximum delay before sending the number of taps counts: ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Use the replenishment boost when energy has run out?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        BOOST_FULL_ENERGY = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Receive a daily reward?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        DAILY_REWARD = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Enable automatic task execution?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        TASKS = action_mapping[answers['action']]
        clear()
        print('You can pass an empty value to use the default parameters (5-10)')
        DELAY_GET_TASKS_MIN = input_str_or_int("Enter the minimum delay after receiving the task list (in seconds): ", text_error)
        DELAY_GET_TASKS_MAX = input_str_or_int("Enter the maximum delay after receiving the task list (in seconds): ", text_error)
        clear()
        print('You can pass an empty value to use the default parameters (10-25)')
        DELAY_TASK_COMPLETE_MIN = input_str_or_int("Enter the minimum delay after the task is completed (in seconds): ", text_error)
        DELAY_TASK_COMPLETE_MAX = input_str_or_int("Enter the maximum delay after the task is completed (in seconds): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Buying lottery tickets automatically?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        LOTTERY = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="How many lottery tickets should I buy (If purchase is allowed)?",
                choices=["1", "3", "5", "10", "Random"]
            ),
        ]
        action_mapping = {
                    '1': "1",
                    '3': "3",
                    '5': "5",
                    '10': "10",
                    'Random': "random",
                }
        answers = inquirer.prompt(questions)
        LOTTERY_COUNT = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Play a game with card selection automatically?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        GAME_CARD = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Which card should I choose in the game (If the game is allowed)?",
                choices=["1", "2", "3", "Random card"]
            ),
        ]
        action_mapping = {
                    '1': "1",
                    '2': "2",
                    '3': "3",
                    'Random card': "random",
                }
        answers = inquirer.prompt(questions)
        GAME_CARD_NUM = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Automatically select an exchange?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        EXCHANGE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Which exchange to choose (If the choice is allowed)?",
                choices=["Binance", "Kucoin", "Bybit", "OKX", "Random selection"]
            ),
        ]
        action_mapping = {
                    'Binance': "Binance",
                    'Kucoin': "Kucoin",
                    'Bybit': "Bybit",
                    'OKX': "OKX",
                    'Random selection': "random",
                }
        answers = inquirer.prompt(questions)
        SET_EXCHANGE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Automatically buy a Multitap booster?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        BAY_BOOSTER_MULTITAP = action_mapping[answers['action']]
        clear()
        BAY_BOOSTER_MULTITAP_LVL = input_str_or_int("To what level should the Multitap booster be upgraded? (0 to 1000): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Automatically buy the Energy Limit booster?",
                choices=["Yes", "No"]
            ),
        ]
        action_mapping = {
                    'Yes': True,
                    'No': False,
                }
        answers = inquirer.prompt(questions)
        BAY_BOOSTER_ENERGY_LIMIT = action_mapping[answers['action']]
        clear()
        BAY_BOOSTER_ENERGY_LIMIT_LVL = input_str_or_int("To what level should the Energy Limit booster be upgraded? (0 to 1000): ", text_error)
        clear()
        print('You can pass an empty value to use the default parameters (600-1800)')
        DELAY_RESTARTING_MIN = input_str_or_int("Enter the minimum delay before restarting (in seconds): ", text_error)
        DELAY_RESTARTING_MAX = input_str_or_int("Enter the maximum delay before restarting (in seconds): ", text_error)
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Use proxy from file (data/proxi.txt) or proxy specified at session creation (sessions/accounts.json)?",
                choices=["Proxy from file", "Proxy specified at session creation"]
            ),
        ]
        action_mapping = {
                    'Proxy from file': True,
                    'Proxy specified at session creation': False,
                }
        answers = inquirer.prompt(questions)
        USE_PROXY_FROM_FILE = action_mapping[answers['action']]
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Select proxy type for telegram session:",
                choices=["http", "socks4", "socks5"]
            ),
        ]
        answers = inquirer.prompt(questions)
        PROXY_TYPE_TG = answers['action']
        clear()
        questions = [
            inquirer.List(
                "action",
                message="Select proxy type for requests:",
                choices=["http", "socks4", "socks5"]
            ),
        ]
        answers = inquirer.prompt(questions)
        PROXY_TYPE_REQUESTS = answers['action']




    config = configparser.ConfigParser()
    config['DEFAULT'] = {
        'LANG': 'EN',
        'API_ID': '6',
        'API_HASH': 'eb06d4abfb49dc3eeb1aeb98ae0f581e',
        'REF_LINK': 'https://t.me/PinEye_Bot/pineye?startapp=r_352437152',
        'USE_PROXY_FROM_FILE': 'False',
        'PROXY_TYPE_TG': 'socks5',
        'PROXY_TYPE_REQUESTS': 'socks5',
        'DELAY_RELOGIN': '5|10',
        'DELAY_ACCOUNT': '5|15',
        'DELAY_TASK_COMPLETE': '10|15',
        'DELAY_GET_TASKS': '5|10',
        'DELAY_RESTARTING': '600|1800',
        'SEND_TAPS': 'True',
        'TAPS_COUNT': '10|100',
        'DELAY_SEND_TAPS': '6|10',
        'BOOST_FULL_ENERGY': 'True',
        'BAY_BOOSTER_MULTITAP': 'False',
        'BAY_BOOSTER_MULTITAP_LVL': '1000',
        'BAY_BOOSTER_ENERGY_LIMIT': 'False',
        'BAY_BOOSTER_ENERGY_LIMIT_LVL': '1000',
        'DAILY_REWARD': 'True',
        'TASKS': 'True',
        'LOTTERY': 'False',
        'LOTTERY_COUNT': 'random',
        'GAME_CARD': 'True',
        'GAME_CARD_NUM': 'random',
        'EXCHANGE': 'False',
        'SET_EXCHANGE': 'random'
    }
    
    config['Config'] = {
        'LANG': lang,
        'SEND_TAPS': SEND_TAPS,
        'BOOST_FULL_ENERGY': BOOST_FULL_ENERGY,
        'DAILY_REWARD': DAILY_REWARD,
        'TASKS': TASKS,
        'LOTTERY': LOTTERY,
        'LOTTERY_COUNT': LOTTERY_COUNT,
        'GAME_CARD': GAME_CARD,
        'GAME_CARD_NUM': GAME_CARD_NUM,
        'EXCHANGE': EXCHANGE,
        'SET_EXCHANGE': SET_EXCHANGE,
        'BAY_BOOSTER_MULTITAP': BAY_BOOSTER_MULTITAP,
        'BAY_BOOSTER_ENERGY_LIMIT': BAY_BOOSTER_ENERGY_LIMIT,
        'USE_PROXY_FROM_FILE': USE_PROXY_FROM_FILE,
        'PROXY_TYPE_TG': PROXY_TYPE_TG,
        'PROXY_TYPE_REQUESTS': PROXY_TYPE_REQUESTS
    }

    if (API_ID != '' and API_HASH != ''):
        config['Config']['API_ID'] = API_ID
        config['Config']['API_HASH'] = API_HASH
    
    if REF_LINK != '':
        config['Config']['REF_LINK'] = REF_LINK
            
    if DELAY_RELOGIN_MIN != '' and DELAY_RELOGIN_MAX != '' and (int(DELAY_RELOGIN_MIN) <= int(DELAY_RELOGIN_MAX)):
        config['Config']['DELAY_RELOGIN'] = f'{DELAY_RELOGIN_MIN}|{DELAY_RELOGIN_MAX}'

    if DELAY_ACCOUNT_MIN != '' and DELAY_ACCOUNT_MAX != '' and (int(DELAY_ACCOUNT_MIN) < int(DELAY_ACCOUNT_MAX)):
        config['Config']['DELAY_ACCOUNT'] = f'{DELAY_ACCOUNT_MIN}|{DELAY_ACCOUNT_MAX}'

    if TAPS_COUNT_MIN != '' and TAPS_COUNT_MAX != '' and (int(TAPS_COUNT_MIN) < int(TAPS_COUNT_MAX)):
        config['Config']['TAPS_COUNT'] = f'{TAPS_COUNT_MIN}|{TAPS_COUNT_MAX}'
    if DELAY_SEND_TAPS_MIN != '' and DELAY_SEND_TAPS_MAX != '' and (int(DELAY_SEND_TAPS_MIN) < int(DELAY_SEND_TAPS_MAX)):
        config['Config']['DELAY_SEND_TAPS'] = f'{DELAY_SEND_TAPS_MIN}|{DELAY_SEND_TAPS_MAX}'

    if DELAY_GET_TASKS_MIN != '' and DELAY_GET_TASKS_MAX != '' and (int(DELAY_GET_TASKS_MIN) < int(DELAY_GET_TASKS_MAX)):
        config['Config']['DELAY_GET_TASKS'] = f'{DELAY_GET_TASKS_MIN}|{DELAY_GET_TASKS_MAX}'
    if DELAY_TASK_COMPLETE_MIN != '' and DELAY_TASK_COMPLETE_MAX != '' and (int(DELAY_TASK_COMPLETE_MIN) < int(DELAY_TASK_COMPLETE_MAX)):
        config['Config']['DELAY_TASK_COMPLETE'] = f'{DELAY_TASK_COMPLETE_MIN}|{DELAY_TASK_COMPLETE_MAX}'

    if BAY_BOOSTER_MULTITAP_LVL != '':
        config['Config']['BAY_BOOSTER_MULTITAP_LVL'] = f'{BAY_BOOSTER_MULTITAP_LVL}'
    if BAY_BOOSTER_ENERGY_LIMIT_LVL != '':
        config['Config']['BAY_BOOSTER_ENERGY_LIMIT_LVL'] = f'{BAY_BOOSTER_ENERGY_LIMIT_LVL}'

    if DELAY_RESTARTING_MIN != '' and DELAY_RESTARTING_MAX != '' and (int(DELAY_RESTARTING_MIN) < int(DELAY_RESTARTING_MAX)):
        config['Config']['DELAY_RESTARTING'] = f'{DELAY_RESTARTING_MIN}|{DELAY_RESTARTING_MAX}'
    
    

    with open('data/config.ini', 'w') as configfile:
      config.write(configfile)

    clear()

    return True