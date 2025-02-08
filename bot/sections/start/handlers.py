from aiogram import Router, F, types
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.connection import db
from bot.sections.user.quiz_about_user.services import is_user_registered
from bot.stages.utils.stages_service import get_current_stage
from bot.utils.keyboards.start_keyboard import get_start_keyboard, get_user_team_info
from bot.utils.middleware.Time import is_duplicate_request

router = Router()
photo_path_welcome = "asset/hack_start_photo.jpg"
photo_path_register = "asset/hack_register_photo.jpg"
photo_path_about_hack = "asset/hack_about_photo.jpg"

@router.message(CommandStart())
async def welcome_user(message: Message):
    username = message.from_user.username

    user_id = message.from_user.id
    message_text = message.text or ""
    test_approved, event_approved = await get_user_team_info(db, message.from_user.id)

    if is_duplicate_request(user_id, message_text):
        return

    is_registered = await is_user_registered(db, username)
    stage = await get_current_stage(db)
    keyboard = get_start_keyboard(stage,is_registered, test_approved, event_approved)


    photo = FSInputFile(photo_path_register)
    await message.answer_photo(photo=photo, caption='Вітаємо на BEST::HACKath0n`9!', reply_markup=keyboard)