from aiogram import Router, F, types
from aiogram.types import FSInputFile

router = Router()

@router.message(F.text == "Тестове Завдання")
async def test_task(message: types.Message):
    photo_path = "asset/test_assignment_coming_soon_image.jpg"

    photo = FSInputFile(photo_path)

    await message.answer_photo(photo = photo, caption="""Ха-ха, а ти схоже дуже вмотивований учасник!🔥

24.04 тут з'явиться тестове завдання для вашої команди на відбір до змагань,
так що готуйте ваші лептопи💻😁""")