from aiogram import Router, F, types
from aiogram.types import FSInputFile
from motor.core import AgnosticDatabase

from bot.sections.user.test_task.services import get_bot_stage, prepare_response_based_on_stage
from bot.stages.utils.bot_stage_filter import BotStageFilter
from bot.utils.middleware.Time import is_duplicate_request

router = Router()

@router.message(F.text == "Тестове Завдання📝",  BotStageFilter(["test", "before_event"]))
async def test_task(message: types.Message, db: AgnosticDatabase):
    user_id = message.from_user.id
    message_text = message.text or ""

    if is_duplicate_request(user_id, message_text):
        return

    bot_stage = await get_bot_stage(db)

    response = await prepare_response_based_on_stage(bot_stage)

    if "error" in response:
        await message.answer(response["error"], parse_mode="HTML")
        return

    if "photo_path" in response:
        photo = FSInputFile(response["photo_path"])
        await message.answer_photo(photo=photo, caption=response["caption"], parse_mode="HTML")
    elif "link" in response:
        await message.answer(response["caption"], disable_web_page_preview=True, parse_mode="HTML")
