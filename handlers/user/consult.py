import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.states import HomeState, QuestionState
from handlers.user.home import home
from keyboards.questions import yes_or_no
from keyboards.callbacks import AnswerCallback, HomeCallback, DatetimeCallback, CategoryCallback
from models.question import get_questions, get_questions
from models.results import find_result, create_all_combinations

router = Router()


@router.callback_query(AnswerCallback.filter(), QuestionState.wait_bool)
async def consult_answer(callback: CallbackQuery, callback_data: AnswerCallback, state: FSMContext, cursor, user):
    data = await state.get_data()
    category_id = data.get("category_id")
    questions = get_questions(cursor, category_id=category_id)
    answers = data.get("answers") + [True if callback_data.action == "yes" else False]
    now = len(answers)
    await state.update_data(answers=answers, msg_id=callback.message.message_id)

    if len(questions) > now:
        if questions[now][4] == "bool":
            await callback.message.edit_text(text=questions[now][1], reply_markup=yes_or_no())
            await state.set_state(QuestionState.wait_bool)
        elif questions[now][4] == "text":
            await callback.message.edit_text(text=questions[now][1])
            await state.set_state(QuestionState.wait_text)
    else:
        await callback.message.edit_text(text=find_result(cursor, answers, category_id))
        await home(callback.message, state, cursor)
    await callback.answer()


@router.message(F.text, QuestionState.wait_text)
async def consult_answer(message: Message, state: FSMContext, cursor, user):
    data = await state.get_data()
    category_id = data.get("category_id")
    msg_id = data.get("msg_id")
    questions = get_questions(cursor, category_id=category_id)
    answers = data.get("answers") + [message.text]
    now = len(answers)
    await state.update_data(answers=answers)

    if len(questions) > now:
        if questions[now][4] == "bool":
            await message.bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
                                                text=questions[now][1], reply_markup=yes_or_no())
            await state.set_state(QuestionState.wait_bool)
        elif questions[now][4] == "text":
            await message.bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id, text=questions[now][1])
            await state.set_state(QuestionState.wait_text)
    else:
        await message.bot.edit_message_text(chat_id=message.from_user.id, message_id=msg_id,
                                            text=find_result(cursor, answers, category_id))
        await home(message, state, cursor)
    await message.delete()


@router.callback_query(CategoryCallback.filter(F.action == "choose"))
async def choose_category(callback: CallbackQuery, callback_data: CategoryCallback, state: FSMContext, cursor, user):
    category_id = callback_data.category_id
    questions = get_questions(cursor, category_id=category_id)
    if questions[0][4] == "bool":
        await callback.message.edit_text(text=questions[0][1], reply_markup=yes_or_no())
        await state.set_state(QuestionState.wait_bool)
    elif questions[0][4] == "text":
        await callback.message.edit_text(text=questions[0][1])
        await state.set_state(QuestionState.wait_text)

    await state.update_data(answers=[], category_id=category_id, msg_id=callback.message.message_id)
    await callback.answer()


@router.message(F.text == "gac3")
async def generate_all_combinations(message: Message, state: FSMContext, cursor):
    create_all_combinations(cursor)