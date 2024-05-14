from aiogram.filters.callback_data import CallbackData


class HomeCallback(CallbackData, prefix='home'):
    action: str


class AnswerCallback(CallbackData, prefix='answer'):
    action: str


class DatetimeCallback(CallbackData, prefix='datetime'):
    action: str
    dt: str


class CategoryCallback(CallbackData, prefix='category'):
    action: str
    category_id: int