from aiogram import Router, F, types
from aiogram.types import FSInputFile

from bot.stages.utils.bot_stage_filter import BotStageFilter
from bot.stages.before_event.data import (
    event_location_photo, event_location_caption,
    participants_chat_photo, participants_chat_caption, participants_chat_link,
    general_info_photo, general_info_caption, general_info_link
)
from bot.utils.keyboards.before_event_keyboard import get_participants_chat_keyboard, get_general_info_keyboard
from bot.utils.middleware.Time import is_duplicate_request

router = Router()

@router.message(F.text == "Де відбуватиметься івент", BotStageFilter("before_event"))
async def handle_event_location(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(event_location_photo)
    await message.answer_photo(photo=photo, caption=event_location_caption, parse_mode="HTML")

@router.message(F.text == "Чат для учасників", BotStageFilter("before_event"))
async def handle_participants_chat(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(participants_chat_photo)
    reply_markup = get_participants_chat_keyboard(participants_chat_link)
    await message.answer_photo(photo=photo, caption=participants_chat_caption, reply_markup=reply_markup, parse_mode="HTML")

@router.message(F.text == "Загальна інформація", BotStageFilter("before_event"))
async def handle_general_info(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(general_info_photo)
    reply_markup = get_general_info_keyboard(general_info_link)
    await message.answer_photo(photo=photo, caption=general_info_caption, reply_markup=reply_markup, parse_mode="HTML")