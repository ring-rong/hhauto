from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.types import Message

from services import is_admin
from keyboards.keyboard import home, TextButtonList
from services.connecting import obj
from services.env import Config


router = Router()


@router.message(Command(commands=['start']))
async def start(message: Message) -> None:
    if await is_admin(message.from_user.id):
        text = 'HeadHunter Resume\nСервис автоматического подъема резюме каждые 4 часа.'
        await message.answer(text, reply_markup=home)


@router.message(F.text == TextButtonList['auth'])
async def auth(message: Message) -> None:
    if await is_admin(message.from_user.id):
        if await obj.login():
            await message.answer('Авторизация выполнена!')
        else:
            await message.answer('Ошибка авторизации')


@router.message(F.text == TextButtonList['profile'])
async def profile(message: Message) -> None:
    if await is_admin(message.from_user.id):
        text = '<b>Ваши данные</b>\n' \
               f"Телефон: {Config.phone}\n" \
               f"Пароль: {Config.password}\n" \
               f"Прокси: {'не используется' if Config.proxy == 'None' else Config.proxy}\n" \
               f"Уведомления: {'включены' if obj.notifications else 'отключены'}\n" \
               f"Часовой пояс: {Config.time_zone}"
        await message.answer(text, parse_mode='html')


@router.message(F.text == TextButtonList['update_list_resume'])
async def update_list_resume(message: Message) -> None:
    if await is_admin(message.from_user.id):
        if await obj.get_resumes():
            text = '<b>Ваши резюме</b>'
            for title in obj.resume_src.keys():
                text += f'\n\n<code>{title}</code>'
            await message.answer(text, parse_mode='html')
        else:
            text = 'Необходимо авторизоваться.'
            await message.answer(text, parse_mode='html')


@router.message(F.text == TextButtonList['list_resume'])
async def list_resume(message: Message) -> None:
    if await is_admin(message.from_user.id):
        if len(obj.resume_src) > 0:
            text = '<b>Ваши резюме</b>'
            for title in obj.resume_src.keys():
                text += f'\n\n<code>{title}</code>'
        else:
            text = '<b>Резюме не найдено</b>' \
                   '\n1) Попробуйте обновить список резюме.' \
                   '\n2) Проверьте наличие резюме в профиле hh.ru'
        await message.answer(text, parse_mode='html')


@router.message(F.text == TextButtonList['list_active_resume'])
async def list_active_resume(message: Message) -> None:
    if await is_admin(message.from_user.id):
        if len(obj.resume_active) > 0:
            text = '<b>Расписание</b>'
            for title, value in obj.resume_active.items():
                text += f"\n\n<code>{title}</code>\n"

                hour = int(obj.resume_active[title]['time']['hour'])
                minute = int(obj.resume_active[title]['time']['minute'])
                seconds = int(obj.resume_active[title]['time']['seconds'])
                for temp in range(0, 21, 4):
                    text += f"\n<code>{(hour + temp) % 24}:" \
                            f"{minute if minute > 9 else f'0{minute}'}:" \
                            f"{seconds if seconds > 9 else f'0{seconds}'}</code>"

        else:
            text = 'Ни одно резюме не добавлено в расписание.'
        await message.answer(text, parse_mode='html')


@router.message(F.text == TextButtonList['notifications'])
async def switch_notifications(message: Message) -> None:
    if await is_admin(message.from_user.id):
        obj.notifications = False if obj.notifications else True
        text = 'Включил' if obj.notifications else 'Отключил'
        await message.answer(text, parse_mode='html')


def register_handler_base(dp):
    dp.include_router(router)