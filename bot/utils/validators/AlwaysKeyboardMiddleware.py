from aiogram import BaseMiddleware
from aiogram.types import Message
from bot.database.connection import db
from bot.stages.utils.stages_service import get_current_stage
from bot.utils.keyboards.start_keyboard import get_start_keyboard, get_user_team_info
from bot.sections.user.quiz_about_user.services import is_user_registered

class AlwaysKeyboardMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: Message, data: dict):
        if "reply_markup" in data:
            return await handler(event, data)

        test_approved, event_approved = await get_user_team_info(db, event.from_user.id)
        username = event.from_user.username
        is_registered = await is_user_registered(db, username)
        stage = await get_current_stage(db)

        data["reply_markup"] = get_start_keyboard(stage,is_registered, test_approved, event_approved)
        return await handler(event, data)
