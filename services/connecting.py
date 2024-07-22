from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from .main import HHru
from .env import Config


bot = Bot(token=Config.bot_token)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

obj = HHru(Config.phone, Config.password, Config.proxy)
