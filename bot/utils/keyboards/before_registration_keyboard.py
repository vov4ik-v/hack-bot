from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

about_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти на Instagram", url="https://www.instagram.com/best_lviv/"),
            InlineKeyboardButton(text="Перейти на сайт", url="https://hack.best-lviv.org.ua")
        ]
    ]
)

hackathon_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти на сайт", url="https://hack.best-lviv.org.ua")
        ]
    ]
)