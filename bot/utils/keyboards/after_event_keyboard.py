from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_feedback_form_keyboard(feedback_form_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Фідбек форма", url=feedback_form_link)]
        ]
    )