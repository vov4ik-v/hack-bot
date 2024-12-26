from aiogram.fsm.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_university = State()
    waiting_for_course = State()
    waiting_for_technologies = State()
    waiting_for_source = State()
    waiting_for_it_experience = State()
    waiting_for_contact = State()
    waiting_for_email = State()
    waiting_for_consent = State()