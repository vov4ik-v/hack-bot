from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_admin_panel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Переключити секцію"),
                KeyboardButton(text="Розсилка")
            ],
            [
                KeyboardButton(text="Список команд"),
                KeyboardButton(text="Командна панель")
            ],
            [
                KeyboardButton(text="Головне меню🏠")
            ]
        ],
        resize_keyboard=True
    )

def get_team_panel_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Інформація про учасників"),
                KeyboardButton(text="Посилання на репо"),
            ],
            [
                KeyboardButton(text="Завантажити CV"),
                KeyboardButton(text="Список технологій"),
            ],
            [
                KeyboardButton(text="Видалити команду"),
                KeyboardButton(text="Апрувнути тестове завдання"),
            ],
            [
                KeyboardButton(text="Апрувнути участь в івенті"),
                KeyboardButton(text="Назад до адмін-панелі")
            ]
        ],
        resize_keyboard=True
    )

def get_broadcast_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Усі користувачі", callback_data="broadcast:all"),
                InlineKeyboardButton(text="Усі команди", callback_data="broadcast:teams"),
            ],
            [
                InlineKeyboardButton(text="Тільки учасники", callback_data="broadcast:participants"),
                InlineKeyboardButton(text="Тільки організатори", callback_data="broadcast:organizers"),
            ],
            [
                InlineKeyboardButton(text="Скасувати", callback_data="broadcast:cancel")
            ]
        ]
    )
