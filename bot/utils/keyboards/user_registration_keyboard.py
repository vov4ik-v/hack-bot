from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

contact_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📞 Поділитись контактом", request_contact=True)]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

consent_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Погоджуюсь", callback_data="consent_yes")]
    ],
    one_time_keyboard=True
)

university_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="НУЛП")],
        [KeyboardButton(text="ЛНУ")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

course_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="1"), KeyboardButton(text="2")],
        [KeyboardButton(text="3"), KeyboardButton(text="4"), KeyboardButton(text="5")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)
