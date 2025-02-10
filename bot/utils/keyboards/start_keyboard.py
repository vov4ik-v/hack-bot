from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from motor.core import AgnosticDatabase

async def get_user_team_info(db: AgnosticDatabase, user_id: int):

    user = await db.get_collection("users").find_one({"chat_id": user_id})
    if not user or "team_id" not in user:
        return False, False

    team = await db.get_collection("teams").find_one({"_id": user["team_id"]})
    if not team:
        return False, False

    return team.get("test_task_status", False), team.get("participation_status", False)


def get_start_keyboard(
    stage: str,
    is_registered: bool,
    test_approved: bool,
    event_approved: bool
) -> ReplyKeyboardMarkup:

    if stage == "before_registration":
        if is_registered:
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Більше про BEST"),
                        KeyboardButton(text="Більше про HACKath0n"),
                    ]
                ],
                resize_keyboard=True
            )
        else:
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Більше про BEST"),
                        KeyboardButton(text="📝 Реєстрація")
                    ],
                    [
                        KeyboardButton(text="Більше про HACKath0n")
                    ]
                ],
                resize_keyboard=True
            )

    elif stage == "registration":
        if is_registered:
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Більше про BEST"),
                        KeyboardButton(text="Більше про HACKath0n")
                    ],
                    [
                        KeyboardButton(text="Моя Команда"),
                        KeyboardButton(text="Знайти команду")
                    ]
                ],
                resize_keyboard=True
            )
        else:
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Більше про BEST"),
                        KeyboardButton(text="📝 Реєстрація")
                    ],
                    [
                        KeyboardButton(text="Більше про HACKath0n")
                    ]
                ],
                resize_keyboard=True
            )

    elif stage == "test":
        if not test_approved:
            if is_registered:
                return ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="Більше про BEST"),
                            KeyboardButton(text="Більше про HACKath0n")
                        ],
                        [
                            KeyboardButton(text="Моя Команда"),
                            KeyboardButton(text="Знайти команду")
                        ]
                    ],
                    resize_keyboard=True
                )
            else:
                return ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="Більше про BEST"),
                            KeyboardButton(text="📝 Реєстрація")
                        ],
                        [
                            KeyboardButton(text="Більше про HACKath0n")
                        ]
                    ],
                    resize_keyboard=True
                )
        else:
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="Більше про BEST"),
                        KeyboardButton(text="Більше про HACKath0n"),
                    ],
                    [
                        KeyboardButton(text="Моя Команда"),
                        KeyboardButton(text="Тестове Завдання")
                    ]
                ],
                resize_keyboard=True
            )

    elif stage == "before_event":
        if not event_approved:
            if test_approved:
                return ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="Більше про BEST"),
                            KeyboardButton(text="Більше про HACKath0n"),
                        ],
                        [
                            KeyboardButton(text="Моя Команда"),
                            KeyboardButton(text="Тестове Завдання")
                        ]
                    ],
                    resize_keyboard=True
                )
            else:
                if is_registered:
                    return ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Більше про BEST"),
                                KeyboardButton(text="Більше про HACKath0n")
                            ],
                            [
                                KeyboardButton(text="Моя Команда"),
                                KeyboardButton(text="Знайти команду")
                            ]
                        ],
                        resize_keyboard=True
                    )
                else:
                    return ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Більше про BEST"),
                                KeyboardButton(text="📝 Реєстрація")
                            ],
                            [
                                KeyboardButton(text="Більше про HACKath0n")
                            ]
                        ],
                        resize_keyboard=True
                    )
        else:
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
        if not event_approved:
            if test_approved:
                return ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="Більше про BEST"),
                            KeyboardButton(text="Більше про HACKath0n"),
                        ],
                        [
                            KeyboardButton(text="Моя Команда"),
                            KeyboardButton(text="Тестове Завдання")
                        ]
                    ],
                    resize_keyboard=True
                )
            else:
                if is_registered:
                    return ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Більше про BEST"),
                                KeyboardButton(text="Більше про HACKath0n")
                            ],
                            [
                                KeyboardButton(text="Моя Команда"),
                                KeyboardButton(text="Знайти команду")
                            ]
                        ],
                        resize_keyboard=True
                    )
                else:
                    return ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Більше про BEST"),
                                KeyboardButton(text="📝 Реєстрація")
                            ],
                            [
                                KeyboardButton(text="Більше про HACKath0n")
                            ]
                        ],
                        resize_keyboard=True
                    )
        else:
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
        if not event_approved:
            if test_approved:
                return ReplyKeyboardMarkup(
                    keyboard=[
                        [
                            KeyboardButton(text="Більше про BEST"),
                            KeyboardButton(text="Більше про HACKath0n"),
                        ],
                        [
                            KeyboardButton(text="Моя Команда"),
                            KeyboardButton(text="Тестове Завдання")
                        ]
                    ],
                    resize_keyboard=True
                )
            else:
                if is_registered:
                    return ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Більше про BEST"),
                                KeyboardButton(text="Більше про HACKath0n")
                            ],
                            [
                                KeyboardButton(text="Моя Команда"),
                                KeyboardButton(text="Знайти команду")
                            ]
                        ],
                        resize_keyboard=True
                    )
                else:
                    return ReplyKeyboardMarkup(
                        keyboard=[
                            [
                                KeyboardButton(text="Більше про BEST"),
                                KeyboardButton(text="📝 Реєстрація")
                            ],
                            [
                                KeyboardButton(text="Більше про HACKath0n")
                            ]
                        ],
                        resize_keyboard=True
                    )
        else:
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

    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Головне меню")]
        ],
        resize_keyboard=True
    )
