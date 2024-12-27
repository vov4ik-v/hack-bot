from motor.motor_asyncio import AsyncIOMotorClient
from config_reader import MONGO_URI

client = AsyncIOMotorClient(MONGO_URI)
db = client["hack_bot2025"]
