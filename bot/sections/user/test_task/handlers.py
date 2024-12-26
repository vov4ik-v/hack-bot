from aiogram import Router, F, types
from aiogram.types import FSInputFile
from motor.core import AgnosticDatabase

from bot.sections.user.test_task.services import get_bot_stage, prepare_response_based_on_stage

router = Router()

@router.message(F.text == "Тестове Завдання")
async def test_task(message: types.Message, db: AgnosticDatabase):
    bot_stage = await get_bot_stage(db)

    response = await prepare_response_based_on_stage(bot_stage)

    if "error" in response:
        await message.answer(response["error"])
        return

    if "photo_path" in response:
        photo = FSInputFile(response["photo_path"])
        await message.answer_photo(photo=photo, caption=response["caption"])
    elif "link" in response:
        await message.answer(response["caption"], disable_web_page_preview=True)
