from aiogram.fsm.state import StatesGroup, State


class AdminStates:
    waiting_for_team_selection = "waiting_for_team_selection"

class BroadcastStates(StatesGroup):
    waiting_for_message = State()

class StageSelectionStates(StatesGroup):
    waiting_for_stage = State()