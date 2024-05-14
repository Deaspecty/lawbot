from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from handlers.states import HomeState, AuthState
from keyboards.auth import contact_keyboard
from keyboards.callbacks import HomeCallback
from keyboards.home import home_keyboard
from keyboards.questions import category_keyboard

router = Router()


@router.message(Command("start"))
async def home(message: Message, state: FSMContext, user, cursor):
    print(user)
    if user[1] is None:
        await message.answer(text="Как к вам обращаться?")
        await state.set_state(AuthState.wait_name)
    elif user[3] is None:
        await message.answer(text="Нажмите на кнопку \"Поделится номером\"", reply_markup=contact_keyboard())
    else:
        await state.set_state(HomeState.wait_home)
        await message.answer(text="Привет я Юрист-бот! "
                                  "\n\nВыберите категорию:"
                                  "\nКатегория 1\nКатегория 2\nКатегория 3", reply_markup=category_keyboard(cursor))


@router.callback_query(HomeCallback.filter(F.action == "faq"))
async def faq(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(text='КУЯЯЯ')