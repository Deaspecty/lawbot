from aiogram import Dispatcher

from handlers.states import AuthState, HomeState
from handlers.user.auth import save_name, save_phone
from handlers.user.consult import consult_home, consult_answer
from handlers.user.home import home, faq
from keyboards.callbacks import HomeCallback, AnswerCallback


def register_home(dp: Dispatcher):
    dp.register_message_handler(home, commands=["start"], state="*")
    dp.register_callback_query_handler(consult_home, HomeCallback.filter(goto="consult", action="answer"), state=HomeState.wait_home)
    dp.register_callback_query_handler(faq, HomeCallback.filter(goto="faq", action="home"), state=HomeState.wait_home)


def register_auth(dp: Dispatcher):
    dp.register_message_handler(save_name, state=AuthState.wait_name)
    dp.register_message_handler(save_phone, content_types=["contact"], state=AuthState.wait_phone)


def register_answer(dp: Dispatcher):
    dp.register_callback_query_handler(consult_answer, AnswerCallback.filter(), state="*")


def register_user(dp: Dispatcher):
    register_home(dp)
    register_auth(dp)
    register_answer(dp)
