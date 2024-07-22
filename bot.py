from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

import asyncio
import os
import subprocess
import urllib.request
import json
import pytz
import platform
import time

from services.background import keep_alive
from handlers import (register_handler_base,
                      register_handler_add_to_schedule,
                      register_handler_delete_from_schedule)
from services import on_startup, on_shutdown, load_tokens_auth, Config
from services.connecting import bot
from services.check_proxy import is_valid
from services.status_code import status

async def load_timezone_map(file_path):
    timezone_map = {}
    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip()
                if line:
                    unix_timezone, windows_timezone = line.split(':')
                    timezone_map[unix_timezone.strip()] = windows_timezone.strip()
    except FileNotFoundError:
        print(f"Timezone mapping file not found: {file_path}")
    return timezone_map

async def set_timezone_windows(timezone_map, timezone):
    windows_timezone = timezone_map.get(timezone)
    if windows_timezone:
        current_timezone = subprocess.check_output(["tzutil", "/g"]).decode().strip()
        if current_timezone != windows_timezone:
            subprocess.call(["tzutil", "/s", windows_timezone])
            print(f"Updating time zone to {windows_timezone}")
        else:
            print("Not updating time zone")

        # Set the timezone using pytz
        tz = pytz.timezone(timezone)
        os.environ['TZ'] = tz.zone
    else:
        print(f"No mapping found for timezone: {timezone}")

async def set_timezone_unix(timezone):
    if timezone:
        os.environ['TZ'] = timezone
        if hasattr(time, 'tzset'):
            time.tzset()
        print(f"Setting time zone to {timezone}")
    else:
        print(f"No mapping found for timezone: {timezone}")

async def set_timezone(timezone_map):
    try:
        url = "http://ip-api.com/json/?fields=timezone"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode())
        timezone = data["timezone"]

        if platform.system() == "Windows":
            await set_timezone_windows(timezone_map, timezone)
        else:
            await set_timezone_unix(timezone)

    except Exception as e:
        print(f"Error setting timezone: {str(e)}")

async def main():
    load_tokens_auth()

    dp = Dispatcher(storage=MemoryStorage())

    register_handler_base(dp)
    register_handler_add_to_schedule(dp)
    register_handler_delete_from_schedule(dp)

    timezone_map = await load_timezone_map('timezone_map.txt')
    await set_timezone(timezone_map)

    # Remove webhook before starting polling to avoid conflicts
    await bot.delete_webhook()

    proxy = Config.proxy
    if is_valid(proxy) or proxy == 'None':
        await dp.start_polling(bot, on_startup=on_startup, on_shutdown=on_shutdown)
    else:
        print(status(0))

keep_alive()
if __name__ == '__main__':
    asyncio.run(main())
