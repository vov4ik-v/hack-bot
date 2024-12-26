from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_participants_chat_keyboard(chat_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Посилання на чат", url=chat_link)]
        ]
    )

def get_general_info_keyboard(guide_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Посилання на Survival Guide", url=guide_link)]
        ]
    )