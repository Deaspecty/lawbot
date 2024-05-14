from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def contact_keyboard():
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="Поделится номером", request_contact=True)]],
                               resize_keyboard=True)
