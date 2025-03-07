from aiogram.fsm.state import StatesGroup, State


class TeamCreationStates(StatesGroup):
    waiting_for_team_name = State()
    waiting_for_team_password = State()
    waiting_for_category = State()

class TeamJoinStates(StatesGroup):
    waiting_for_team_name = State()
    waiting_for_team_password = State()

class TeamGitHubStates(StatesGroup):
    waiting_for_github_link = State()

class TeamCVStates(StatesGroup):
    waiting_for_cv = State()

class TeamCategoryStates(StatesGroup):
    waiting_for_category = State()
