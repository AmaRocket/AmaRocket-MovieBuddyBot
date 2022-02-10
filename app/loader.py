import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config
from language_middleware import setup_middleware

loop = asyncio.get_event_loop()
bot = Bot(token=config.TOKEN, parse_mode="HTML")

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

logging.basicConfig(
    format="%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s",
    level=logging.INFO,
)

i18n = setup_middleware(dp)
_ = i18n.gettext
