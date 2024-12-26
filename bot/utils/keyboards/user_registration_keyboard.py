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
        [KeyboardButton(text="НУЛП"),
        KeyboardButton(text="ЛНУ"),
        KeyboardButton(text="УКУ"),
        KeyboardButton(text="КПІ"),
        KeyboardButton(text="КНУ"),
        KeyboardButton(text="Ще в школі"),
        KeyboardButton(text="Вже закінчив (-ла)")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

course_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Перший"), KeyboardButton(text="Другий")],
        [KeyboardButton(text="Третій"), KeyboardButton(text="Четвертий"), KeyboardButton(text="На магістратурі"), KeyboardButton(text="Нічого з переліченого")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

