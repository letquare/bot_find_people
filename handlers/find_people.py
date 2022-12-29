from copy import deepcopy

from aiogram import Router, types
from aiogram.fsm.context import FSMContext

from bot_find_people.button import make_buttons
from bot_find_people.states import BotStateFind, BotState
from bot_find_people.phrases import choice_where_find, choice_profile_or_find, choice_find_people

router = Router()
state_in_loop = {}
users = [
    {'имя': 'Emmy',
     'возраст': 18,
     'чем занимается': 'Играю в игры',
     'о себе': 'Пока не получу ачивке не успокоюсь',
     'город': 'Москва'},
    {'имя': 'Tim',
     'возраст': 28,
     'чем занимается': 'Шахтер',
     'о себе': 'Вахтовик',
     'город': 'Тамбов'},
    {'имя': 'Oleg',
     'возраст': 27,
     'чем занимается': 'Варю кофя',
     'о себе': 'В Dota2 2344 часов',
     'город': 'Спб'}
]


@router.message(BotStateFind.find)
async def find_main(message: types.Message, state: FSMContext):
    await message.answer('Тут ты можешь выбрать зону поиска',
                         reply_markup=make_buttons(choice_where_find))
    await state.set_state(BotStateFind.find_filter)


@router.message(BotStateFind.find_filter)
async def find_in_filter(message: types.Message, state: FSMContext):
    if message.text not in choice_where_find:
        await message.answer('Это варианта - нет, внизу ты можешь выбрать нужный',
                             reply_markup=make_buttons(choice_where_find))
    else:
        find_filter = ''
        if message.text == 'По всей России':
            await message.answer('Хорошо, поиск по России')
            find_filter = 'russia'
        elif message.text == 'По всему миру':
            await message.answer('Хорошо, поиск по Миру')
            find_filter = 'world'
        state_in_loop['where_find'] = find_filter
        state_in_loop['first_times'] = False

        state_in_loop['users'] = deepcopy(users)

        await state.set_state(BotStateFind.find_choice)
        await find_in_db_with_filter(message, state)


@router.message(BotStateFind.find_choice)
async def find_in_db_with_filter(message: types.Message, state: FSMContext):
    if message.text == 'Нет, поищу ещё':
        for index, user in enumerate(state_in_loop['users']):
            response = f'Имя {user["имя"]}\nВозраст {user["возраст"]}\nО себе{user["о себе"]}\n'
            del state_in_loop['users'][index]
            await message.answer(response,
                                 reply_markup=make_buttons(choice_find_people))
            break
        else:
            await message.answer('У меня закончились люди для тебя :(')
            state_in_loop['users'] = deepcopy(users)
    elif message.text == 'Стоп':
        await state.set_state(BotState.main)
        await message.answer('Тут ты можешь категорю "Анкета" или Начать поиск',
                             reply_markup=make_buttons(choice_profile_or_find))
    elif message.text == 'Погнали!':
        await state.set_state(BotState.main)
        await message.answer('Твой запрос отправлен! Теперь остается ждать ответа)',
                             reply_markup=make_buttons(choice_profile_or_find))
    else:
        for index, user in enumerate(state_in_loop['users']):
            response = f'Имя {user["имя"]}\nВозраст {user["возраст"]}\nО себе{user["о себе"]}\n'
            del state_in_loop['users'][index]
            await message.answer(response,
                                 reply_markup=make_buttons(choice_find_people))
            break
