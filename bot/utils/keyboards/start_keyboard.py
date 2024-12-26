from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_start_keyboard(stage: str, is_registered: bool = False) -> ReplyKeyboardMarkup:
    if stage == "before_registration" or stage == "registration":
        if is_registered:
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Більше про BEST"),
                        KeyboardButton(text="Більше про HACKath0n"),
                        KeyboardButton(text="Моя Команда"),
                        KeyboardButton(text="Знайти команду"),
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
    elif stage == "before_event":
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Моя Команда"),
                    KeyboardButton(text="Де відбуватиметься івент"),
                ],
                [
                    KeyboardButton(text="Чат для учасників"),
                    KeyboardButton(text="Загальна інформація")
                ]
            ],
            resize_keyboard=True
        )
    elif stage == "event":
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Моя Команда"),
                    KeyboardButton(text="Правила поведінки на хакатоні"),
                ],
                [
                    KeyboardButton(text="Розклад"),
                    KeyboardButton(text="Основне Завдання"),
                ],
                [
                    KeyboardButton(text="Команді потрібна допомога")
                ]
            ],
            resize_keyboard=True
        )
    elif stage == "after_event":
        return ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(text="Нас Підтримували"),
                    KeyboardButton(text="Переможці"),
                ],
                [
                    KeyboardButton(text="Фідбек форма")
                ]
            ],
            resize_keyboard=True
        )
    else:
        # Дефолтна клавіатура або для інших стадій
        return ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Головне меню")]
            ],
            resize_keyboard=True
        )
