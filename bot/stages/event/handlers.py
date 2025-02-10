from aiogram import Router, F, types
from aiogram.types import FSInputFile

from bot.stages.event.data import (
    event_rules_photo, event_rules_caption,
    main_task_photo, main_task_caption,
    schedule_photo, schedule_caption, schedule_link,
    team_help_photo, team_help_caption
)
from bot.stages.utils.bot_stage_filter import BotStageFilter
from bot.utils.keyboards.event_keyboard import get_schedule_keyboard
from bot.utils.middleware.Time import is_duplicate_request

router = Router()

@router.message(F.text == "Правила поведінки на хакатоні📜", BotStageFilter("event"))
async def handle_event_rules(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(event_rules_photo)
    await message.answer_photo(photo=photo, caption=event_rules_caption, parse_mode="HTML")

@router.message(F.text == "Основне Завдання🎯", BotStageFilter("event"))
async def handle_main_task(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(main_task_photo)
    await message.answer_photo(photo=photo, caption=main_task_caption, parse_mode="HTML")

@router.message(F.text == "Розклад🕒", BotStageFilter("event"))
async def handle_schedule(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(schedule_photo)
    reply_markup = get_schedule_keyboard(schedule_link)
    await message.answer_photo(photo=photo, caption=schedule_caption, reply_markup=reply_markup, parse_mode="HTML")

@router.message(F.text == "Команді потрібна допомога🆘", BotStageFilter("event"))
async def handle_team_help(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    photo = FSInputFile(team_help_photo)
    await message.answer_photo(photo=photo, caption=team_help_caption, parse_mode="HTML")