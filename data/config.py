#
#   DO NOT CHANGE ANYTHING IN THIS FILE!!!! ALL SETTINGS ARE STORED IN config.ini AND CHANGED FROM SOFTWARE MENU
#
#   В ЭТОМ ФАЙЛЕ НИЧЕГО НЕ МЕНЯТЬ!!! ВСЕ НАСТРОЙКИ ХРАНЯТСЯ В config.ini И МЕНЯЮТСЯ ЧЕРЕЗ МЕНЮ СОФТА
#
#   У ЦЬОМУ ФАЙЛІ НІЧОГО НЕ ЗМІНЮВАТИ!!! УСІ НАЛАШТУВАННЯ ЗБЕРІГАЮТЬСЯ В config.ini І ЗМІНЮЮТЬСЯ ЧЕРЕЗ МЕНЮ СОФТА

import configparser

config = configparser.ConfigParser()
config.sections()

config.read('data/config.ini')

LANG = config['Config']['LANG']

API_ID = int(config['Config']['API_ID'])
API_HASH = config['Config']['API_HASH']

REF_LINK = config['Config']['REF_LINK']

SEND_TAPS = config['Config'].getboolean('SEND_TAPS')
TAPS_COUNT = list(map(int, config['Config']['TAPS_COUNT'].split("|")))
BOOST_FULL_ENERGY = config['Config'].getboolean('BOOST_FULL_ENERGY')
BAY_BOOSTER_MULTITAP = config['Config'].getboolean('BAY_BOOSTER_MULTITAP')
BAY_BOOSTER_MULTITAP_LVL = config['Config']['BAY_BOOSTER_MULTITAP_LVL']
BAY_BOOSTER_ENERGY_LIMIT = config['Config'].getboolean('BAY_BOOSTER_ENERGY_LIMIT')
BAY_BOOSTER_ENERGY_LIMIT_LVL = config['Config']['BAY_BOOSTER_ENERGY_LIMIT_LVL']
DAILY_REWARD = config['Config'].getboolean('DAILY_REWARD')
TASKS = config['Config'].getboolean('TASKS')
LOTTERY = config['Config'].getboolean('LOTTERY')
LOTTERY_COUNT = config['Config']['LOTTERY_COUNT']
GAME_CARD = config['Config'].getboolean('GAME_CARD')
GAME_CARD_NUM = config['Config']['GAME_CARD_NUM']
EXCHANGE = config['Config'].getboolean('EXCHANGE')
SET_EXCHANGE = config['Config']['SET_EXCHANGE']

DELAYS = {
    "RELOGIN": list(map(int, config['Config']['DELAY_RELOGIN'].split("|"))),  # delay after a login attempt
    'ACCOUNT': list(map(int, config['Config']['DELAY_ACCOUNT'].split("|"))),  # delay between connections to accounts (the more accounts, the longer the delay)
    'SEND_TAPS': list(map(int, config['Config']['DELAY_SEND_TAPS'].split("|"))),
    'TASK_COMPLETE': list(map(int, config['Config']['DELAY_TASK_COMPLETE'].split("|"))),  # delay after completed the task
    'GET_TASKS': list(map(int, config['Config']['DELAY_GET_TASKS'].split("|"))),  # delay after receiving list of tasks
    'RESTARTING': list(map(int, config['Config']['DELAY_RESTARTING'].split("|")))  # delay before restart
}

# blacklist tasks
with open('data/BLACKLIST_TASK.txt', 'r') as f:
    BLACKLIST_TASK = f.read().splitlines()

PROXY = {
    "USE_PROXY_FROM_FILE": config['Config'].getboolean('USE_PROXY_FROM_FILE'),  # True - if use proxy from file, False - if use proxy from accounts.json
    "PROXY_PATH": "data/proxy.txt",  # path to file proxy
    "TYPE": {
        "TG": config['Config']['PROXY_TYPE_TG'],  # proxy type for tg client. "socks4", "socks5" and "http" are supported
        "REQUESTS": config['Config']['PROXY_TYPE_REQUESTS']  # proxy type for requests. "http" for https and http proxys, "socks5" for socks5 proxy.
        }
}

# session folder (do not change)
WORKDIR = "sessions/"

# timeout in seconds for checking accounts on valid
TIMEOUT = 30
