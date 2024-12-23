from aiogram import Router, F, types
from aiogram.types import FSInputFile

router = Router()

@router.message(F.text == "Моя Команда")
async def test_task(message: types.Message):
    photo_path = "asset/team_image.jpg"

    photo = FSInputFile(photo_path)

    await message.answer_photo(photo = photo, caption="""Дочекайся початку реєстрації, щоб створити або долучитись до команди💻""")