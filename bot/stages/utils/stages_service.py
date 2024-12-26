from motor.core import AgnosticDatabase


async def get_current_stage(db: AgnosticDatabase) -> str:
    collection = db.get_collection("bot_stage")
    doc = await collection.find_one({})
    if not doc or "stage" not in doc:
        return "unknown"
    return doc["stage"]