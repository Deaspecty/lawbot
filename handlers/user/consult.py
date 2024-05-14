import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy.ext.asyncio import AsyncSession

from handlers.states import HomeState
from handlers.user.home import home
from keyboards.questions import yes_or_no
from keyboards.callbacks import AnswerCallback, HomeCallback, DatetimeCallback, CategoryCallback
from models.question import get_all_questions, get_questions_by_category
from models.results import find_result, create_all_combinations

router = Router()


@router.callback_query(AnswerCallback.filter())
async def consult_answer(callback: CallbackQuery, callback_data: AnswerCallback, state: FSMContext, cursor, user):
    data = await state.get_data()
    category_id = data.get("category_id")
    questions = get_questions_by_category(cursor, category_id=category_id)
    answers = data.get("answers") + [True if callback_data.action == "yes" else False]
    now = len(answers)
    await state.update_data(answers=answers)

    if len(questions) > now:
        await callback.message.edit_text(text=questions[now][1], reply_markup=yes_or_no())
    else:
        await callback.message.edit_text(text=find_result(cursor, answers, category_id))
        await home(callback.message, state, user, cursor)
    await callback.answer()


# @router.callback_query(HomeCallback.filter(F.action == "answer"), HomeState.wait_home)
# async def consult_home(callback: CallbackQuery, callback_data: dict, state: FSMContext, cursor, user):
#     questions = get_all_questions(cursor)
#
#     await callback.answer()
#     await callback.message.edit_text(text=questions[0][1], reply_markup=yes_or_no())
#     await state.update_data(answers=[])


@router.callback_query(CategoryCallback.filter(F.action == "choose"))
async def choose_category(callback: CallbackQuery, callback_data: CategoryCallback, state: FSMContext, cursor, user):
    category_id = callback_data.category_id
    questions = get_questions_by_category(cursor, category_id=category_id)
    await callback.message.edit_text(text=questions[0][1], reply_markup=yes_or_no())
    await state.update_data(answers=[], category_id=category_id)
    await callback.answer()


@router.message(F.text == "gac3")
async def generate_all_combinations(message: Message, state: FSMContext, cursor):
    create_all_combinations(cursor)