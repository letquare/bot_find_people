from aiogram import types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from bot_find_people.button import make_buttons
from bot_find_people.states import BotState, BotStateMain, BotStateFind
from bot_find_people.handlers.find_people import find_main
from bot_find_people.phrases import choice_list, choice_profile_or_find, choice_profile

router = Router()


@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message, state: FSMContext):
    """
    This handler will be called when user sends `/start` command.
    """

    greeting_message = """
    Добро пожаловать в Погнали бот. Мы поможем найти компаньона в городах для похода на мероприятия. А так же у нас есть собственные мероприятия, узнать про которые можно в нашем канале @pognaly
    """

    await message.answer(greeting_message, reply_markup=ReplyKeyboardRemove())
    user_agreement = """
    Продолжая пользоваться ботом вы соглашаетесь с пользовательским соглашением и даете разрешение на обработку персональных данных.
    Поддержка - @pognaly_support
    """

    await message.answer(user_agreement)
    try:
        with open('save.txt', 'r') as file:
            info = file.read()
        if str(message.from_user.id) in info: #TODO добавить проверку на известность
            await message.answer('Вижу новенький, давай знакомиться!')
            await message.answer('Как тебя зовут?')
            await state.set_state(BotState.name)
        else:
            await message.answer('Чтож выбери варики внизу', reply_markup=make_buttons(choice_list))
    except FileNotFoundError:
        await message.answer('Вижу новенький, давай знакомиться!')
        await message.answer('Как тебя зовут?')
        await state.set_state(BotState.name)



@router.message(BotStateMain.change_info)
async def change_date(message: types.Message, state: FSMContext):
    with open('save.txt', 'r') as file:
        info = file.read().split('\n')
    for item in message.text.split(', '):
        item = item.split()
        if item[0].lower() in info:
            pass
            # data_user[item[0]] = item[1].lower() # TODO Нужно будет потом поменять на запись в бд и выбрасывать на главную
    else:
        if message.text.lower() == 'назад':
            await state.set_state(BotState.main)
            await message.answer('Тут ты можешь категорю "Анкета" или Начать поиск',
                                 reply_markup=make_buttons(choice_profile_or_find))
        else:
            await message.answer('В целом я всё запомнил, но пока у меня нет БД чтобы поменять твои данные')
            # await message.answer('Что-то пошло не так:/ Попробуй еще раз или нажми на кнопку "Назад"')


@router.message(BotStateMain.my_profile)
async def my_profile(message: types.Message, state: FSMContext):
    if message.text == 'Изменить анкету':
        await state.set_state(BotStateMain.change_info)
        await message.answer('Формат ввода изменения данных, вводи парами через запятую\n Пример: имя Артем, возраст 28')
    elif message.text == 'Назад':
        await state.set_state(BotState.main)
        await main_waiter(message, state)
    elif message.text == 'Остановить анкету':
        await message.answer('Твоя анкета убрана из поиска.\nНапиши "/start" если захочешь вернуться!',
                             reply_markup=ReplyKeyboardRemove())
        pass #TODO Поставить active_account=False
    else:
        #TODO Заменить файл на БД
        with open('save.txt', 'r') as file:
            info = file.read()
        await message.answer(f'Тут ты можешь изменить свою анкету. Вот что ты можешь изменить\n{info}',
                             reply_markup=make_buttons(choice_profile))


@router.message(BotState.main)
async def main_waiter(message: types.Message, state: FSMContext):
    if message.text.lower() == 'анкета':
        await state.set_state(BotStateMain.my_profile)
        await my_profile(message, state)
    elif message.text.lower() == 'начать поиск':
        await state.set_state(BotStateFind.find)
        await find_main(message, state)
    else:
        await message.answer('Тут ты можешь категорю "Анкета" или "Начать поиск"',
                             reply_markup=make_buttons(choice_profile_or_find))

