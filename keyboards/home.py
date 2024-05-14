from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.callbacks import HomeCallback, AnswerCallback


def home_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Записаться на консультацию", callback_data=HomeCallback(action="answer").pack()),
        InlineKeyboardButton(text="О компании", callback_data=HomeCallback(action="faq").pack())
    ]])
