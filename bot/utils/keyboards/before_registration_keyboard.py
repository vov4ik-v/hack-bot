from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

about_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти на Instagram", url="https://www.instagram.com/best_lviv/"),
            InlineKeyboardButton(text="Перейти на сайт", url="https://www.best-lviv.org.ua/ua")
        ]
    ]
)

hackathon_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Перейти на сайт", url="https://hack-2025.best-lviv.org.ua")
        ]
    ]
)