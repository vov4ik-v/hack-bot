from aiogram.filters import Filter
from aiogram.types import Message
from motor.core import AgnosticDatabase

class BotStageFilter(Filter):

    def __init__(self, expected_stages):
        if isinstance(expected_stages, str):
            self.expected_stages = [expected_stages]
        else:
            self.expected_stages = expected_stages

    async def __call__(self, message: Message, db: AgnosticDatabase) -> bool:
        collection = db.get_collection("bot_stage")

        doc = await collection.find_one({})
        if not doc or "stage" not in doc:
            return False
        current_stage = doc["stage"]
        return current_stage in self.expected_stages
