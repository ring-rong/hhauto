from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


TextButtonList = {
    'profile': '⚙ Профиль',
    'list_resume': '📜 Список резюме',
    'list_active_resume': '📅 Расписание',
    'add_resume': '➕ Добавить/обновить',
    'del_resume': '❌ Удалить',
    'auth': '🚀️ Авторизоваться',
    'update_list_resume': '📝 Обновить список резюме',
    'notifications': '🔔 Вкл/выкл уведомления',
}

ButtonList = {key: KeyboardButton(text=text) for key, text in TextButtonList.items()}

def create_home_keyboard():
    keyboard = ReplyKeyboardBuilder()
    keyboard.row(ButtonList['profile'], ButtonList['notifications'])
    keyboard.row(ButtonList['list_resume'], ButtonList['list_active_resume'])
    keyboard.row(ButtonList['add_resume'], ButtonList['del_resume'])
    keyboard.row(ButtonList['auth'], ButtonList['update_list_resume'])
    return keyboard.as_markup(resize_keyboard=True)


home = create_home_keyboard()