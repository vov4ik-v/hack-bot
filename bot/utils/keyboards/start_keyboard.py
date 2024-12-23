from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_keyboard(is_registered: bool) -> ReplyKeyboardMarkup:
    if is_registered:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Більше про BEST"),
                    KeyboardButton(text="Більше про HACKath0n"),
                    KeyboardButton(text="Моя Команда"),
                    KeyboardButton(text="Тестове Завдання")
                ]
            ],
            resize_keyboard=True
        )
    else:
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Більше про BEST"),
                    KeyboardButton(text="📝 Реєстрація"),
                    KeyboardButton(text="Більше про HACKath0n")
                ]
            ],
            resize_keyboard=True
        )