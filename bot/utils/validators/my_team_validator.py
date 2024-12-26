from aiogram.types import Message


async def validate_text_only(message: Message,max_length: int = 4000) -> bool:
    if not message.text or len(message.text) > max_length:
        await message.answer("Будь ласка, введи текстове повідомлення. 🤡")
        return False
    return True