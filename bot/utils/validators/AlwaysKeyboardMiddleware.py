from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.database.connection import db
from bot.utils.keyboards.start_keyboard import get_start_keyboard
from bot.sections.user.registration.services import is_user_registered

class AlwaysKeyboardMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if "reply_markup" in data:
            return await handler(event, data)

        username = event.from_user.username
        is_registered = await is_user_registered(db, username)

        data["reply_markup"] = get_start_keyboard(is_registered)
        return await handler(event, data)
