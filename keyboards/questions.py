from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.callbacks import AnswerCallback, CategoryCallback
from models.question import get_all_questions


def yes_or_no():
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="Да", callback_data=AnswerCallback(action="yes").pack()),
        InlineKeyboardButton(text="Нет", callback_data=AnswerCallback(action="no").pack())
    ]])


def category_keyboard(cursor):
    category_count = 0
    ikb = []
    for q in get_all_questions(cursor):
        if category_count < q[3]:
            category_count = q[3]
    for i in range(1, category_count+1):
        ikb.append(InlineKeyboardButton(text=str(i),
                                        callback_data=CategoryCallback(action="choose", category_id=i).pack()))
    return InlineKeyboardMarkup(inline_keyboard=[ikb])