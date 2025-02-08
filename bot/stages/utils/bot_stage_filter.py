from aiogram.filters import Filter
from aiogram.types import Message
from motor.core import AgnosticDatabase
from bson import ObjectId

class BotStageFilter(Filter):

    def __init__(self, expected_stages):
        if isinstance(expected_stages, str):
            self.expected_stages = [expected_stages]
        else:
            self.expected_stages = expected_stages

    async def __call__(self, message: Message, db: AgnosticDatabase) -> bool:
        doc = await db.get_collection("bot_stage").find_one({})
        if not doc or "stage" not in doc:
            return False

        current_stage = doc["stage"]

        if current_stage not in self.expected_stages:
            return False


        if current_stage == "test":
            if not await self._is_test_approved(db, message.from_user.id):
                return False

        elif current_stage in ("before_event", "event", "after_event"):
            if not await self._is_event_approved(db, message.from_user.id):
                return False

        return True

    async def _is_test_approved(self, db: AgnosticDatabase, user_id: int) -> bool:
        user = await db.get_collection("users").find_one({"chat_id": user_id})
        if not user or "team_id" not in user:
            return False

        team = await db.get_collection("teams").find_one({"_id": user["team_id"]})
        if not team:
            return False

        return team.get("test_task_status", False) is True

    async def _is_event_approved(self, db: AgnosticDatabase, user_id: int) -> bool:
        user = await db.get_collection("users").find_one({"chat_id": user_id})
        if not user or "team_id" not in user:
            return False

        team = await db.get_collection("teams").find_one({"_id": user["team_id"]})
        if not team:
            return False

        return team.get("participation_status", False) is True
