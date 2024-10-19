from utils.pineye import PinEye
from asyncio import sleep
from random import uniform
from data import config
from utils.core import logger
import datetime
from utils.core.telegram import Accounts
import asyncio
from aiohttp.client_exceptions import ContentTypeError


async def start(thread: int, session_name: str, phone_number: str, proxy: [str, None]):
    pineye = PinEye(session_name=session_name, phone_number=phone_number, thread=thread, proxy=proxy)
    account = session_name + '.session'

    sleep_timer = round(uniform(*config.DELAYS['ACCOUNT']))
    if config.LANG == 'RU':
        logger.info(f"Thread {thread} | {account} | Бот будет запущен через {sleep_timer} сек.")
    elif config.LANG == 'UA':
        logger.info(f"Thread {thread} | {account} | Бот буде запущений через {sleep_timer} сек.")
    else:
        logger.info(f"Thread {thread} | {account} | Bot will start in {sleep_timer}s")
    await sleep(sleep_timer)

    attempts = 3
    while attempts:
        try:
            balance = await pineye.login()
            if config.LANG == 'RU':
                logger.success(f"Поток {thread} | {account} | Вход выполнен! | Balance: {balance}")
            elif config.LANG == 'UA':
                logger.success(f"Поток {thread} | {account} | Вхід виконано! | Balance: {balance}")
            else:
                logger.success(f"Thread {thread} | {account} | Login! | Balance: {balance}")
            break
        except Exception as e:
            logger.error(f"Thread {thread} | {account} | Left login attempts: {attempts}, error: {e}")
            await asyncio.sleep(uniform(*config.DELAYS['RELOGIN']))
            attempts -= 1
    else:
        if config.LANG == 'RU':
            logger.error(f"Поток {thread} | {account} | Не удалось войти")
        elif config.LANG == 'UA':
            logger.error(f"Поток {thread} | {account} | Не вдалося увійти")
        else:
            logger.error(f"Thread {thread} | {account} | Couldn't login")
        await pineye.logout()
        return

    while True:
        try:
            await asyncio.sleep(5)
            if await pineye.need_new_login():
                if await pineye.login() is None:
                    return
            
            if config.EXCHANGE:
                await pineye.exchange(config.SET_EXCHANGE)
                await asyncio.sleep(3.5)

            if config.DAILY_REWARD:
                await pineye.daily_reward()
                await asyncio.sleep(3.5)

            if config.SEND_TAPS:
                currentEnergy = 9999999
                while True:
                    taps_count = round(uniform(*config.TAPS_COUNT))
                    if taps_count <= currentEnergy:
                        currentEnergy = await pineye.send_taps(taps_count)
                        await sleep(uniform(*config.DELAYS['SEND_TAPS']))
                    else:
                        if config.BOOST_FULL_ENERGY:
                            isClaimed_full_energy = await pineye.full_energy()
                            if isClaimed_full_energy:
                                currentEnergy = 9999999
                            else:
                                break
                        else:
                            break

            if config.BAY_BOOSTER_MULTITAP:
                await pineye.bay_booster_multitap(config.BAY_BOOSTER_MULTITAP_LVL)
                await asyncio.sleep(2)

            if config.BAY_BOOSTER_ENERGY_LIMIT:
                await pineye.bay_booster_energy_limit(config.BAY_BOOSTER_ENERGY_LIMIT_LVL)
                await asyncio.sleep(2)

            if config.TASKS:
                await pineye.tasks()
                await asyncio.sleep(3.5)

            if config.LOTTERY:
                await pineye.lottery(config.LOTTERY_COUNT)
                await asyncio.sleep(5.5)

            if config.GAME_CARD:
                await pineye.game_card(config.GAME_CARD_NUM)
                await asyncio.sleep(3.5)
            
            sleep_timer = round(uniform(*config.DELAYS['RESTARTING']))
            if config.LANG == 'RU':
                logger.success(f"Поток {thread} | {account} | Сон: {sleep_timer} секунд...")
            elif config.LANG == 'UA':
                logger.success(f"Поток {thread} | {account} | Сон: {sleep_timer} секунд...")
            else:
                logger.success(f"Thread {thread} | {account} | Sleep: {sleep_timer} second...")
            await asyncio.sleep(sleep_timer)

        except ContentTypeError as e:
            if config.LANG == 'RU':
                logger.error(f"Поток {thread} | {account} | Ошибка: {e}")
            elif config.LANG == 'UA':
                logger.error(f"Поток {thread} | {account} | Помилка: {e}")
            else:
                logger.error(f"Thread {thread} | {account} | Error: {e}")
            await asyncio.sleep(120)

        except Exception as e:
            if config.LANG == 'RU':
                logger.error(f"Поток {thread} | {account} | Ошибка: {e}")
            elif config.LANG == 'UA':
                logger.error(f"Поток {thread} | {account} | Помилка: {e}")
            else:
                logger.error(f"Thread {thread} | {account} | Error: {e}")


