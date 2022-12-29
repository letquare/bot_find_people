from aiogram.fsm.state import StatesGroup, State


class BotStateFind(StatesGroup):

    find = State()
    find_filter = State()
    find_choice = State()


class BotState(StatesGroup):

    name = State()
    how_old_u = State()
    photo = State()
    what_u_do = State()
    about_you = State()
    city = State()
    main = State()


class BotStateMain(StatesGroup):

    my_profile = State()
    change_info = State()


