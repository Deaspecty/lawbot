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
        cursor.execute(f"SELECT * FROM users WHERE id = {event.from_user.id}")
        user = cursor.fetchone()
        if user is None or user == ():
            cursor.execute("INSERT INTO users(id, fullname, is_admin) VALUES (%s, %s, false)",
                           (event.from_user.id, event.from_user.full_name))
        data["user"] = user
        return await handler(event, data)
