from aiogram import Router, F
from aiogram.enums import ContentType
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from sqlalchemy.ext.asyncio import AsyncSession
from handlers.states import AuthState
from handlers.user.home import home
from keyboards.auth import contact_keyboard
from methods.parse_phone import parse_phone
from models.user import save_user

router = Router()


@router.message(AuthState.wait_name)
async def save_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(AuthState.wait_phone)
    await message.answer(text="Нажмите на кнопку \"Поделится номером\"", reply_markup=contact_keyboard())


@router.message(AuthState.wait_phone, F.contact)
async def save_phone(message: Message, state: FSMContext, user, cursor):
    data = await state.get_data()
    phone_number = parse_phone(message.contact.phone_number)
    save_user(cursor, phone_number, data.get("name"), message.from_user.id)

    await message.answer("Вы успешно авторизовались.")
    await home(message, state, user)