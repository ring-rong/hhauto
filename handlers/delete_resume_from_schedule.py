from aiogram import Router, types, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services import is_admin
from services.connecting import obj
from keyboards.keyboard import TextButtonList


class DelResume(StatesGroup):
    title = State()


router = Router()


@router.message(F.text == TextButtonList['del_resume'])
async def del_resume(message: types.Message) -> None:
    if await is_admin(message.from_user.id):
        if len(obj.resume_active) > 0:
            await message.answer('Введите наименование резюме, которое хотите удалить.')
            await DelResume.title.set()
        else:
            await message.answer('В расписании нет резюме')


@router.message(DelResume.title)
async def set_title(message: types.Message, state: FSMContext) -> None:
    title = message.text
    if await obj.del_resume_active(title):
        text = "<b>Удалено следующее резюме</b>" \
               f"\n{title}"
    else:
        text = 'Резюме с таким наименованием не найдено.'
    await message.answer(text, parse_mode='html')
    await state.clear()


def register_handler_delete_from_schedule(dp: Dispatcher):
    dp.include_router(router)