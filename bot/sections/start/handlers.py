from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton

from bot.database.connection import db
from bot.sections.user.registration.services import is_user_registered
from bot.utils.keyboards.start_keyboard import get_start_keyboard

router = Router()
photo_path_welcome = "asset/hack_start_photo.jpg"
photo_path_register = "asset/hack_register_photo.jpg"
photo_path_about_hack = "asset/hack_about_photo.jpg"

# Головне меню
@router.message(CommandStart())
async def welcome_user(message: Message):
    username = message.from_user.username

    is_registered = await is_user_registered(db, username)
    keyboard = get_start_keyboard(is_registered)


    photo = FSInputFile(photo_path_register)
    await message.answer_photo(photo=photo, caption='Вітаємо на BEST::HACKath0n`9!', reply_markup=keyboard)


# Інформація про BEST
@router.message(F.text == "Більше про BEST")
async def about_best(message: Message):
    about_text = (
        "BEST Lviv — європейська студентська волонтерська організація з 85 осередками в 30 країнах.\n\n"
        "Організація спрямована на розвиток студентів у сфері технологій, інженерії та менеджменту.\n\n"
        "Наша місія — розвиток студентів, а візія — сила у різноманітті\n\n"
        "Щороку, ми організовуємо близько 4-х масштабних івентів, серед яких:\n"
        "HACKath0n, BEC (Best Engineering Competition), BTW (BEST Training Week) та BCI (Best Company Insight).\n\n"
        "Детальніше про ці івенти ви можете дізнатися в нашому інстаграмі:"
    )
    photo = FSInputFile(photo_path_about_hack)
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
            InlineKeyboardButton(text="Перейти на Instagram", url="https://www.instagram.com/best_lviv/"),
            InlineKeyboardButton(text="Перейти на сайт", url="https://hack.best-lviv.org.ua")
            ]
        ]
    )
    await message.answer_photo(photo=photo, caption=about_text, reply_markup=reply_markup)

# Інформація про HACKath0n
@router.message(F.text == "Більше про HACKath0n")
async def about_hackathon(message: Message):
    hackathon_text = (
        "BEST::HACKath0n — це 24-х годинний марафон з програмування [Marathon + Hack = HACKath0n!] 👨‍💻\n\n"
        "• У нашому осередку цей проект проводиться вже ввосьме! 🤯\n"
        "• Цей проект дасть тобі, як учаснику, хороший пункт для твого CV, а також безцінний досвід роботи у команді 😎\n"
        "• Це прекрасна можливість випробувати та продемонструвати свої софт і хард скіли, отож лови її! 🔥"
    )
    photo = FSInputFile(photo_path_about_hack)
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Перейти на сайт", url="https://hack.best-lviv.org.ua")]
        ]
    )
    await message.answer_photo(photo=photo, caption=hackathon_text, reply_markup=reply_markup)