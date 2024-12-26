from aiogram.fsm.state import StatesGroup, State
from motor.core import AgnosticDatabase


async def process_registration_data(db: AgnosticDatabase,state_data: dict):
    user_data = {
        "name": state_data.get("name"),
        "age": state_data.get("age"),
        "university": state_data.get("university"),
        "course": state_data.get("course"),
        "technologies": state_data.get("technologies"),
        "source": state_data.get("source"),
        "it_experience": state_data.get("it_experience"),
        "contact": state_data.get("contact"),
        "email": state_data.get("email"),
        "chat_id": state_data.get("chat_id")
    }
    await register_user(db, user_data)
    return user_data


async def register_user(db: AgnosticDatabase, data: dict):
    collection = db.get_collection("users")
    await collection.insert_one(data)


async def is_user_registered(db: AgnosticDatabase, username: str) -> bool:
    collection = db.get_collection("users")
    user = await collection.find_one({"contact.username": username})
    return user is not None
