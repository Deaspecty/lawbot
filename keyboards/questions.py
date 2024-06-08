from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import AnswerCallback, CategoryCallback, HomeCallback
from models.question import get_questions


def yes_or_no():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Да", callback_data=AnswerCallback(action="yes").pack()),
        InlineKeyboardButton(text="Нет", callback_data=AnswerCallback(action="no").pack())
    ]])


def c_u_a():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Колледж", callback_data=AnswerCallback(action="cg").pack()),
        InlineKeyboardButton(text="Универ", callback_data=AnswerCallback(action="vuz").pack()),
        InlineKeyboardButton(text="Армия", callback_data=AnswerCallback(action="army").pack())
    ]])


def category_keyboard():
    ikb = InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Студент", callback_data=HomeCallback(action=1).pack()),
        InlineKeyboardButton(text="Рабочий", callback_data=HomeCallback(action=2).pack())
    ]])
    return ikb