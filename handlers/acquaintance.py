from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot_find_people.button import make_buttons
from bot_find_people.states import BotState
from bot_find_people.phrases import choice_profile_or_find

router = Router()
data_user = {}


@router.message(BotState.name)
async def name_user(message: types.Message, state: FSMContext):
    data_user['id'] = message.from_user.id
    data_user['имя'] = message.text.lower()
    await message.answer(f'Хорошо, {message.text.title()}!\nЕсли, что имя можно будет потом поменять!')
    await message.answer('Сколько тебе лет?')
    await state.set_state(BotState.how_old_u)


@router.message(BotState.how_old_u)
async def how_old_u(message: types.Message, state: FSMContext):
    if message.text.isdigit() and len(message.text) < 3:
        year = message.text
        data_user['возраст'] = year
        await state.set_state(BotState.photo)
        await message.answer('Теперь нужно от тебя фото!')
    else:
        await message.answer('Попробуй еще раз')


@router.message(BotState.photo)
async def phote_user(message: types.Message, state: FSMContext):
    data_user['фото'] = message.photo[-1]
    await message.answer('Cупер!')
    await message.answer('Твой род деятельности?')
    await state.set_state(BotState.what_u_do)


@router.message(BotState.what_u_do)
async def what_u_do(message: types.Message, state: FSMContext):
    data_user['чем занимается'] = message.text.lower()
    await message.answer('Спасибо!')
    await message.answer('Напишите о себе пару слов:')
    await state.set_state(BotState.about_you)


@router.message(BotState.about_you)
async def about_you(message: types.Message, state: FSMContext):
    data_user['о себе'] = message.text.lower()
    await message.answer('Спасибо!')
    await message.answer('В каком городе ты находишься?')
    await state.set_state(BotState.city)


@router.message(BotState.city)
async def city_user(message: types.Message, state: FSMContext):
    data_user['город'] = message.text.lower()
    await message.answer('Ура! Всё готово!')
    with open('save.txt', 'w') as file:
        [file.write(f'{k}: {v}\n') for k, v in data_user.items()]
    await state.set_state(BotState.main)
    await message.answer('Тут ты можешь выбрать категорю "Анкета" или Начать поиск',
                         reply_markup=make_buttons(choice_profile_or_find))


