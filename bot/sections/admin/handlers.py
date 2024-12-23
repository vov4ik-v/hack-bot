from aiogram import Router, F, types
from aiogram.fsm.state import StatesGroup, State
from motor.core import AgnosticDatabase
from aiogram.fsm.context import FSMContext
from config_reader import ADMIN_PASSWORD
from . import keyboards

router = Router()


class AdminStates(StatesGroup):
    waiting_for_secretary_username = State()


@router.message(F.text == str(ADMIN_PASSWORD))
async def open_admin_panel(message: types.Message):
    await message.answer('Вітаю в адмінці')

