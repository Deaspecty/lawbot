from aiogram.fsm.state import StatesGroup, State


class HomeState(StatesGroup):
    wait_home = State()


class AuthState(StatesGroup):
    wait_name = State()
    wait_phone = State()