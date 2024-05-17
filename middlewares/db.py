from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
import config.config


class DbMiddleware(BaseMiddleware):
    skip_patterns = ["error", "update"]

    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject,
                       data: Dict[str, Any]):
        cursor = config.config.con.cursor()
        data["cursor"] = cursor
        return await handler(event, data)
