from aiogram import Router, F, types
from aiogram.types import FSInputFile

from bot.stages.after_event.data import feedback_form_link, feedback_form_caption, winners_photo, winners_caption, \
    supporters_photo, supporters_caption
from bot.utils.keyboards.after_event_keyboard import get_feedback_form_keyboard
from bot.utils.middleware.Time import is_duplicate_request

router = Router()



@router.message(F.text == "Фідбек форма✍🏻")
async def handle_feedback_form(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    reply_markup = get_feedback_form_keyboard(feedback_form_link)
    await message.answer(feedback_form_caption, reply_markup=reply_markup, parse_mode="HTML")

@router.message(F.text == "Переможці🏆")
async def handle_winners(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    try:
        photo = FSInputFile(winners_photo)
        await message.answer_photo(photo=photo, caption=winners_caption, parse_mode="HTML")
    except FileNotFoundError:
        await message.answer(winners_caption, parse_mode="HTML")

@router.message(F.text == "Нас Підтримували🤍")
async def handle_supporters(message: types.Message):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    try:
        photo = FSInputFile(supporters_photo)
        await message.answer_photo(photo=photo, caption=supporters_caption, parse_mode="HTML")
    except FileNotFoundError:
        await message.answer(supporters_caption, parse_mode="HTML")