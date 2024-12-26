from aiogram import Router, F
from aiogram.types import Message, FSInputFile

from bot.stages.before_registration.data import photo_path_about_hack, about_text, hackathon_text
from bot.utils.keyboards.before_registration_keyboard import about_keyboard, hackathon_keyboard

router = Router()

@router.message(F.text == "Більше про BEST")
async def about_best(message: Message):
    photo = FSInputFile(photo_path_about_hack)
    await message.answer_photo(photo=photo, caption=about_text, reply_markup=about_keyboard)

@router.message(F.text == "Більше про HACKath0n")
async def about_hackathon(message: Message):
    photo = FSInputFile(photo_path_about_hack)
    await message.answer_photo(photo=photo, caption=hackathon_text, reply_markup=hackathon_keyboard)