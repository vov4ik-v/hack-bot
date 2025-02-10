from motor.core import AgnosticDatabase


async def get_bot_stage(db: AgnosticDatabase):
    collection = db.get_collection("bot_stage")
    bot_stage = await collection.find_one({})
    return bot_stage


async def prepare_response_based_on_stage(bot_stage: dict) -> dict:
    if not bot_stage or "isTestReady" not in bot_stage or "linkForTest" not in bot_stage:
        return {
            "error": "Помилка: стадія не знайдена або дані некоректні."
        }

    if bot_stage["isTestReady"] == "false":
        return {
            "photo_path": "asset/test_assignment_coming_soon_image.png",
            "caption": (
                """Ого, ти справді <b>вмотивований учасник!</b> 💪

🧩 Тут з’явиться <b>тестове завдання</b> для твоєї команди.
🎮 Готуйте ноутбуки – справжні виклики вже чекають! 🚀"""
            )
        }
    else:
        return {
            "link": bot_stage["linkForTest"],
            "caption": (
                "Ну от і настав цей день 🔥\n\n"
                "Тестове завдання уже відкрите! Збирай свою команду до купи, адже ваша спільна робота починається 🤜🏻🤛🏻\n\n"
                f"➡️ [Перейти до тестового завдання]({bot_stage['linkForTest']}) ⬅️\n\n"
                "Чекаємо на виконане завдання до 28.04 23:59.\n\n"
                "Надсилайте вашу роботу на цю пошту \n"
                "➡️ hack@best-lviv.org.ua ⬅️\n\n"
                "Бажаємо удачі! Сподіваємось побачити на BEST::HACKath0n 2024 саме твою команду 💚"
            )
        }
