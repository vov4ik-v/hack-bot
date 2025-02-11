from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

from bot.sections.user.my_team.data import chat_link


def get_team_keyboard(is_in_team: bool) -> ReplyKeyboardMarkup:
    if is_in_team:
        keyboard = [
            [
                KeyboardButton(text="Надіслати GitHub-репозиторій📂"),
                KeyboardButton(text="Надіслати резюме📄"),
            ],
            [
                KeyboardButton(text="Покинути команду🚪"),
                KeyboardButton(text="Головне меню🏠"),
            ]
        ]

    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)


def cancel_keyboard() -> ReplyKeyboardMarkup:
    keyboard = [
        [KeyboardButton(text="Скасувати❌")]
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)

def cancel_send_github_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Скасувати❌")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


def not_in_team_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="Увійти в команду", callback_data="join_team")],
        [InlineKeyboardButton(text="Зареєструвати команду", callback_data="create_team")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def handle_find_team_keyboard() -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text="Долучитись до чату", url=chat_link)]
    ]
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


