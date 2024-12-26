from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_schedule_keyboard(schedule_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Переглянути Розклад", url=schedule_link)]
        ]
    )