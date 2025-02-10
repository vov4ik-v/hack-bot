from motor.core import AgnosticDatabase


async def get_current_stage(db: AgnosticDatabase):
    doc = await db.get_collection("bot_stage").find_one({})
    return doc.get("stage", "before_registration") if doc else "before_registration"

async def is_user_admin(db: AgnosticDatabase, chat_id: int) -> bool:
    user = await db.get_collection("users").find_one({"chat_id": chat_id})
    return user and user.get("is_admin", False)


async def update_stage(db: AgnosticDatabase, new_stage: str):
    await db.get_collection("bot_stage").update_one({}, {"$set": {"stage": new_stage}}, upsert=True)


async def list_teams(db: AgnosticDatabase):

    return await db.get_collection("teams").find({}).to_list(length=None)


async def get_user_team_id(db: AgnosticDatabase, user_id):
    user = await db.get_collection("users").find_one({"chat_id": user_id})
    return user.get("team_id") if user else None


async def get_team_members_info(db: AgnosticDatabase, team_id: str):
    members = await db.get_collection("users").find({"team_id": team_id}).to_list(length=None)
    if not members:
        return ""
    lines = []
    for member in members:
        username = member.get("contact", {}).get("username", "")
        name = member.get("name", "")
        line = f"{name} - @{username}" if username else name
        lines.append(line)
    return "\n".join(lines)


async def get_team_repo_link(db: AgnosticDatabase, team_id: str):
    team = await db.get_collection("teams").find_one({"_id": team_id})
    return team.get("github_repo") if team else None


async def delete_team(db: AgnosticDatabase, team_id: str):
    await db.get_collection("teams").delete_one({"_id": team_id})
    await db.get_collection("users").update_many({"team_id": team_id}, {"$unset": {"team_id": ""}})


async def approve_test_submission(db: AgnosticDatabase, team_id: str):
    await db.get_collection("teams").update_one({"_id": team_id}, {"$set": {"test_task_status": True}})


async def approve_event_participation(db: AgnosticDatabase, team_id: str):
    await db.get_collection("teams").update_one({"_id": team_id}, {"$set": {"participation_status": True}})

async def get_all_users(db: AgnosticDatabase):
    return await db.get_collection("users").find({}).to_list(length=None)

async def get_teams_by_test_status(db: AgnosticDatabase, status: bool):
    return await db.get_collection("teams").find({"test_task_status": status}).to_list(length=None)

async def get_teams_with_participation_status(db: AgnosticDatabase, status: bool):
    return await db.get_collection("teams").find({"participation_status": status}).to_list(length=None)

async def get_users_by_team_ids(db: AgnosticDatabase, team_ids: list):
    return await db.get_collection("users").find({"team_id": {"$in": team_ids}}).to_list(length=None)
