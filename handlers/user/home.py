from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from handlers.states import HomeState
from keyboards.callbacks import HomeCallback
from keyboards.questions import category_keyboard

router = Router()


@router.message(Command("start"))
async def home(message: Message, state: FSMContext, cursor):
    await state.set_state(HomeState.wait_home)
    await message.answer(text="Привет я Юрист-бот! "
                              "\n\nВыберите категорию:"
                              "\nСтудент\nРабочий", reply_markup=category_keyboard())