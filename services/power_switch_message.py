from aiogram import Bot, Dispatcher
from aiogram.exceptions import TelegramBadRequest

import asyncio
import time
import os

from .auto_raise_resume import tasks
from .connecting import bot
from .env import Config


async def on_startup(bot: Bot) -> None:
    asyncio.create_task(tasks())
    os.environ['TZ'] = Config.time_zone
    time.tzset()
    text = '🟩 Бот включился' \
           f'\n{time.strftime("%H:%M:%S")}'
    try:
        await bot.send_message(os.getenv('admin_tg'), text)
    except TelegramBadRequest as e:
        if e.message == 'Chat not found':
            pass
        elif e.message == 'Forbidden: bot was blocked by the user':
            print('[Запуск] Бот заблокирован пользователем')
        else:
            raise e


async def on_shutdown(bot: Bot) -> None:
    os.environ['TZ'] = Config.time_zone
    time.tzset()
    text = '🟥 Бот выключился' \
           f'\n{time.strftime("%H:%M:%S")}'
    try:
        await bot.send_message(os.getenv('admin_tg'), text)
    except TelegramBadRequest as e:
        if e.message == 'Chat not found':
            pass
        elif e.message == 'Forbidden: bot was blocked by the user':
            print('[Отключение] Бот заблокирован пользователем')
        else:
            raise e