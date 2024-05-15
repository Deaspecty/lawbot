from aiogram.fsm.state import StatesGroup, State


class HomeState(StatesGroup):
    wait_home = State()


class AuthState(StatesGroup):
    wait_name = State()
    wait_phone = State()


class QuestionState(StatesGroup):
    wait_bool = State()
    wait_text = State()