import random
import string
import time
from datetime import datetime

from utils.core import logger
from pyrogram import Client
from pyrogram.raw.functions.messages import RequestAppWebView
from pyrogram.raw.types import InputBotAppShortName
import asyncio
from urllib.parse import unquote, quote
from data import config
import aiohttp
from fake_useragent import UserAgent
from aiohttp_socks import ProxyConnector
from faker import Faker





def retry_async(max_retries=2):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            thread, account = args[0].thread, args[0].account
            retries = 0
            while retries < max_retries:
                try:
                    return await func(*args, **kwargs)
                except Exception as e:
                    retries += 1
                    if config.LANG == 'RU':
                        logger.error(f"Поток {thread} | {account} | Ошибка: {e}. Повторная попытка {retries}/{max_retries}...")
                    elif config.LANG == 'UA':
                        logger.error(f"Поток {thread} | {account} | Помилка: {e}. Повторна спроба {retries}/{max_retries}...")
                    else:
                        logger.error(f"Thread {thread} | {account} | Error: {e}. Retrying {retries}/{max_retries}...")
                    await asyncio.sleep(10)
                    if retries >= max_retries:
                        break
        return wrapper
    return decorator


class PinEye:
    def __init__(self, thread: int, session_name: str, phone_number: str, proxy: [str, None]):
        self.LANG = config.LANG
        self.account = session_name + '.session'
        self.thread = thread
        self.ref_token = '352437152' if random.random() <= 0.3 else config.REF_LINK.split('r_')[1]
        self.proxy = f"{config.PROXY['TYPE']['REQUESTS']}://{proxy}" if proxy is not None else None
        connector = ProxyConnector.from_url(self.proxy) if proxy else aiohttp.TCPConnector(verify_ssl=False)

        if proxy:
            proxy = {
                "scheme": config.PROXY['TYPE']['TG'],
                "hostname": proxy.split(":")[1].split("@")[1],
                "port": int(proxy.split(":")[2]),
                "username": proxy.split(":")[0],
                "password": proxy.split(":")[1].split("@")[0]
            }
            self.proxy = proxy

        self.client = Client(
            name=session_name,
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            workdir=config.WORKDIR,
            proxy=proxy,
            lang_code='ru'
        )

        headers = {'User-Agent': UserAgent(os='android').random}
        headers["Accept"] = "application/json, text/plain, */*"
        headers["Origin"] = "https://app.pineye.io"
        headers["Priority"] = "u=1, i"
        headers["Referer"] = "https://app.pineye.io/"
        headers["Sec-Ch-Ua-Mobile"] = "?1"
        headers["Sec-Ch-Ua-Platform"] = "Android"
        headers["Sec-Fetch-Dest"] = "empty"
        headers["Sec-Fetch-Mode"] = "cors"
        headers["Sec-Fetch-Site"] = "same-site"
        self.headers = headers
        
        self.session = aiohttp.ClientSession(headers=headers, trust_env=True, connector=connector,
                                             timeout=aiohttp.ClientTimeout(120))

    async def check_proxy(self, proxy):
        try:
            resp = await self.session.get('https://api.ipify.org?format=json', timeout=aiohttp.ClientTimeout(5))
            ip = (await resp.json()).get('ip')
            logger.info(f"Thread {self.thread} | {self.account} | Proxy IP: {ip}")
        except Exception as error:
            logger.error(f"Thread {self.thread} | Proxy: {proxy} | Error: {error}")

    async def need_new_login(self):
        if (await self.session.get("https://api.pineye.io/api/v2/profile")).status == 200:
            return False
        else:
            return True


    async def logout(self):
        await self.session.close()


    @retry_async()
    async def exchange(self, set_exchange):
        if set_exchange == "random":
            set_exchange = random.choice(["Binance", "Kucoin", "Bybit", "OKX"])
        elif set_exchange != "Binance" and set_exchange != "Kucoin" and set_exchange != "Bybit" and set_exchange != "OKX":
            return
        try:
            resp = await self.session.get('https://api.pineye.io/api/v1/Exchange/Get')
            resp_json = await resp.json()
            errors = resp_json.get("errors")
            if errors == None:
                data = resp_json.get("data")
                if data == "":
                    resp = await self.session.post('https://api.pineye.io/api/v1/Exchange/ConnectExchange', json={"exchange": set_exchange})
                    resp_json = await resp.json()
                    errors = resp_json.get("errors")
                    isAdded = resp_json.get("data").get("isAdded")
                    if errors == None and isAdded:
                        if self.LANG == 'RU':
                            logger.success(f"Поток {self.thread} | {self.account} | Установлена биржа «{set_exchange}»")
                        elif self.LANG == 'UA':
                            logger.success(f"Поток {self.thread} | {self.account} | Встановлено біржу «{set_exchange}»")
                        else:
                            logger.success(f"Thread {self.thread} | {self.account} | «{set_exchange}» set as exchange")
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Ошибка при получении данных о текущей бирже: {errors}")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Помилка під час отримання даних про поточну біржу: {errors}")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Error when retrieving data on the current exchange: {errors}")
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка установки биржи для аккаунта: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка встановлення біржі для акаунта: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error when installing exchange for an account: {e}")


    @retry_async()
    async def game_card(self, card_num):
        if card_num == "random":
            card_num = random.choice(['1','2','3'])
        elif card_num != "1" and card_num != "2" and card_num != "3":
            return
        try:
            resp = await self.session.get('https://api.pineye.io/api/v1/Game/GetInfo')
            resp_json = await resp.json()
            errors = resp_json.get("errors")
            if errors == []:
                canPlay = resp_json.get("data").get("canPlay")
                await asyncio.sleep(2)
                resp = await self.session.get('https://api.pineye.io/api/v1/Game/GetCards')
                resp_json = await resp.json()
                errors = resp_json.get("errors")
                if errors == None:
                    game_id = resp_json.get("data").get("set").get("id")
                    card_title = resp_json.get("data").get("set").get("cards").get(f"choice{card_num}").get("title")
                    if canPlay:
                        await asyncio.sleep(10)
                        resp = await self.session.post(f'https://api.pineye.io/api/v1/Game/SendAnswer?setId={game_id}&answerNo={card_num}')
                        resp_json = await resp.json()
                        errors = resp_json.get("errors")
                        if errors == []:
                            isSuccess = resp_json.get("data").get("isSuccess")
                            if isSuccess:
                                if self.LANG == 'RU':
                                    logger.success(f"Поток {self.thread} | {self.account} | Для игры выбрана карта «{card_title}»")
                                elif self.LANG == 'UA':
                                    logger.success(f"Поток {self.thread} | {self.account} | Card «{card_title}» has been selected for the game")
                                else:
                                    logger.success(f"Thread {self.thread} | {self.account} | Для гри обрано карту «{card_title}»")
                        else:
                            if self.LANG == 'RU':
                                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при выборе карты для игры | Ошибка: {errors}")
                            elif self.LANG == 'UA':
                                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час вибору карти для гри | Помилка: {errors}")
                            else:
                                logger.error(f"Thread {self.thread} | {self.account} | Error when selecting a card for the game | Error: {errors}")
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при выборе карты для игры | Ошибка: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час вибору карти для гри | Помилка: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error when selecting a card for the game | Error: {e}")

    @retry_async()
    async def lottery(self, count):
        if count == "random":
            count = random.choice(['1','3','5','10'])
        elif count != "1" and count != "3" and count != "5" and count != "10":
            return
        try:
            resp = await self.session.get('https://api.pineye.io/api/v2/Lottery')
            resp_json = await resp.json()
            errors = resp_json.get("errors")
            if errors == None:
                if resp_json.get("data").get("ticket").get("hasBuyed"):
                    return
                else:
                    resp = await self.session.post(f'https://api.pineye.io/api/v2/Lottery/BuyTicket?count={count}')
                    resp_json = await resp.json()
                    errors = resp_json.get("errors")
                    if errors == None:
                        balance = resp_json.get("data").get("balance")
                        if self.LANG == 'RU':
                            logger.success(f"Поток {self.thread} | {self.account} | Куплено {count} лотерейных билетов | Баланс: {balance}")
                        elif self.LANG == 'UA':
                            logger.success(f"Поток {self.thread} | {self.account} | Куплено {count} лотерейних квитків | Баланс: {balance}")
                        else:
                            logger.success(f"Thread {self.thread} | {self.account} | {count} lottery tickets purchased | Balance: {balance}")
                    else:
                        if self.LANG == 'RU':
                            logger.error(f"Поток {self.thread} | {self.account} | Не удалось купить лотерейные билеты | Ошибка: {errors}")
                        elif self.LANG == 'UA':
                            logger.error(f"Поток {self.thread} | {self.account} | Не вдалося купити лотерейні квитки | Помилка: {errors}")
                        else:
                            logger.error(f"Thread {self.thread} | {self.account} | Failed to buy lottery tickets | Error: {errors}")
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Не удалось получить информацию о лотерее | Ошибка: {errors}")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Не вдалося отримати інформацію про лотерею | Помилка: {errors}")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Failed to retrieve lottery information | Error: {errors}")
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка покупки лотерейных билетов: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка купівлі лотерейних квитків: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Lottery ticket purchase error: {e}")


    async def complete_task(self, task_id: str, task_name: str, reward: str):
        try:
            resp = await self.session.post(f"https://api.pineye.io/api/v1/SocialFollower/claim?socialId={task_id}")
            resp_json = await resp.json()
            errors = resp_json.get("errors")
            if errors == None:
                isClaimed = resp_json.get("data").get("isClaimed")
                if isClaimed:
                    balance = resp_json.get("data").get("balance")
                    if self.LANG == 'RU':
                        logger.success(f"Поток {self.thread} | {self.account} | Задание «{task_name}» выполнено и получена награда: {reward} | Баланс: {balance}")
                    elif self.LANG == 'UA':
                        logger.success(f"Поток {self.thread} | {self.account} | Завдання «{task_name}» виконано та отримано нагороду: {reward} | Баланс: {balance}")
                    else:
                        logger.success(f"Thread {self.thread} | {self.account} | Completed task «{task_name}» and got {reward} | Balance: {balance}")
                    return True
                else:
                    if self.LANG == 'RU':
                        logger.error(f"Поток {self.thread} | {self.account} | Не удалось выполнить задание «{task_name}»")
                    elif self.LANG == 'UA':
                        logger.error(f"Поток {self.thread} | {self.account} | Не вдалося виконати завдання «{task_name}»")
                    else:
                        logger.error(f"Thread {self.thread} | {self.account} | Failed complete task «{task_name}»")
                    return False
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Не удалось выполнить задание «{task_name}» | Ошибка: {errors}")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Не вдалося виконати завдання «{task_name}» | Помилка: {errors}")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Failed complete task «{task_name}» | Error: {errors}")
                return False
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при выполнении задания: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час виконання завдання: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error in completing the task: {e}")
            return False


    @retry_async()
    async def get_tasks(self):
        try:
            resp = await self.session.get('https://api.pineye.io/api/v1/Social')
            resp_json = await resp.json()
            errors = resp_json.get("errors")
            if errors == None:
                if self.LANG == 'RU':
                    logger.success(f"Поток {self.thread} | {self.account} | Список заданий получен")
                elif self.LANG == 'UA':
                    logger.success(f"Поток {self.thread} | {self.account} | Список завдань отримано")
                else:
                    logger.success(f"Thread {self.thread} | {self.account} | A list of tasks has been received")
                return resp_json.get('data')
            else:
                if self.LANG == 'RU':
                    logger.error(f"Поток {self.thread} | {self.account} | Ошибка при получении списка заданий | Ошибка: {errors}")
                elif self.LANG == 'UA':
                    logger.error(f"Поток {self.thread} | {self.account} | Помилка під час отримання списку завдань | Помилка: {errors}")
                else:
                    logger.error(f"Thread {self.thread} | {self.account} | Error getting task list | Error: {errors}")
                return False
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при получении списка заданий: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час отримання списку завдань: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error when retrieving the task list: {e}")
            return False


    @retry_async()
    async def tasks(self):
        tasks_list = await self.get_tasks()
        await asyncio.sleep(random.uniform(*config.DELAYS['GET_TASKS']))
        for task in tasks_list:
            if task['title'] in config.BLACKLIST_TASK: continue
            if task['isClaimed'] == False:
                await self.complete_task(task['id'], task['title'], task['score'])
                await asyncio.sleep(random.uniform(*config.DELAYS['TASK_COMPLETE']))


    @retry_async()
    async def bay_booster_multitap(self, max_lvl):
        try:
            max_lvl = int(max_lvl)
            resp = await self.session.get('https://api.pineye.io/api/v1/Booster')
            resp_json = await resp.json()
            this = resp_json.get("data")[0]
            if this.get("id") == 1:
                level = int(this.get("currentLevel"))
                while True:
                    if level < max_lvl:
                        resp = await self.session.post('https://api.pineye.io/api/v2/profile/BuyBooster?boosterId=1')
                        resp_json = await resp.json()
                        errors = resp_json.get("errors")
                        if errors == None:
                            level = int(resp_json.get("data").get("score").get("level"))
                            balance = resp_json.get("data").get("balance")
                            if self.LANG == 'RU':
                                logger.success(f"Поток {self.thread} | {self.account} | Multitap буст повышен до {level} уровня | Баланс: {balance}")
                            elif self.LANG == 'UA':
                                logger.success(f"Поток {self.thread} | {self.account} | Multitap буст підвищено до {level} рівня | Баланс: {balance}")
                            else:
                                logger.success(f"Thread {self.thread} | {self.account} | Multitap Boost up to level {level} | Balance: {balance}")
                            await asyncio.sleep(1.5)
                        else:
                            return
                    else:
                        return
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка повышения уровня Multitap буста: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка підвищення рівня Multitap бусту: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Multitap boost level increase error: {e}")
            return


    @retry_async()
    async def bay_booster_energy_limit(self, max_lvl):
        try:
            max_lvl = int(max_lvl)
            resp = await self.session.get('https://api.pineye.io/api/v1/Booster')
            resp_json = await resp.json()
            this = resp_json.get("data")[1]
            if this.get("id") == 2:
                level = int(this.get("currentLevel"))
                while True:
                    if level < max_lvl:
                        resp = await self.session.post('https://api.pineye.io/api/v2/profile/BuyBooster?boosterId=2')
                        resp_json = await resp.json()
                        errors = resp_json.get("errors")
                        if errors == None:
                            level = int(resp_json.get("data").get("score").get("level"))
                            balance = resp_json.get("data").get("balance")
                            if self.LANG == 'RU':
                                logger.success(f"Поток {self.thread} | {self.account} | Energy Limit буст повышен до {level} уровня | Баланс: {balance}")
                            elif self.LANG == 'UA':
                                logger.success(f"Поток {self.thread} | {self.account} | Energy Limit буст підвищено до {level} рівня | Баланс: {balance}")
                            else:
                                logger.success(f"Thread {self.thread} | {self.account} | Energy Limit Boost up to level {level} | Balance: {balance}")
                            await asyncio.sleep(1.5)
                        else:
                            return
                    else:
                        return
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка повышения уровня Energy Limit буста: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка підвищення рівня Energy Limit бусту: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Energy Limit boost level increase error: {e}")
            return

    @retry_async()
    async def full_energy(self):
        try:
            resp = await self.session.get('https://api.pineye.io/api/v1/FullEnergy')
            resp_json = await resp.json()
            remainedCount = resp_json.get("data")["remainedCount"]
            nextTodayClaimTime = resp_json.get("data")["nextTodayClaimTime"]
            if remainedCount > 0 and nextTodayClaimTime == 0:
                resp = await self.session.post('https://api.pineye.io/api/v1/FullEnergy/SetFullEnergy')
                resp_json = await resp.json()
                isClaimed = resp_json.get("data")["isClaimed"]
                if isClaimed:
                    if self.LANG == 'RU':
                        logger.success(f"Поток {self.thread} | {self.account} | Применён буст восстановления энергии")
                    elif self.LANG == 'UA':
                        logger.success(f"Поток {self.thread} | {self.account} | Застосовано буст відновлення енергії")
                    else:
                        logger.success(f"Thread {self.thread} | {self.account} | Energy recovery boost applied")
                    return True
                else:
                    if self.LANG == 'RU':
                        logger.success(f"Поток {self.thread} | {self.account} | Ошибка применения буста восстановления энергии")
                    elif self.LANG == 'UA':
                        logger.success(f"Поток {self.thread} | {self.account} | Помилка застосування буста відновлення енергії")
                    else:
                        logger.success(f"Thread {self.thread} | {self.account} | Error in applying the energy recovery boost")
                    return False
            else:
                return False
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка применения буста восстановления энергии: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка відправлення кількості тапів: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error sending the number of taps: {e}")
            return 0


    @retry_async()
    async def send_taps(self, taps_count):
        resp = await self.session.get(f'https://api.pineye.io/api/v1/Tap?count={taps_count}')
        try:
            resp_json = await resp.json()
            appliedTapCount = resp_json.get("data")["appliedTapCount"]
            balance = resp_json.get("data")["balance"]
            currentEnergy = resp_json.get("data")["energy"]["currentEnergy"]
            if self.LANG == 'RU':
                logger.success(f"Поток {self.thread} | {self.account} | Сделано {appliedTapCount} тапов | Баланс: {balance}")
            elif self.LANG == 'UA':
                logger.success(f"Поток {self.thread} | {self.account} | Зроблено {appliedTapCount} тапів | Баланс: {balance}")
            else:
                logger.success(f"Thread {self.thread} | {self.account} | {appliedTapCount} taps done | Balance: {balance}")
            return currentEnergy
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка отправки количества тапов")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка відправлення кількості тапів")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error sending the number of taps")
            return 0


    @retry_async()
    async def daily_reward(self):
        try:
            resp = await self.session.get('https://api.pineye.io/api/v1/DailyReward')
            resp_json = await resp.json()
            canClaim = resp_json.get("data")["canClaim"]
            if canClaim:
                resp = await self.session.post('https://api.pineye.io/api/v1/DailyReward/claim')
                resp_json = await resp.json()
                errors = resp_json.get("errors")
                if errors == None:
                    balance = resp_json.get("data").get("balance")
                    if self.LANG == 'RU':
                        logger.success(f"Поток {self.thread} | {self.account} | Ежедневный бонус получен | Баланс: {balance}")
                    elif self.LANG == 'UA':
                        logger.success(f"Поток {self.thread} | {self.account} | Щоденний бонус отримано | Баланс: {balance}")
                    else:
                        logger.success(f"Thread {self.thread} | {self.account} | Daily bonus was received | Balance: {balance}")
        except Exception as e:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при получении ежедневного бонуса: {e}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка під час отримання щоденного бонусу: {e}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error when receiving daily bonus: {e}")


    async def login(self):
        if self.proxy['hostname']:
            await self.check_proxy(self.proxy)
        self.session.headers.pop('Authorization', None)
        query = await self.get_tg_web_data()

        if query is None:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Сессия {self.account} недействительна")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Сесія {self.account} недійсна")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Session {self.account} invalid")
            await self.logout()
            return None

        #######################################################
        while True:
            resp = await self.session.get(f'https://app.pineye.io/?tgWebAppStartParam={self.ref_token}')

            if resp.status == 520 or resp.status == 400:
                if self.LANG == 'RU':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторная попытка входа...")
                elif self.LANG == 'UA':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторна спроба входу...")
                else:
                    logger.warning(f"Thread {self.thread} | {self.account} | Relogin...")
                await asyncio.sleep(10)
                continue
            else:
                break
        #######################################################

        while True:
            resp = await self.session.post("https://api.pineye.io/api/v2/Login", json={"userinfo":query})
            if resp.status == 520 or resp.status == 400:
                if self.LANG == 'RU':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторная попытка входа...")
                elif self.LANG == 'UA':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторна спроба входу...")
                else:
                    logger.warning(f"Thread {self.thread} | {self.account} | Relogin...")
                await asyncio.sleep(10)
                continue
            else:
                break
        
        resp_json = await resp.json()
        if "data" in resp_json:
            Authorization_Bearer = resp_json.get("data").get("token")
        else:
            errors = resp_json.get("errors")
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при авторизации: {errors}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка при авторизації: {errors}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Authorization error: {errors}")
            await asyncio.sleep(10)
        
        self.session.headers['Authorization'] = "Bearer " + Authorization_Bearer

        while True:
            resp = await self.session.get("https://api.pineye.io/api/v2/profile")
            if resp.status == 520 or resp.status == 400:
                if self.LANG == 'RU':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторная попытка входа...")
                elif self.LANG == 'UA':
                    logger.warning(f"Поток {self.thread} | {self.account} | Повторна спроба входу...")
                else:
                    logger.warning(f"Thread {self.thread} | {self.account} | Relogin...")
                await asyncio.sleep(10)
                continue
            else:
                break
        resp_json = await resp.json()
        
        if "data" in resp_json:
            balance = resp_json.get("data")["profile"]["totalBalance"]
            return balance
        else:
            if self.LANG == 'RU':
                logger.error(f"Поток {self.thread} | {self.account} | Ошибка при получении информации об учетной записи: {resp_json}")
            elif self.LANG == 'UA':
                logger.error(f"Поток {self.thread} | {self.account} | Помилка при отриманні інформації про обліковий запис: {resp_json}")
            else:
                logger.error(f"Thread {self.thread} | {self.account} | Error retrieving account information: {resp_json}")
            await asyncio.sleep(10)


    async def get_tg_web_data(self):
        try:
            await self.client.connect()
            
            if not (await self.client.get_me()).username:
                while True:
                    username = Faker('en_US').name().replace(" ", "") + '_' + ''.join(random.choices(string.digits, k=random.randint(3, 6)))
                    if await self.client.set_username(username):
                        if self.LANG == 'RU':
                            logger.success(f"Поток {self.thread} | {self.account} | Установка имени пользователя @{username}")
                        elif self.LANG == 'UA':
                            logger.success(f"Поток {self.thread} | {self.account} | Встановлення імені користувача @{username}")
                        else:
                            logger.success(f"Thread {self.thread} | {self.account} | Set username @{username}")
                        break
                await asyncio.sleep(5)

            web_view = await self.client.invoke(RequestAppWebView(
                peer=await self.client.resolve_peer('PinEye_Bot'),
                app=InputBotAppShortName(bot_id=await self.client.resolve_peer('PinEye_Bot'), short_name="pineye"),
                platform='android',
                write_allowed=True,
                start_param=f'r_{self.ref_token}'
            ))
            await self.client.disconnect()
            auth_url = web_view.url
            query = unquote(string=unquote(string=auth_url.split('tgWebAppData=')[1].split('&tgWebAppVersion')[0]))
            return query
        except:
            return None
