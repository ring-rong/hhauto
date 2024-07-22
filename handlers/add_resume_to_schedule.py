from aiogram import Router, types, F, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from services import is_admin
from services.connecting import obj
from keyboards.keyboard import TextButtonList


class AddResume(StatesGroup):
    title = State()
    time = State()


router = Router()


@router.message(F.text == TextButtonList['add_resume'])
async def add_resume(message: types.Message, state: FSMContext) -> None:
    if await is_admin(message.from_user.id):
        if len(obj.resume_src) > 0:
            await message.answer('Введите наименование резюме, которое нужно поднимать.')
            await state.set_state(AddResume.title)
        else:
            await message.answer('Обновите список резюме.')


@router.message(AddResume.title)
async def set_resume(message: types.Message, state: FSMContext) -> None:
    title = message.text
    if title in obj.resume_src.keys():
        await state.update_data(title=title)
        await message.answer(
            'Введите время поднятия, например 14:00 будет соответствовать '
            '2:00 6:00 10:00 <code>14:00</code> 18:00 22:00',
            parse_mode='html'
        )
        await state.set_state(AddResume.time)
    else:
        await message.answer('Резюме с таким наименованием не найдено.')
        await state.clear()


@router.message(AddResume.time)
async def set_time(message: types.Message, state: FSMContext) -> None:
    time = message.text
    if ':' in time:
        hour, minute = time.split(':')
        if hour.isnumeric() and minute.isnumeric():
            hour, minute = int(hour), int(minute)
            if (0 <= hour < 24) and (0 <= minute < 60):
                data = await state.get_data()
                title = data['title']
                await obj.add_resume_active(title, hour, minute)
                await message.answer(
                    f'<b>Добавлено новое расписание</b>\n'
                    f'{title}\n'
                    f'{time}',
                    parse_mode='html'
                )
            else:
                await message.answer('Ошибка при вводе времени, используйте формат 10:30.')
        else:
            await message.answer('Ошибка при вводе времени, используйте формат 10:30.')
    else:
        await message.answer('Ошибка при вводе времени, используйте формат 10:30.')

    await state.clear()


def register_handler_add_to_schedule(dp: Dispatcher):
    dp.include_router(router)