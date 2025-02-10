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
         KeyboardButton(text="ЛНУ")],
        [KeyboardButton(text="УКУ"),
         KeyboardButton(text="КПІ")],
        [KeyboardButton(text="КНУ"),
         KeyboardButton(text="Ще в школі")],
        [KeyboardButton(text="Вже закінчив (-ла)")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
)

course_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Перший"), KeyboardButton(text="Другий")],
        [KeyboardButton(text="Третій"), KeyboardButton(text="Четвертий")],
        [KeyboardButton(text="На магістратурі"), KeyboardButton(text="Нічого з переліченого")]
    ],
    resize_keyboard=True,
    one_time_keyboard=True
) 

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_source_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Був(-ла) учасником(-цею) проєкту(-ів)")],
            [KeyboardButton(text="Від друзів, які теж подаються")],
            [KeyboardButton(text="Від друзів, що є в організації")],
            [KeyboardButton(text="Побачив(-ла) в Instagram")],
            [KeyboardButton(text="Побачив(-ла) у TikTok")],
            [KeyboardButton(text="Почув(-ла) на інфостійках або живих оголошеннях")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_it_experience_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Так"), KeyboardButton(text ="Ні")],
            [KeyboardButton(text ="Планую")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


