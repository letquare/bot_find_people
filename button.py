from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton


def make_buttons(items: tuple[str, ...]) -> ReplyKeyboardMarkup:
    row = [KeyboardButton(text=item) for item in items]
    return ReplyKeyboardMarkup(keyboard=[row], resize_keyboard=True)
