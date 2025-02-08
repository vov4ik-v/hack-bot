from datetime import datetime
from aiogram.types import Message, FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from motor.core import AgnosticDatabase
from bot.utils.keyboards.start_keyboard import get_start_keyboard
from bot.sections.user.quiz_about_user.services import is_user_registered
from bot.stages.utils.stages_service import get_current_stage
from bson import ObjectId
from motor.core import AgnosticDatabase

from bot.utils.keyboards.team_keyboard import get_team_keyboard, not_in_team_keyboard


async def user_has_team(db: AgnosticDatabase, user_id: int) -> bool:
    """
    Перевіряємо, чи є у користувача (user_id) команда.
    Для прикладу: шукаємо в колекції users поле 'team_id'.
    """
    users_collection = db.get_collection("users")
    user_doc = await users_collection.find_one({"chat_id": user_id})
    if user_doc and user_doc.get("team_id"):
        return True
    return False


async def create_team(db: AgnosticDatabase, team_name: str, team_password: str) -> ObjectId:
    """
    Створює нову команду в колекції 'teams' та повертає її _id.
    """
    teams_collection = db.get_collection("teams")

    result = await teams_collection.insert_one({
        "name": team_name,
        "password": team_password,
        "github_repo": None,  # або "" - за замовчуванням
        "created_at": datetime.now(),
        "participation_status": False,
        "test_task_status": False,
    })
    return result.inserted_id


async def get_team_by_name(db: AgnosticDatabase, team_name: str) -> dict:
    """
    Повертає документ команди за її ім'ям або None, якщо не знайдено.
    """
    teams_collection = db.get_collection("teams")
    return await teams_collection.find_one({"name": team_name})


async def update_team_github(db: AgnosticDatabase, team_id: ObjectId, github_link: str):
    """
    Оновлює поле 'github_repo' у команди
    """
    teams_collection = db.get_collection("teams")
    await teams_collection.update_one(
        {"_id": team_id},
        {"$set": {"github_repo": github_link}}
    )


async def update_user_cv(db: AgnosticDatabase, user_id: int, file_id: str, file_name: str, file_size: int):
    """
    Зберігає дані про резюме (CV) у колекції користувача.
    """
    users_collection = db.get_collection("users")
    cv_data = {
        "file_id": file_id,
        "file_name": file_name,
        "file_size": file_size,
    }
    await users_collection.update_one(
        {"chat_id": user_id},
        {"$set": {"resume": cv_data}}
    )


async def set_user_team(db: AgnosticDatabase, user_id: int, team_id: ObjectId):
    """
    Записує в user колекції ідентифікатор (team_id) команди.
    """
    users_collection = db.get_collection("users")
    existing_user = await users_collection.find_one({"chat_id": user_id})
    if not existing_user:
        print(f"User with user_id={user_id} not found in the database.")
        return
    await users_collection.update_one(
        {"chat_id": user_id},
        {"$set": {"team_id": team_id}}
    )


async def unset_user_team(db: AgnosticDatabase, user_id: int):
    """
    Видаляє у користувача прив'язку до команди (team_id).
    """
    users_collection = db.get_collection("users")
    await users_collection.update_one(
        {"chat_id": user_id},
        {"$unset": {"team_id": ""}}
    )


async def get_team_by_id(db: AgnosticDatabase, team_id: ObjectId) -> dict:
    teams_collection = db.get_collection("teams")
    return await teams_collection.find_one({"_id": team_id})


async def send_team_info(message: Message, db: AgnosticDatabase, user_id: int):
    user_doc = await db.get_collection("users").find_one({"chat_id": user_id})
    photo_path = "asset/team_image.jpg"
    stage = await get_current_stage(db)
    username = message.from_user.username
    is_registered = await is_user_registered(db, username)
    photo = FSInputFile(photo_path)
    if not user_doc or not user_doc.get("team_id"):
        await message.answer_photo(photo, caption="""
        <b>Ти ще не в команді 🥲</b>
Щоб продовжити, створи власну команду або приєднайся до вже існуючої.
Командна робота – ключ до перемоги! 🏆

🔷 <b>Створи команду</b> – збери друзів або знайди нових!
🔷 <b>Приєднайся</b> – знайди команду та стань її частиною!""", reply_markup=not_in_team_keyboard(), parse_mode="HTML")
        return
    team_id = user_doc["team_id"]
    team_doc = await db.get_collection("teams").find_one({"_id": team_id})
    if not team_doc:
        await message.answer(
            "Команду не знайдено🥲. Можливо, вона була видалена. Створи нову або приєднайся до існуючої.",
            reply_markup=get_start_keyboard(stage, is_registered))
        return
    team_members_cursor = db.get_collection("users").find({"team_id": team_id})
    team_members = await team_members_cursor.to_list(length=None)
    members_info = []
    resumes_info = []
    for member in team_members:
        name = member.get("name", "Невідомо")
        contact = member.get("contact", {})
        username = contact.get("username", "")
        resume = member.get("resume")
        members_info.append(f"{name} - @{username}" if username else f"{name}")
        if resume:
            resumes_info.append(f"{name} - {resume['file_name']}")
        else:
            resumes_info.append(f"{name} - резюме не надіслано.")
    github_repo = team_doc.get("github_repo", "Ще не надіслано")
    if github_repo:
        github_info = github_repo
    else:
        github_info = "Ще не надіслано"

    test_task_status = team_doc.get("test_task_status", False)
    participation_status = team_doc.get("participation_status", False)
    test_task_display = "❌" if not test_task_status else "✅"
    participation_display = "✅" if participation_status else "❌"
    team_name = team_doc.get("name", "Невідома команда")
    members_text = "\n".join(members_info)
    resumes_text = "\n".join(resumes_info)
    response_text = (
        f"<b>Команда {team_name}</b>\n\n"
        f"<b>Учасники команди:</b>\n{members_text}\n\n"
        f"<b>Резюме:</b>\n{resumes_text}\n\n"
        f"<b>Гітхаб:</b> - {github_info}\n\n"
        f"<b>Команда допущена до тестового</b> - {test_task_display}\n"
        f"<b>Команда бере участь в хакатоні</b> - {participation_display}"
    )
    team_photo_path = "asset/team_image.jpg"
    try:
        photo = FSInputFile(team_photo_path)
        await message.answer_photo(photo=photo, caption=response_text, parse_mode="HTML",
                                   reply_markup=get_team_keyboard(True))
    except FileNotFoundError:
        await message.answer(response_text, parse_mode="HTML", reply_markup=get_team_keyboard(True))
